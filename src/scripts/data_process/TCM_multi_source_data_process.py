#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TCM多源数据处理脚本
用于从多个MySQL数据库中提取并处理中医术语数据，基于field_mapping.csv的映射关系

主要功能:
1. 读取field_mapping.csv获取字段映射关系
2. 从多个数据库(symap, herb2_0, etcm2_0)提取数据
3. 根据模板格式处理数据
4. 追加到现有的临时ID文件中，确保ID唯一性
5. 支持pattern、symptom、herb、formula四种数据类型

创建时间: 2025.11.12
版本: 1.0
"""

import pymysql
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import csv
import re


# MySQL数据库连接配置
DB_CONFIGS = {
    'symap': {
        'host': 'eggabc.site',
        'port': 19104,
        'user': 'tcm',
        'password': 'tcm@123',
        'database': 'symap',
        'charset': 'utf8mb4'
    },
    'herb2_0': {
        'host': 'eggabc.site',
        'port': 19104,
        'user': 'tcm',
        'password': 'tcm@123',
        'database': 'herb2_0',
        'charset': 'utf8mb4'
    },
    'etcm2_0': {
        'host': 'eggabc.site',
        'port': 19104,
        'user': 'tcm',
        'password': 'tcm@123',
        'database': 'etcm2_0',
        'charset': 'utf8mb4'
    }
}

# 临时ID配置
TEMP_ID_CONFIGS = {
    'pattern': {
        'prefix': 'TmpTCH:PATTERN_',
        'start_number': 10000,
        'padding': 5
    },
    'symptom': {
        'prefix': 'TmpTCH:SYMPTOM_',
        'start_number': 20000,
        'padding': 5
    },
    'herb': {
        'prefix': 'TmpTCH:HERB_',
        'start_number': 100000,
        'padding': 6
    },
    'formula': {
        'prefix': 'TmpTCH:FORMULA_',
        'start_number': 400000,
        'padding': 6
    }
}

# 文件路径
BASE_DIR = Path(__file__).parent
FIELD_MAPPING_FILE = BASE_DIR / 'field_mapping.csv'
OUTPUT_DIR = BASE_DIR.parent.parent.parent / 'data' / 'data_temp_ids'


class MultiSourceDataProcessor:
    """多源数据处理器"""
    
    def __init__(self):
        """初始化处理器"""
        self.connections = {}
        self.field_mappings = {}
        self.existing_data = {}
        self.current_temp_numbers = {}
        self.used_temp_ids = {}
        
        # 初始化每个数据类型的临时ID计数器
        for data_type in TEMP_ID_CONFIGS.keys():
            self.current_temp_numbers[data_type] = TEMP_ID_CONFIGS[data_type]['start_number']
            self.used_temp_ids[data_type] = set()
    
    def connect_db(self, db_name: str):
        """连接指定的MySQL数据库"""
        if db_name in self.connections:
            return self.connections[db_name]
        
        try:
            config = DB_CONFIGS[db_name]
            connection = pymysql.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database'],
                charset=config['charset'],
                connect_timeout=30,  # 增加连接超时
                read_timeout=300,     # 增加读取超时（5分钟）
                write_timeout=300     # 增加写入超时（5分钟）
            )
            self.connections[db_name] = connection
            print(f"✅ 连接到数据库 {db_name} 成功")
            return connection
        except Exception as e:
            print(f"❌ 连接数据库 {db_name} 失败: {e}")
            raise
    
    def close_connections(self):
        """关闭所有数据库连接"""
        for db_name, conn in self.connections.items():
            if conn:
                conn.close()
                print(f"✅ 数据库 {db_name} 连接已关闭")
    
    def load_field_mappings(self):
        """加载字段映射配置"""
        print("\n" + "="*70)
        print("📥 加载字段映射配置")
        print("="*70)
        
        try:
            df = pd.read_csv(FIELD_MAPPING_FILE)
            
            # 按data_type分组
            for data_type in df['data_type'].unique():
                type_mappings = df[df['data_type'] == data_type]
                
                # 按数据库和表分组
                db_table_groups = {}
                for _, row in type_mappings.iterrows():
                    db = row['database']
                    table = row['table']
                    key = f"{db}.{table}"
                    
                    if key not in db_table_groups:
                        db_table_groups[key] = {
                            'database': db,
                            'table': table,
                            'mappings': []
                        }
                    
                    db_table_groups[key]['mappings'].append({
                        'template_field': row['template_field'],
                        'db_field': row['db_field'],
                        'notes': row['notes'] if pd.notna(row['notes']) else ''
                    })
                
                self.field_mappings[data_type] = db_table_groups
            
            print(f"✅ 成功加载字段映射配置")
            for data_type, groups in self.field_mappings.items():
                print(f"   - {data_type}: {len(groups)} 个数据源")
            
            return True
        except Exception as e:
            print(f"❌ 加载字段映射配置失败: {e}")
            return False
    
    def load_existing_data(self, data_type: str):
        """加载现有的临时ID数据"""
        output_file = OUTPUT_DIR / f'{data_type}_data_temp_ids.csv'
        
        if output_file.exists():
            try:
                df = pd.read_csv(output_file)
                self.existing_data[data_type] = df
                
                # 收集已使用的临时ID
                for temp_id in df['tch_id']:
                    self.used_temp_ids[data_type].add(temp_id)
                    
                    # 更新当前临时ID计数器
                    if temp_id.startswith(TEMP_ID_CONFIGS[data_type]['prefix']):
                        try:
                            id_num = int(temp_id.replace(TEMP_ID_CONFIGS[data_type]['prefix'], ''))
                            if id_num >= self.current_temp_numbers[data_type]:
                                self.current_temp_numbers[data_type] = id_num + 1
                        except:
                            pass
                
                print(f"✅ 已加载现有 {data_type} 数据: {len(df)} 条记录")
                print(f"   下一个临时ID将从 {TEMP_ID_CONFIGS[data_type]['prefix']}{str(self.current_temp_numbers[data_type]).zfill(TEMP_ID_CONFIGS[data_type]['padding'])} 开始")
                return True
            except Exception as e:
                print(f"⚠️  加载现有 {data_type} 数据失败: {e}")
                return False
        else:
            print(f"ℹ️  {data_type} 数据文件不存在，将创建新文件")
            self.existing_data[data_type] = None
            return True
    
    def allocate_temp_id(self, data_type: str) -> str:
        """为指定数据类型分配新的临时ID"""
        prefix = TEMP_ID_CONFIGS[data_type]['prefix']
        padding = TEMP_ID_CONFIGS[data_type]['padding']
        
        while True:
            temp_id = f"{prefix}{str(self.current_temp_numbers[data_type]).zfill(padding)}"
            if temp_id not in self.used_temp_ids[data_type]:
                break
            self.current_temp_numbers[data_type] += 1
        
        self.used_temp_ids[data_type].add(temp_id)
        self.current_temp_numbers[data_type] += 1
        
        return temp_id
    
    def extract_field_names_from_expression(self, expression: str) -> List[str]:
        """
        从字段表达式中提取所有数据库字段名
        例如: "SymMap2.0 SMSY"+Syndrome_id -> [Syndrome_id]
        例如: Herb_id;SymMap_id;"TCMID: "+TCMID_id -> [Herb_id, SymMap_id, TCMID_id]
        """
        if not expression:
            return []
        
        field_names = []
        
        # 分割表达式（按分号或加号）
        # 首先提取所有引号包裹的部分
        quoted_parts = re.findall(r'"[^"]*"', expression)
        # 临时替换引号部分为占位符
        temp_expr = expression
        for i, quoted in enumerate(quoted_parts):
            temp_expr = temp_expr.replace(quoted, f'__QUOTED_{i}__', 1)
        
        # 分割表达式
        parts = re.split(r'[;+]', temp_expr)
        
        for part in parts:
            part = part.strip()
            # 跳过占位符（引号内容）
            if part.startswith('__QUOTED_'):
                continue
            # 跳过空字符串
            if not part:
                continue
            # 这应该是一个字段名
            field_names.append(part)
        
        return field_names
    
    def parse_composite_field(self, row: pd.Series, db_field: str) -> str:
        """
        解析复合字段表达式
        例如: Herb_id;SymMap_id;"TCMID: "+TCMID_id
        例如: "SymMap2.0 SMSY"+Syndrome_id
        """
        if not db_field:
            return ''
        
        # 检查是否包含特殊操作符
        if ';' in db_field or '+' in db_field or '"' in db_field:
            result_parts = []
            
            # 分割表达式（按分号）
            if ';' in db_field:
                segments = db_field.split(';')
            else:
                segments = [db_field]
            
            for segment in segments:
                segment = segment.strip()
                
                # 处理每个段（可能包含加号连接）
                if '+' in segment:
                    # 分割加号连接的部分
                    sub_parts = segment.split('+')
                    combined = ''
                    for sub_part in sub_parts:
                        sub_part = sub_part.strip()
                        
                        # 检查是否是引号包裹的字符串
                        if sub_part.startswith('"') and sub_part.endswith('"'):
                            # 去掉引号，添加到combined
                            combined += sub_part[1:-1]
                        else:
                            # 这是一个字段名，从row中获取值
                            value = row.get(sub_part, '')
                            if pd.notna(value) and str(value).strip():
                                combined += str(value)
                    
                    if combined:
                        result_parts.append(combined)
                else:
                    # 没有加号，直接处理
                    if segment.startswith('"') and segment.endswith('"'):
                        # 引号包裹的字符串
                        result_parts.append(segment[1:-1])
                    else:
                        # 普通字段名
                        value = row.get(segment, '')
                        if pd.notna(value) and str(value).strip():
                            result_parts.append(str(value))
            
            # 用分号连接所有部分
            return ';'.join(result_parts) if result_parts else ''
        else:
            # 简单字段，直接获取值
            value = row.get(db_field, '')
            return str(value) if pd.notna(value) and str(value).strip() else ''
    
    def extract_data_from_source(self, data_type: str, db_name: str, table: str, mappings: List[Dict]) -> List[Dict]:
        """从指定数据源提取数据（使用分批查询避免超时）"""
        print(f"\n📥 从 {db_name}.{table} 提取 {data_type} 数据")
        
        try:
            connection = self.connect_db(db_name)
            
            # 构建需要查询的字段列表
            db_fields = set()
            for mapping in mappings:
                db_field = mapping['db_field']
                # 使用helper方法提取字段名
                field_names = self.extract_field_names_from_expression(db_field)
                db_fields.update(field_names)
            
            # 构建SQL查询 - 用反引号包裹字段名以避免保留字冲突
            fields_str = ', '.join(f'`{field}`' for field in db_fields)
            
            # 分批查询，每次最多2000条记录（减小批量以避免超时）
            batch_size = 2000
            offset = 0
            all_rows = []
            
            while True:
                query = f"SELECT {fields_str} FROM {table} LIMIT {batch_size} OFFSET {offset}"
                
                try:
                    # 执行查询
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                        rows = cursor.fetchall()
                        
                        if not rows:
                            break
                        
                        all_rows.extend(rows)
                        offset += batch_size
                        print(f"   已提取 {len(all_rows)} 条记录...")
                        
                        # 如果返回的记录少于batch_size，说明已经是最后一批
                        if len(rows) < batch_size:
                            break
                            
                except pymysql.err.OperationalError as e:
                    if '2013' in str(e):  # Lost connection
                        print(f"   ⚠️  连接断开，尝试重新连接...")
                        # 关闭旧连接
                        if db_name in self.connections:
                            try:
                                self.connections[db_name].close()
                            except:
                                pass
                            del self.connections[db_name]
                        
                        # 重新连接
                        connection = self.connect_db(db_name)
                        
                        # 重试当前批次
                        with connection.cursor() as cursor:
                            cursor.execute(query)
                            rows = cursor.fetchall()
                            
                            if not rows:
                                break
                            
                            all_rows.extend(rows)
                            offset += batch_size
                            print(f"   已提取 {len(all_rows)} 条记录（重连后继续）...")
                            
                            if len(rows) < batch_size:
                                break
                    else:
                        raise
            
            # 构建DataFrame
            df = pd.DataFrame(all_rows, columns=list(db_fields))
            
            print(f"✅ 成功提取 {len(df)} 条原始数据")
            
            # 转换为模板格式
            processed_records = []
            for idx, row in df.iterrows():
                record = {
                    'tch_id': self.allocate_temp_id(data_type),
                    'data_category': data_type
                }
                
                # 根据映射填充字段
                for mapping in mappings:
                    template_field = mapping['template_field']
                    db_field = mapping['db_field']
                    
                    # 解析字段值
                    value = self.parse_composite_field(row, db_field)
                    record[template_field] = value
                
                # 添加标准字段
                if 'date_accessed' not in record:
                    record['date_accessed'] = datetime.now().strftime('%Y-%m-%d')
                
                if 'notes' not in record:
                    record['notes'] = f'Source: {db_name}.{table}'
                else:
                    record['notes'] += f'; Source: {db_name}.{table}'
                
                processed_records.append(record)
            
            print(f"✅ 成功处理 {len(processed_records)} 条记录")
            return processed_records
                
        except Exception as e:
            print(f"❌ 从 {db_name}.{table} 提取数据失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def process_data_type(self, data_type: str):
        """处理指定数据类型的所有数据源"""
        print("\n" + "="*70)
        print(f"🔄 开始处理 {data_type.upper()} 数据")
        print("="*70)
        
        # 加载现有数据
        self.load_existing_data(data_type)
        
        # 获取该数据类型的所有数据源
        if data_type not in self.field_mappings:
            print(f"⚠️  未找到 {data_type} 的字段映射配置")
            return
        
        all_new_records = []
        
        # 从每个数据源提取数据
        for source_key, source_info in self.field_mappings[data_type].items():
            db_name = source_info['database']
            table = source_info['table']
            mappings = source_info['mappings']
            
            records = self.extract_data_from_source(data_type, db_name, table, mappings)
            all_new_records.extend(records)
        
        if not all_new_records:
            print(f"⚠️  未提取到新的 {data_type} 数据")
            return
        
        # 合并新旧数据
        new_df = pd.DataFrame(all_new_records)
        
        if self.existing_data[data_type] is not None:
            # 追加到现有数据
            combined_df = pd.concat([self.existing_data[data_type], new_df], ignore_index=True)
            print(f"✅ 追加 {len(new_df)} 条新记录到现有 {len(self.existing_data[data_type])} 条记录")
        else:
            combined_df = new_df
            print(f"✅ 创建新文件，包含 {len(combined_df)} 条记录")
        
        # 保存数据
        output_file = OUTPUT_DIR / f'{data_type}_data_temp_ids.csv'
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        combined_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"💾 数据已保存到: {output_file}")
        print(f"   总记录数: {len(combined_df)}")
        print(f"   新增记录数: {len(new_df)}")
        print(f"   文件大小: {output_file.stat().st_size / 1024:.2f} KB")
    
    def process_all_data_types(self, data_types: List[str] = None):
        """处理所有或指定的数据类型"""
        if data_types is None:
            data_types = ['pattern', 'symptom', 'herb', 'formula']
        
        print("="*70)
        print("TCM多源数据处理程序".center(70))
        print("="*70)
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"处理数据类型: {', '.join(data_types)}")
        
        try:
            # 加载字段映射
            if not self.load_field_mappings():
                return
            
            # 处理每个数据类型
            for data_type in data_types:
                self.process_data_type(data_type)
            
            print("\n" + "="*70)
            print("✅ 所有数据处理完成!".center(70))
            print("="*70)
            print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"\n❌ 处理过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.close_connections()


def main():
    """主函数"""
    import sys
    
    processor = MultiSourceDataProcessor()
    
    # 支持命令行参数指定数据类型
    if len(sys.argv) > 1:
        data_types = sys.argv[1:]
        processor.process_all_data_types(data_types)
    else:
        # 默认处理所有数据类型
        processor.process_all_data_types()


if __name__ == '__main__':
    main()
