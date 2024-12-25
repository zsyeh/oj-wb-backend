import sqlite3
import pandas as pd

def generate_html_report(db_name, table_name, output_file):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 查询表中的所有记录
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    
    # 生成 HTML 报告
    html = df.to_html()
    
    # 保存 HTML 报告到文件
    with open(output_file, 'w') as f:
        f.write(html)
    
    # 关闭连接
    conn.close()

# 调用函数生成 HTML 报告
# 三个参数含义分别是：数据库文件名、表名、输出文件名
generate_html_report('db.sqlite3', 'django_admin_log', 'students_report.html')