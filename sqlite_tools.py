import sqlite3
import os
def list_tables(db_name):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 查询所有表的名称
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    # 打印表名
    print("Tables in the database:")
    for table in tables:
        print(table[0])
    
    # 关闭连接
    conn.close()

# 打印指定数据表里的所有数据
def print_table(db_name, table_name):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 查询表中的所有记录
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    records = cursor.fetchall()
    
    # 获取表的列名
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    # 打印表头
    print(f"Table: {table_name}")
    print(f"{', '.join(column_names)}")
    
    # 打印数据
    for record in records:
        print(record)
    
    # 关闭连接
    conn.close()

# 从指定数据表里查询指定学号的学生信息
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
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    # 打印结果
    if record:
        print(f"Student ID: {username}")
        for col_name, value in zip(column_names, record):
            print(f"{col_name}: {value}")
    else:
        print(f"No record found for username: {username}")
    
    # 关闭连接
    conn.close()

# 删除某一条信息
def delete_student_by_id(db_name, table_name, username):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 删除指定学号的学生信息
    query = f"DELETE FROM {table_name} WHERE username = ?"
    cursor.execute(query, (username,))
    
    # 提交事务
    conn.commit()
    
    # 关闭连接
    conn.close()


# 主函数，用来人机交互操作数据库
def main():
    files = os.listdir()
    db_files = [f for f in files if f.endswith('.sqlite3') or f.endswith('.db')]
    print(db_files)
    db_name = input("Enter the database file name: ")
    
    # 打印数据库中所有表的名称
    list_tables(db_name)
    table_name = input("Enter the table name: ")
   
   # 选择你的操作：打印表格、查询学生信息、删除学生信息
    operation = input("Enter the operation (print/query/delete): ")
    
    if operation == "print":
        print_table(db_name, table_name)
    elif operation == "query":
        username = input("Enter the student ID: ")
        query_student_by_id(db_name, table_name, username)
    elif operation == "delete":
        username = input("Enter the student ID: ")
        delete_student_by_id(db_name, table_name, username)
    else:
        print("Invalid operation. Please enter 'print', 'query', or 'delete'.")

    
if __name__ == '__main__':
    main()
