# MySQL数据库中的who数据库里的数据有一些问题，需要处理
# 问题：该数据库目前有三个表，但是这三个表其中还有很多不同类别的数据混在一起，需要将不同的类别的数据分离出来，存储到不同的表中
# 其中，"二、诊断、病证和体质术语"表数据有误，先不做处理
# "一、中医基础理论术语"、"三、治则、治法与疗法"表数据需要处理，分离出不同类别的数据，存储到不同的表中，不同类别的数据区分方法如下：数据中会有仅有某些字段有值，其他字段为空的行，如"chinese_term"列为"1.1 阴阳类"和"1.2 五行类"之间的数据为1.1 阴阳类的数据，其他类似。
# 本脚本处理"一、中医基础理论术语"、"三、治则、治法与疗法"表数据，分离出不同类别的数据，存储到MySQL的who数据库中（新增表，结构与原始表一致，但是如"1.1 阴阳类"就作为表名而不是数据）

import pymysql
import re
from typing import List, Dict, Tuple

# MySQL连接配置
SQL_CONFIG = {
    'host': 'eggabc.site',
    'port': 19104,
    'user': 'tcm',
    'password': 'tcm@123',
    'database': 'who',
}

# 需要处理的表名
TABLES_TO_PROCESS = [
    "一、中医基础理论术语",
    "三、治则、治法与疗法"
]


