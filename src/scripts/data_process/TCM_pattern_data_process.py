#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TCM证候(Pattern)数据处理脚本 - 临时ID版本
用于从MySQL数据库中提取并处理中医证候术语数据，生成符合pattern_template.csv格式的标准化文件

主要功能:
1. 从MySQL数据库提取证候数据
2. 使用临时ID系统(TmpTCH:PATTERN_XXXXX)进行ID分配
3. 处理术语的层级关系
4. 验证层级完整性和循环引用
5. 生成ID映射指南文档

数据来源:
- 数据库: clinical_diagnosis_and_treatment.clinical_syndrome
- 标准: 中医临床诊疗术语第2部分:证候(GB/T 16751.2—2021)

创建时间: 2025.11.9
版本: 2.0 (临时ID版)
"""

import pymysql
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re


# MySQL连接配置
SQL_CONFIG = {
    'host': 'eggabc.site',
    'port': 19104,
    'user': 'tcm',
    'password': 'tcm@123',
    'database': 'clinical_diagnosis_and_treatment',
    'charset': 'utf8mb4'
}

# 临时ID配置
TEMP_ID_CONFIG = {
    'prefix': 'TmpTCH:PATTERN_',  # 临时ID前缀
    'start_number': 10000,         # 起始编号(确保唯一性)
    'padding': 5                   # 编号位数
}

# 输出文件路径
OUTPUT_DIR = Path(__file__).parent.parent.parent.parent / 'data' / 'data_temp_ids'
OUTPUT_FILE = OUTPUT_DIR / 'pattern_data_temp_ids.csv'
MAPPING_GUIDE_FILE = OUTPUT_DIR / 'pattern_temp_id_mapping_guide.md'


class TCMPatternDataProcessor:
    """证候数据处理器 - 临时ID版本"""
    
    def __init__(self, config: Dict):
        """初始化处理器"""
        self.config = config
        self.connection = None
        self.raw_data = None
        self.processed_data = []
        self.code_to_temp_id = {}     # code -> 临时ID 映射
        self.temp_id_to_code = {}     # 临时ID -> code 映射
        self.used_temp_ids = set()    # 已使用的临时ID集合
        self.current_temp_number = TEMP_ID_CONFIG['start_number']
        
    def connect_db(self):
        """连接MySQL数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config['charset']
            )
            print("✅ 数据库连接成功")
            print(f"   连接到: {self.config['host']}:{self.config['port']}/{self.config['database']}")
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            raise
    
    def close_connection(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("✅ 数据库连接已关闭")
    
    def fetch_data(self) -> bool:
        """从数据库提取数据"""
        print("\n" + "="*70)
        print("📥 从数据库提取数据")
        print("="*70)
        
        query = """
            SELECT
                id,
                code,
                term_cn,
                term_synonym,
                term_en,
                definition,
                source_file,
                upload_time
            FROM clinical_syndrome
            ORDER BY code
        """
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                
                # 手动构建DataFrame
                columns = ['id', 'code', 'term_cn', 'term_synonym', 'term_en', 
                          'definition', 'source_file', 'upload_time']
                self.raw_data = pd.DataFrame(rows, columns=columns)
                
                # 过滤掉列名行
                self.raw_data = self.raw_data[
                    (self.raw_data['term_cn'] != 'term_cn') & 
                    (self.raw_data['term_cn'].notna())
                ]
                
                print(f"✅ 成功提取 {len(self.raw_data)} 条原始数据")
                print(f"   数据字段: {', '.join(columns)}")
                return True
                
        except Exception as e:
            print(f"❌ 数据提取失败: {e}")
            return False
    
    def allocate_temp_id(self, code: str) -> str:
        """分配临时ID"""
        if code in self.code_to_temp_id:
            return self.code_to_temp_id[code]
        
        # 生成新的临时ID
        prefix = TEMP_ID_CONFIG['prefix']
        padding = TEMP_ID_CONFIG['padding']
        
        while True:
            temp_id = f"{prefix}{str(self.current_temp_number).zfill(padding)}"
            if temp_id not in self.used_temp_ids:
                break
            self.current_temp_number += 1
        
        # 记录映射关系
        self.code_to_temp_id[code] = temp_id
        self.temp_id_to_code[temp_id] = code
        self.used_temp_ids.add(temp_id)
        self.current_temp_number += 1
        
        return temp_id
    
    def get_parent_code(self, code: str) -> Optional[str]:
        """获取父级code
        
        层级关系规则:
        - 2.3.2.1 的父级是 2.3.2
        - 2.3.2 的父级是 2.3
        - 2.3 的父级是 2
        - 2 的父级是 ROOT(顶层类别)
        - ROOT 无父级
        """
        if not code or code == 'ROOT':
            return None
        
        # 拆分code
        parts = code.split('.')
        
        if len(parts) == 1:
            # 单级code(如 "2"),父级是ROOT
            return 'ROOT'
        else:
            # 多级code,去掉最后一级
            return '.'.join(parts[:-1])
    
    def get_parent_temp_id(self, code: str) -> str:
        """获取父级的临时ID"""
        parent_code = self.get_parent_code(code)
        
        if parent_code is None:
            return ''  # 顶层无父级
        
        if parent_code == 'ROOT':
            # ROOT类别的临时ID
            if 'ROOT' not in self.code_to_temp_id:
                self.allocate_temp_id('ROOT')
            return self.code_to_temp_id['ROOT']
        
        # 确保父级已分配临时ID
        if parent_code not in self.code_to_temp_id:
            # 如果父级不在原始数据中,创建占位符
            if parent_code not in self.raw_data['code'].values:
                self.allocate_temp_id(parent_code)
        
        return self.code_to_temp_id.get(parent_code, '')
    
    def process_data(self):
        """处理数据"""
        print("\n" + "="*70)
        print("🔄 开始数据处理")
        print("="*70)
        
        # 先为ROOT分配临时ID
        root_temp_id = self.allocate_temp_id('ROOT')
        print(f"📌 ROOT类别临时ID: {root_temp_id}")
        
        # 收集所有需要的父级code
        all_parent_codes = set()
        for code in self.raw_data['code']:
            parent_code = self.get_parent_code(code)
            while parent_code and parent_code != 'ROOT':
                all_parent_codes.add(parent_code)
                parent_code = self.get_parent_code(parent_code)
        
        # 为所有code(包括占位符)分配临时ID
        for code in sorted(all_parent_codes):
            if code not in self.code_to_temp_id:
                self.allocate_temp_id(code)
        
        for code in self.raw_data['code']:
            if code not in self.code_to_temp_id:
                self.allocate_temp_id(code)
        
        print(f"✅ 已分配 {len(self.code_to_temp_id)} 个临时ID")
        
        # 先添加ROOT节点
        root_data = {
            'tch_id': root_temp_id,
            'data_category': 'pattern',
            'label_zh': '证候',
            'label_en': 'Pattern',
            'definition_zh': '中医证候根类别，包含所有证候术语',
            'definition_en': 'Root category for all TCM pattern terms',
            'has_synonym_zh': '',
            'has_synonym_en': '',
            'parents': '',
            'has_sign': '',
            'has_symptom': '',
            'reflected_by_pathomechanism': '',
            'treated_by_principle': '',
            'diagnosed_by_differentiation': '',
            'associated_disease': '',
            'xrefs': '',
            'sources': 'GB/T 16751.2-2021',
            'date_accessed': datetime.now().strftime('%Y-%m-%d'),
            'notes': 'ROOT category for Pattern hierarchy; Database: clinical_syndrome'
        }
        self.processed_data.append(root_data)
        
        # 处理每条记录
        for idx, row in self.raw_data.iterrows():
            code = row['code']
            temp_id = self.code_to_temp_id[code]
            parent_temp_id = self.get_parent_temp_id(code)
            
            # 构建processed_data条目
            term_data = {
                'tch_id': temp_id,
                'data_category': 'pattern',
                'label_zh': row['term_cn'] if pd.notna(row['term_cn']) else '',
                'label_en': row['term_en'] if pd.notna(row['term_en']) else '',
                'definition_zh': row['definition'] if pd.notna(row['definition']) else '',
                'definition_en': '',
                'has_synonym_zh': row['term_synonym'] if pd.notna(row['term_synonym']) else '',
                'has_synonym_en': '',
                'parents': parent_temp_id,
                'has_sign': '',
                'has_symptom': '',
                'reflected_by_pathomechanism': '',
                'treated_by_principle': '',
                'diagnosed_by_differentiation': '',
                'associated_disease': '',
                'xrefs': '',
                'sources': row['source_file'] if pd.notna(row['source_file']) else 'GB/T 16751.2-2021',
                'date_accessed': datetime.now().strftime('%Y-%m-%d'),
                'notes': f'Original code: {code}; Database: clinical_syndrome'
            }
            
            self.processed_data.append(term_data)
        
        print(f"✅ 成功处理 {len(self.processed_data)} 条数据(包含ROOT节点)")
    
    def validate_hierarchy(self) -> Tuple[bool, List[str]]:
        """验证层级关系完整性"""
        print("\n" + "="*70)
        print("🔍 验证层级关系")
        print("="*70)
        
        issues = []
        
        # 检查孤儿节点
        all_temp_ids = set(item['tch_id'] for item in self.processed_data)
        for item in self.processed_data:
            parent_id = item['parents']
            if parent_id and parent_id not in all_temp_ids:
                issues.append(f"孤儿节点: {item['tch_id']} ({item['label_zh']}) 的父级 {parent_id} 不存在")
        
        # 检查循环引用
        def has_cycle(temp_id, visited=None):
            if visited is None:
                visited = set()
            
            if temp_id in visited:
                return True
            
            visited.add(temp_id)
            
            # 查找parent
            for item in self.processed_data:
                if item['tch_id'] == temp_id:
                    parent_id = item['parents']
                    if parent_id:
                        if has_cycle(parent_id, visited.copy()):
                            return True
                    break
            
            return False
        
        for item in self.processed_data:
            if has_cycle(item['tch_id']):
                issues.append(f"循环引用: {item['tch_id']} ({item['label_zh']})")
        
        if issues:
            print(f"❌ 发现 {len(issues)} 个层级问题:")
            for issue in issues[:10]:  # 只显示前10个
                print(f"   - {issue}")
            return False, issues
        else:
            print("✅ 层级关系验证通过")
            return True, []
    
    def generate_id_mapping_guide(self):
        """生成临时ID映射指南"""
        print("\n" + "="*70)
        print("📄 生成ID映射指南")
        print("="*70)
        
        guide_content = f"""# Pattern临时ID映射指南

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**数据来源**: clinical_diagnosis_and_treatment.clinical_syndrome
**临时ID范围**: {TEMP_ID_CONFIG['prefix']}{str(TEMP_ID_CONFIG['start_number']).zfill(TEMP_ID_CONFIG['padding'])} - {TEMP_ID_CONFIG['prefix']}{str(self.current_temp_number-1).zfill(TEMP_ID_CONFIG['padding'])}
**总术语数**: {len(self.code_to_temp_id)}

## 1. 映射关系概览

| 临时ID | 原始Code | 中文术语 | 父级临时ID |
|--------|----------|----------|------------|
"""
        
        # 按code排序
        sorted_codes = sorted(self.code_to_temp_id.keys())
        
        for code in sorted_codes:
            temp_id = self.code_to_temp_id[code]
            parent_temp_id = self.get_parent_temp_id(code) if code != 'ROOT' else ''
            
            # 查找中文术语
            label_zh = ''
            for item in self.processed_data:
                if item['tch_id'] == temp_id:
                    label_zh = item['label_zh']
                    break
            
            if code == 'ROOT':
                label_zh = '证候(根类别)'
            
            guide_content += f"| {temp_id} | {code} | {label_zh} | {parent_temp_id} |\n"
        
        guide_content += f"""

## 2. 层级结构示例

以下是几个典型的层级关系示例:

"""
        # 选择几个示例展示层级
        example_codes = ['2', '2.3', '2.3.2', '2.3.2.1']
        for code in example_codes:
            if code in self.code_to_temp_id:
                temp_id = self.code_to_temp_id[code]
                parent_temp_id = self.get_parent_temp_id(code)
                
                # 查找中文术语
                label_zh = ''
                for item in self.processed_data:
                    if item['tch_id'] == temp_id:
                        label_zh = item['label_zh']
                        break
                
                guide_content += f"- **{code}** → {temp_id} ({label_zh})\n"
                if parent_temp_id:
                    guide_content += f"  - 父级: {parent_temp_id}\n"
        
        guide_content += """

## 3. 后续处理步骤

### 3.1 人工审核阶段
1. 审核 `pattern_data_temp_ids.csv` 文件中的术语
2. 删除不需要的术语行
3. 修正术语信息(如有需要)

### 3.2 最终ID分配阶段
1. 确定保留的术语列表
2. 按照TCH ID分配策略分配正式ID(TCH:0001000-0099999)
3. 更新parents字段为正式ID
4. 生成最终的pattern_data_processed.csv

### 3.3 ID重分配脚本
可以使用以下脚本将临时ID替换为正式ID:

```python
# 示例:ID重分配脚本框架
def reassign_final_ids(temp_csv_path, id_range_start=1000):
    df = pd.read_csv(temp_csv_path)
    
    # 建立临时ID到最终ID的映射
    temp_to_final = {{}}
    current_id = id_range_start
    
    for temp_id in df['tch_id']:
        if temp_id not in temp_to_final:
            temp_to_final[temp_id] = f"TCH:{{str(current_id).zfill(7)}}"
            current_id += 1
    
    # 替换ID
    df['tch_id'] = df['tch_id'].map(temp_to_final)
    df['parents'] = df['parents'].apply(
        lambda x: temp_to_final.get(x, '') if x else ''
    )
    
    return df
```

## 4. 注意事项

⚠️ **重要提醒**:
- 临时ID仅用于审核阶段,不应用于生产环境
- 删除术语时注意检查是否有子术语依赖
- 最终ID分配时需保持层级关系的一致性
- 建议在ID重分配前备份数据

---
*本文档由 TCM_pattern_data_process.py 自动生成*
"""
        
        # 保存指南
        MAPPING_GUIDE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MAPPING_GUIDE_FILE, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"✅ ID映射指南已保存: {MAPPING_GUIDE_FILE}")
    
    def save_data(self):
        """保存处理后的数据"""
        print("\n" + "="*70)
        print("💾 保存处理结果")
        print("="*70)
        
        # 转换为DataFrame
        df = pd.DataFrame(self.processed_data)
        
        # 确保输出目录存在
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # 保存CSV
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        
        print(f"✅ 数据已保存到: {OUTPUT_FILE}")
        print(f"   记录数: {len(df)}")
        print(f"   文件大小: {OUTPUT_FILE.stat().st_size / 1024:.2f} KB")
        
        # 显示统计信息
        self.print_statistics(df)
    
    def print_statistics(self, df: pd.DataFrame):
        """打印统计信息"""
        print("\n" + "="*70)
        print("📊 数据统计")
        print("="*70)
        
        # 基本统计
        print(f"总术语数: {len(df)}")
        print(f"临时ID范围: {df['tch_id'].min()} - {df['tch_id'].max()}")
        
        # 字段完整性
        print("\n字段完整性:")
        print(f"  - 中文名称: {df['label_zh'].notna().sum()} ({df['label_zh'].notna().sum()/len(df)*100:.1f}%)")
        print(f"  - 英文名称: {df['label_en'].notna().sum()} ({df['label_en'].notna().sum()/len(df)*100:.1f}%)")
        print(f"  - 中文定义: {df['definition_zh'].notna().sum()} ({df['definition_zh'].notna().sum()/len(df)*100:.1f}%)")
        print(f"  - 中文同义词: {(df['has_synonym_zh'].notna() & (df['has_synonym_zh'] != '')).sum()} ({(df['has_synonym_zh'].notna() & (df['has_synonym_zh'] != '')).sum()/len(df)*100:.1f}%)")
        
        # 层级统计
        root_children = df[df['parents'] == self.code_to_temp_id.get('ROOT', '')]['tch_id'].tolist()
        print(f"\n层级关系:")
        print(f"  - 顶级类别数: {len(root_children)}")
        
        # 计算最大层级深度
        def get_depth(temp_id, depth=0):
            parent = df[df['tch_id'] == temp_id]['parents'].values
            if len(parent) == 0 or not parent[0]:
                return depth
            return get_depth(parent[0], depth + 1)
        
        max_depth = max(get_depth(tid) for tid in df['tch_id'])
        print(f"  - 最大层级深度: {max_depth}")
        
        print("\n" + "="*70)


def main():
    """主函数"""
    print("="*70)
    print("TCM证候数据处理程序 - 临时ID版本".center(70))
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    processor = TCMPatternDataProcessor(SQL_CONFIG)
    
    try:
        # 1. 连接数据库
        processor.connect_db()
        
        # 2. 提取数据
        if not processor.fetch_data():
            return
        
        # 3. 处理数据
        processor.process_data()
        
        # 4. 验证层级关系
        valid, issues = processor.validate_hierarchy()
        if not valid:
            print("\n⚠️ 警告: 发现层级关系问题,但继续处理...")
        
        # 5. 生成ID映射指南
        processor.generate_id_mapping_guide()
        
        # 6. 保存数据
        processor.save_data()
        
        print("\n" + "="*70)
        print("✅ 处理完成!".center(70))
        print("="*70)
        print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n输出文件:")
        print(f"  - 数据文件: {OUTPUT_FILE}")
        print(f"  - 映射指南: {MAPPING_GUIDE_FILE}")
        
    except Exception as e:
        print(f"\n❌ 处理过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        processor.close_connection()


if __name__ == '__main__':
    main()
