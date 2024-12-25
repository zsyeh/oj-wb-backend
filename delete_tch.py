# coding=utf-8

import os
import django
import pandas as pd
import argparse  # 导入 argparse 库

# 配置 Django 设置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leave_management.settings')
django.setup()

from django.contrib.auth.models import User, Group

# 获取 `tch` 组
try:
    tch_group = Group.objects.get(name="tch")
except Group.DoesNotExist:
    print("Group 'tch' does not exist.")
else:
    # 查询属于 `tch` 组的用户
    users_in_tch_group = User.objects.filter(groups=tch_group)

    # 逐个删除用户的组关系，然后删除用户
    for user in users_in_tch_group:
        user.groups.clear()  # 清除用户的所有组关联
        user.delete()        # 删除用户

    print(f"Deleted users from 'tch' group.")