def get_connection():
    """获取MySQL数据库连接"""
    return pymysql.connect(
        host=SQL_CONFIG['host'],
        port=SQL_CONFIG['port'],
        user=SQL_CONFIG['user'],
        password=SQL_CONFIG['password'],
        database=SQL_CONFIG['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def get_table_structure(cursor, table_name: str) -> str:
    """获取表结构的CREATE TABLE语句"""
    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
    result = cursor.fetchone()
    return result['Create Table']


def sanitize_table_name(category_name: str) -> str:
    """
    将类别名称转换为合法的表名
    例如："1.1 阴阳类" -> "category_1_1_阴阳类"
    """
    # 移除特殊字符，保留中文、数字和字母
    sanitized = re.sub(r'[^\w\u4e00-\u9fff]', '_', category_name)
    # 移除多余的下划线
    sanitized = re.sub(r'_+', '_', sanitized)
    # 移除首尾的下划线
    sanitized = sanitized.strip('_')
    # 添加前缀以避免以数字开头
    if sanitized and sanitized[0].isdigit():
        sanitized = f"category_{sanitized}"
    return sanitized


def is_category_row(row: Dict) -> bool:
    """
    判断某一行是否为类别标识行
    类别标识行的特点：
    1. chinese_term字段包含类别标识（如"1.1 阴阳类"）
    2. 缺少english_definition_description或pinyin_term字段
    """
    chinese_term = row.get('chinese_term', '') or ''
    chinese_term = chinese_term.strip() if chinese_term else ''
    
    # 检查是否符合类别标识的模式：数字.数字 + 中文
    import re
    is_category_pattern = bool(re.match(r'^\d+\.\d+\s*[\u4e00-\u9fff]+', chinese_term))
    
    # 或者检查是否缺少关键字段（正常数据行通常有这些字段）
    has_definition = row.get('english_definition_description') is not None and str(row.get('english_definition_description', '')).strip()
    has_pinyin = row.get('pinyin_term') is not None and str(row.get('pinyin_term', '')).strip()
    
    # 类别行通常符合模式且缺少定义和拼音
    return is_category_pattern and not (has_definition and has_pinyin)


def extract_categories(cursor, table_name: str) -> List[Tuple[str, int, int]]:
    """
    从表中提取所有类别及其数据范围
    返回: [(类别名, 起始行号, 结束行号), ...]
    """
    cursor.execute(f"SELECT * FROM `{table_name}`")
    rows = cursor.fetchall()
    
    categories = []
    current_category = None
    start_index = None
    
    for index, row in enumerate(rows):
        if is_category_row(row):
            # 找到新的类别标识行
            if current_category is not None:
                # 保存上一个类别的范围
                categories.append((current_category, start_index, index - 1))
            
            # 获取类别名称（通常在chinese_term字段）
            category_name = row.get('chinese_term', '') or ''
            category_name = category_name.strip() if category_name else ''
            if category_name:
                current_category = category_name
                start_index = index + 1  # 数据从下一行开始
    
    # 保存最后一个类别
    if current_category is not None and start_index is not None:
        categories.append((current_category, start_index, len(rows) - 1))
    
    return categories


def create_category_table(cursor, original_table: str, category_name: str):
    """
    为某个类别创建新表
    """
    new_table_name = sanitize_table_name(category_name)
    
    # 获取原表结构
    create_statement = get_table_structure(cursor, original_table)
    
    # 修改表名
    new_create_statement = create_statement.replace(
        f"CREATE TABLE `{original_table}`",
        f"CREATE TABLE `{new_table_name}`"
    )
    
    # 删除旧表（如果存在）
    cursor.execute(f"DROP TABLE IF EXISTS `{new_table_name}`")
    
    # 创建新表
    cursor.execute(new_create_statement)
    
    print(f"  创建表: {new_table_name}")
    return new_table_name


def copy_category_data(cursor, original_table: str, new_table: str, 
                       start_index: int, end_index: int):
    """
    将指定范围的数据从原表复制到新表
    """
    # 获取原表的所有数据
    cursor.execute(f"SELECT * FROM `{original_table}`")
    all_rows = cursor.fetchall()
    
    # 获取字段名
    if not all_rows:
        return
    
    columns = list(all_rows[0].keys())
    
    # 提取需要复制的数据
    data_to_copy = all_rows[start_index:end_index + 1]
    
    if not data_to_copy:
        print(f"    警告: 没有数据需要复制 (范围: {start_index}-{end_index})")
        return
    
    # 过滤掉类别标识行（如果有的话）
    data_to_copy = [row for row in data_to_copy if not is_category_row(row)]
    
    if not data_to_copy:
        print(f"    警告: 过滤后没有有效数据")
        return
    
    # 构建INSERT语句
    placeholders = ', '.join(['%s'] * len(columns))
    columns_str = ', '.join([f'`{col}`' for col in columns])
    insert_sql = f"INSERT INTO `{new_table}` ({columns_str}) VALUES ({placeholders})"
    
    # 批量插入数据
    for row in data_to_copy:
        values = [row[col] for col in columns]
        cursor.execute(insert_sql, values)
    
    print(f"    复制了 {len(data_to_copy)} 条数据")


def process_table(connection, table_name: str):
    """
    处理单个表，分离不同类别的数据
    """
    print(f"\n处理表: {table_name}")
    print("=" * 60)
    
    cursor = connection.cursor()
    
    try:
        # 提取所有类别
        categories = extract_categories(cursor, table_name)
        print(f"发现 {len(categories)} 个类别:")
        
        for category_name, start_idx, end_idx in categories:
            print(f"\n类别: {category_name}")
            print(f"  数据范围: 第 {start_idx + 1} 行 到 第 {end_idx + 1} 行")
            
            # 创建新表
            new_table_name = create_category_table(cursor, table_name, category_name)
            
            # 复制数据
            copy_category_data(cursor, table_name, new_table_name, start_idx, end_idx)
        
        connection.commit()
        print(f"\n表 '{table_name}' 处理完成!")
        
    except Exception as e:
        connection.rollback()
        print(f"处理表 '{table_name}' 时出错: {str(e)}")
        raise
    finally:
        cursor.close()


def main():
    """主函数"""
    print("WHO中医术语数据处理脚本")
    print("=" * 60)
    
    connection = None
    try:
        # 连接数据库
        print("连接数据库...")
        connection = get_connection()
        print("数据库连接成功!")
        
        # 处理每个表
        for table_name in TABLES_TO_PROCESS:
            process_table(connection, table_name)
        
        print("\n" + "=" * 60)
        print("所有表处理完成!")
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if connection:
            connection.close()
            print("数据库连接已关闭")


if __name__ == "__main__":
    # 添加调试模式：先查看数据结构
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--debug':
        connection = get_connection()
        cursor = connection.cursor()
        
        # 查看第一个表的数据
        table_name = "一、中医基础理论术语"
        print(f"查看表 '{table_name}' 的数据结构:\n")
        
        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 20")
        rows = cursor.fetchall()
        
        print(f"总共获取了 {len(rows)} 行数据\n")
        
        for i, row in enumerate(rows):
            print(f"第 {i+1} 行:")
            non_empty = []
            for key, value in row.items():
                if value is not None and str(value).strip():
                    non_empty.append(f"  {key}: {value}")
            print(f"  非空字段数: {len(non_empty)}")
            if non_empty:
                print('\n'.join(non_empty))
            print()
        
        cursor.close()
        connection.close()
    else:
        main()
