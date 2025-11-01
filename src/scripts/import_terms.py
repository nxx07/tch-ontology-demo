#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCH 本体术语导入脚本
TCH Ontology Term Import Script

功能 / Features:
- 从 CSV/Excel 文件导入术语到 tch-edit.owl
- 支持所有 11 个术语类别
- 自动验证字段和关系
- 生成导入报告

用法 / Usage:
    python import_terms.py --category pattern --input pattern_terms.csv
    python import_terms.py --category herb --input herb_terms.xlsx --validate-only
    
依赖 / Dependencies:
    pip install pandas openpyxl pyyaml rdflib owlready2
"""

import argparse
import sys
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd
import yaml
from owlready2 import get_ontology, locstr

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('term_import.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TCHTermImporter:
    """TCH 本体术语导入器"""
    
    def __init__(self, config_path: str, ontology_path: str):
        """
        初始化导入器
        
        Args:
            config_path: 配置文件路径
            ontology_path: 本体文件路径 (tch-edit.owl)
        """
        self.config_path = Path(config_path)
        self.ontology_path = Path(ontology_path)
        self.config = self._load_config()
        self.ontology = None
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
        
    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"配置文件加载成功: {self.config_path}")
            return config
        except Exception as e:
            logger.error(f"配置文件加载失败: {e}")
            sys.exit(1)
    
    def load_ontology(self):
        """加载本体文件"""
        try:
            if self.config['import_options']['backup_before_import']:
                backup_path = f"{self.ontology_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                import shutil
                shutil.copy(self.ontology_path, backup_path)
                logger.info(f"本体文件已备份: {backup_path}")
            
            # 使用 file:// 协议加载本地文件，明确指定格式
            onto_iri = f"file://{os.path.abspath(self.ontology_path)}"
            self.ontology = get_ontology(onto_iri).load(format="ofn")  # OWL Functional Syntax
            logger.info(f"本体文件加载成功: {self.ontology_path}")
        except Exception as e:
            logger.error(f"本体文件加载失败: {e}")
            logger.info("提示: 如果导入失败，请确保 tch-edit.owl 是有效的 OWL 格式")
            sys.exit(1)
    
    def load_terms_data(self, file_path: str) -> pd.DataFrame:
        """
        加载术语数据文件
        
        Args:
            file_path: CSV 或 Excel 文件路径
            
        Returns:
            pandas DataFrame
        """
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(
                    file_path,
                    encoding=self.config['import_options']['input_encoding'],
                    delimiter=self.config['import_options']['csv_delimiter']
                )
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
            
            # 去除空行
            if self.config['import_options']['skip_empty_rows']:
                df = df.dropna(how='all')
            
            # 去除字段前后空格
            if self.config['import_options']['strip_whitespace']:
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            
            logger.info(f"术语数据加载成功: {file_path}, 共 {len(df)} 条记录")
            return df
            
        except Exception as e:
            logger.error(f"术语数据加载失败: {e}")
            sys.exit(1)
    
    def validate_term_id(self, term_id: str, category: str) -> bool:
        """
        验证术语ID格式和范围
        
        Args:
            term_id: 术语ID (如 TCH_0001000)
            category: 术语类别
            
        Returns:
            验证是否通过
        """
        # 格式验证
        pattern = self.config['validation_rules']['id_format']['pattern']
        import re
        if not re.match(pattern, term_id):
            error_msg = self.config['validation_rules']['id_format']['error_message']
            logger.error(f"ID格式错误: {term_id} - {error_msg}")
            return False
        
        # 范围验证
        if self.config['validation_rules']['id_range_check']:
            category_config = self.config['category_specific_fields'].get(category)
            if category_config and 'id_range' in category_config:
                id_range = category_config['id_range']
                start, end = id_range.split('-')
                term_num = int(term_id.replace('TCH_', ''))
                
                if not (int(start) <= term_num <= int(end)):
                    logger.error(f"ID范围错误: {term_id} 不在 {category} 类别范围 {id_range} 内")
                    return False
        
        return True
    
    def validate_required_fields(self, row: pd.Series, category: str) -> bool:
        """
        验证必填字段
        
        Args:
            row: 数据行
            category: 术语类别
            
        Returns:
            验证是否通过
        """
        # 检查通用必填字段
        for field_name, field_config in self.config['common_fields'].items():
            if field_config.get('required', False):
                if field_name not in row or pd.isna(row[field_name]) or str(row[field_name]).strip() == '':
                    logger.error(f"必填字段缺失: {field_name}")
                    return False
        
        # 检查类别特定必填字段
        category_config = self.config['category_specific_fields'].get(category, {})
        for field_name, field_config in category_config.items():
            # 跳过非字段配置（如 base_class, id_range 等元数据）
            if not isinstance(field_config, dict) or 'property' not in field_config:
                continue
            if field_config.get('required', False):
                if field_name not in row or pd.isna(row[field_name]) or str(row[field_name]).strip() == '':
                    logger.error(f"必填字段缺失: {field_name} (类别: {category})")
                    return False
        
        return True
    
    def parse_field_value(self, value: Any, field_config: Dict) -> Any:
        """
        解析字段值
        
        Args:
            value: 原始值
            field_config: 字段配置
            
        Returns:
            解析后的值
        """
        if pd.isna(value) or str(value).strip() == '':
            return None
        
        value = str(value).strip()
        field_type = field_config.get('type', 'string')
        
        # 字符串列表
        if field_type == 'string_list':
            separator = field_config.get('separator', '|')
            values = [v.strip() for v in value.split(separator) if v.strip()]
            return values if values else None
        
        # ID列表
        elif field_type == 'id_list':
            separator = field_config.get('separator', '|')
            ids = [v.strip() for v in value.split(separator) if v.strip()]
            # 添加前缀（如果需要）
            prefix = field_config.get('prefix', '')
            if prefix and not prefix.startswith('TCH'):
                ids = [f"{prefix}{id_val}" if not id_val.startswith(prefix) else id_val for id_val in ids]
            return ids if ids else None
        
        # 日期
        elif field_type == 'date':
            try:
                date_format = field_config.get('format', '%Y-%m-%d')
                return datetime.strptime(value, date_format).strftime('%Y-%m-%d')
            except:
                logger.warning(f"日期格式解析失败: {value}")
                return value
        
        # ID
        elif field_type == 'id':
            return value
        
        # 字符串
        else:
            prefix = field_config.get('prefix', '')
            if prefix and not value.startswith(prefix):
                return f"{prefix}{value}"
            return value
    
    def create_term(self, row: pd.Series, category: str) -> bool:
        """
        创建术语
        
        Args:
            row: 术语数据行
            category: 术语类别
            
        Returns:
            是否创建成功
        """
        try:
            term_id = row['tch_id']
            
            # 验证ID
            if not self.validate_term_id(term_id, category):
                return False
            
            # 验证必填字段
            if not self.validate_required_fields(row, category):
                return False
            
            # 检查术语是否已存在
            term_iri = f"{self.config['general']['term_prefix']}{term_id.replace('TCH_', '')}"
            existing_term = self.ontology.search_one(iri=term_iri)
            
            if existing_term:
                logger.warning(f"术语已存在，跳过: {term_id}")
                self.stats['skipped'] += 1
                return True
            
            # 获取基类
            category_config = self.config['category_specific_fields'].get(category, {})
            base_class_id = category_config.get('base_class', 'TCH:0000000')
            base_class_iri = base_class_id.replace('TCH:', self.config['general']['term_prefix'])
            base_class = self.ontology.search_one(iri=base_class_iri)
            
            if not base_class:
                logger.error(f"基类不存在: {base_class_id}")
                return False
            
            # 创建新类（使用 owlready2 的正确方式）
            with self.ontology:
                # 创建类名（移除 TCH_ 前缀）
                class_name = term_id.replace('_', '')
                
                # 动态创建类
                NewClass = type(class_name, (base_class,), {"namespace": self.ontology})
                
                # 设置 IRI
                NewClass.iri = term_iri
                
                # 添加标签和定义
                self._add_annotations(NewClass, row, category)
                
                # 添加关系
                self._add_relationships(NewClass, row, category)
            
            logger.info(f"术语创建成功: {term_id}")
            self.stats['success'] += 1
            return True
            
        except Exception as e:
            logger.error(f"术语创建失败: {row.get('tch_id', 'UNKNOWN')} - {e}")
            self.stats['errors'].append({
                'term_id': row.get('tch_id', 'UNKNOWN'),
                'error': str(e)
            })
            self.stats['failed'] += 1
            return False
    
    def _add_annotations(self, owl_class, row: pd.Series, category: str):
        """添加注释属性"""
        # 处理通用字段
        for field_name, field_config in self.config['common_fields'].items():
            if field_name in row and not pd.isna(row[field_name]):
                value = self.parse_field_value(row[field_name], field_config)
                if value is None:
                    continue
                
                property_name = field_config['property']
                lang = field_config.get('lang')
                
                # 根据属性类型添加
                if property_name == 'rdfs:label':
                    if lang:
                        owl_class.label.append(locstr(value, lang=lang))
                    else:
                        owl_class.label.append(value)
                
                elif property_name == 'IAO:0000115':  # definition
                    # 需要使用定义属性
                    # 这里简化处理，实际需要根据IAO本体添加
                    if lang:
                        owl_class.comment.append(locstr(f"Definition: {value}", lang=lang))
                    else:
                        owl_class.comment.append(f"Definition: {value}")
                
                elif property_name == 'rdfs:comment':
                    if lang:
                        owl_class.comment.append(locstr(value, lang=lang))
                    else:
                        owl_class.comment.append(value)
    
    def _add_relationships(self, owl_class, row: pd.Series, category: str):
        """添加关系属性"""
        category_config = self.config['category_specific_fields'].get(category, {})
        
        for field_name, field_config in category_config.items():
            # 跳过非字段配置（如 base_class, id_range 等元数据）
            if not isinstance(field_config, dict) or 'property' not in field_config:
                continue
                
            if field_name in row and not pd.isna(row[field_name]):
                value = self.parse_field_value(row[field_name], field_config)
                if value is None:
                    continue
                
                property_name = field_config['property']
                
                # 处理父类关系
                if property_name == 'rdfs:subClassOf' and isinstance(value, list):
                    for parent_id in value:
                        parent_iri = f"{self.config['general']['term_prefix']}{parent_id.replace('TCH_', '')}"
                        parent_class = self.ontology.search_one(iri=parent_iri)
                        if parent_class:
                            owl_class.is_a.append(parent_class)
                
                # 其他对象属性关系（简化处理）
                # 实际实现需要根据具体的OWL属性类型处理
    
    def import_terms(self, file_path: str, category: str, validate_only: bool = False):
        """
        导入术语
        
        Args:
            file_path: 术语数据文件路径
            category: 术语类别
            validate_only: 仅验证不导入
        """
        logger.info(f"开始导入术语 - 类别: {category}, 文件: {file_path}")
        
        # 加载数据
        df = self.load_terms_data(file_path)
        self.stats['total'] = len(df)
        
        # 加载本体
        if not validate_only:
            self.load_ontology()
        
        # 逐行处理
        for row_num, (idx, row) in enumerate(df.iterrows(), 1):
            logger.info(f"处理第 {row_num}/{len(df)} 条术语: {row.get('tch_id', 'UNKNOWN')}")
            
            if validate_only:
                # 仅验证
                valid_id = self.validate_term_id(row['tch_id'], category)
                valid_fields = self.validate_required_fields(row, category)
                if valid_id and valid_fields:
                    self.stats['success'] += 1
                else:
                    self.stats['failed'] += 1
            else:
                # 创建术语
                self.create_term(row, category)
        
        # 保存本体
        if not validate_only:
            try:
                self.ontology.save(file=str(self.ontology_path))
                logger.info(f"本体文件保存成功: {self.ontology_path}")
            except Exception as e:
                logger.error(f"本体文件保存失败: {e}")
        
        # 生成报告
        self._generate_report(category, file_path, validate_only)
    
    def _generate_report(self, category: str, file_path: str, validate_only: bool):
        """生成导入报告"""
        report = f"""
{'='*80}
TCH 本体术语导入报告
{'='*80}

