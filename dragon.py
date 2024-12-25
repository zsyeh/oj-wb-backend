import os
import django
import pandas as pd
import sqlite3
from django.conf import settings
from django.contrib.auth.hashers import make_password
from datetime import datetime

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ],
    PASSWORD_HASHERS=[
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
)

# 初始化 Django
django.setup()

def import_users_from_xlsx(xlsx_file, db_name):
    # 读取 XLSX 文件
    df = pd.read_excel(xlsx_file)
    
    # 连接到 SQLite 数据库（如果数据库不存在，则会自动创建）
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 动态创建 auth_user 表（如果不存在）
    create_table_query = """
    CREATE TABLE IF NOT EXISTS auth_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT NOT NULL,
        last_login DATETIME,
        is_superuser INTEGER NOT NULL,
        username TEXT NOT NULL UNIQUE,
        first_name TEXT,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        is_staff INTEGER NOT NULL,
        is_active INTEGER NOT NULL,
        date_joined DATETIME NOT NULL
    )
    """
    cursor.execute(create_table_query)
    
    # 设置默认密码并使用 pbkdf2_sha256 存储方式
    default_password = '123456'
    hashed_password = make_password(default_password, hasher='pbkdf2_sha256')
    
    # 遍历每一行数据并插入到 auth_user 表中
    for index, row in df.iterrows():
        username = row['学号']
        last_name = row['姓名']
        email = row['电子邮箱'] if '电子邮箱' in row else ''
        is_superuser = 0
        is_active = 1
        is_staff = 0
        date_joined = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        insert_query = """
        INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            cursor.execute(insert_query, (hashed_password, None, is_superuser, username, '', last_name, email, is_staff, is_active, date_joined))
        except sqlite3.IntegrityError:
            print(f"Duplicate entry for username: {username}")
    
    # 提交事务并关闭连接
    conn.commit()
    conn.close()

# 调用函数导入用户数据
import_users_from_xlsx('full_data.xlsx', 'db.sqlite3')

print("用户数据已成功导入到 SQLite 数据库中。")