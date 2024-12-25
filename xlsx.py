import pandas as pd
import sqlite3

# 读取 XLSX 文件中的所有工作表
sheets = pd.read_excel('full_data.xlsx', sheet_name=None)

# 连接到 SQLite 数据库（如果数据库不存在，则会自动创建）
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# 动态创建 SQLite 数据库表
create_table_query = """
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    username TEXT PRIMARY KEY,
    password TEXT DEFAULT '123456',
    class TEXT DEFAULT 'None'
)
"""
cursor.execute(create_table_query)

# 遍历每个工作表并处理数据
for sheet_name, df in sheets.items():
    print(f"Processing sheet: {sheet_name}")
    
    # 提取姓名和学号，并添加默认字段
    df_filtered = df[['姓名', '学号']].copy()
    df_filtered['密码'] = '123456'
    df_filtered['班级'] = 'None'
    
    # 插入数据
    for index, row in df_filtered.iterrows():
        insert_query = "INSERT INTO students (name, username, password, class) VALUES (?, ?, ?, ?)"
        try:
            cursor.execute(insert_query, (row['姓名'], row['学号'], row['密码'], row['班级']))
        except sqlite3.IntegrityError:
            print(f"Duplicate entry for username: {row['学号']}")

# 提交事务并关闭连接
conn.commit()
conn.close()

print("数据已成功保存到 SQLite 数据库中。")