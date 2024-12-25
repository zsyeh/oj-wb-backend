import sqlite3

def query_student_by_id(db_name, table_name, username):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 查询指定学号的学生信息
    query = f"SELECT * FROM {table_name} WHERE username = ?"
    cursor.execute(query, (username,))
    
    # 获取查询结果
    record = cursor.fetchone()
    
    # 获取表的列名
    column_names = [description[0] for description in cursor.description]
    
    # 打印结果
    if record:
        print(f"Student ID: {username}")
        for col_name, value in zip(column_names, record):
            print(f"{col_name}: {value}")
    else:
        print(f"No record found for username: {username}")
    
    # 关闭连接
    conn.close()

# 调用查询函数
username_to_query = '22110403011'  # 替换为你要查询的学号
query_student_by_id('students.db', 'students', username_to_query)


def list_all_primary_keys(db_name):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 查询所有表的名称
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    # 遍历每个表并查询主键
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # 查找主键列
        primary_keys = [col[1] for col in columns if col[5] == 1]
        
        # 打印表名和主键
        print(f"Table: {table_name}")
        print(f"Primary Keys: {', '.join(primary_keys)}")
        print()
    
    # 关闭连接
    conn.close()

# 调用查询函数
list_all_primary_keys('students.db')