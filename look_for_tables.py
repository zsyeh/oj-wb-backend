import sqlite3

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

# 调用查询函数
list_tables('db.sqlite3')