导入时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
术语类别: {category}
数据文件: {file_path}
操作模式: {'仅验证' if validate_only else '导入'}

统计信息:
-----------
总计: {self.stats['total']}
成功: {self.stats['success']}
失败: {self.stats['failed']}
跳过: {self.stats['skipped']}

"""
        
        if self.stats['errors']:
            report += "\n错误详情:\n-----------\n"
            for error in self.stats['errors'][:10]:  # 只显示前10个错误
                report += f"- {error['term_id']}: {error['error']}\n"
            
            if len(self.stats['errors']) > 10:
                report += f"\n... 还有 {len(self.stats['errors']) - 10} 个错误\n"
        
        report += f"\n{'='*80}\n"
        
        print(report)
        
        # 保存报告到文件
        if self.config['import_options']['generate_report']:
            report_file = f"term_import_report_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"导入报告已保存: {report_file}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='TCH 本体术语导入工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 导入Pattern类术语
  python import_terms.py --category pattern --input data/pattern_terms.csv
  
  # 仅验证Herb类术语
  python import_terms.py --category herb --input data/herb_terms.xlsx --validate-only
  
  # 使用自定义配置文件
  python import_terms.py --category disease --input data/disease.csv --config my-config.yaml
        """
    )
    
    parser.add_argument(
        '--category',
        required=True,
        choices=[
            'pattern', 'disease', 'symptom', 'sign', 'herb', 'formula',
            'principle', 'method', 'differentiation', 'pathomechanism'
        ],
        help='术语类别'
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='输入文件路径 (CSV或Excel)'
    )
    
    parser.add_argument(
        '--config',
        default='term-import-config.yaml',
        help='配置文件路径 (默认: term-import-config.yaml)'
    )
    
    parser.add_argument(
        '--ontology',
        default='tch-edit.owl',
        help='本体文件路径 (默认: tch-edit.owl)'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='仅验证数据，不导入到本体'
    )
    
    args = parser.parse_args()
    
    # 创建导入器
    importer = TCHTermImporter(
        config_path=args.config,
        ontology_path=args.ontology
    )
    
    # 执行导入
    importer.import_terms(
        file_path=args.input,
        category=args.category,
        validate_only=args.validate_only
    )


if __name__ == '__main__':
    main()
