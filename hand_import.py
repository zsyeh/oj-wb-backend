# coding=utf-8

import os
import django

def setup_django():
    """
    配置并初始化 Django 环境
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leave_management.settings')
    django.setup()

def get_or_create_group(group_name):
    from django.contrib.auth.models import Group
    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f"已创建用户组: {group_name}")
    return group

def get_or_create_class(class_name, description=''):
    from leave.models import Class
    from django.db import IntegrityError
    try:
        class_obj, created = Class.objects.get_or_create(
            name=class_name,
            defaults={'description': description}
        )
        if created:
            print(f"成功创建班级: {class_name}")
        else:
            print(f"班级已存在: {class_name}")
        return class_obj
    except IntegrityError:
        print(f"无法创建或获取班级: {class_name}")
        return None

def get_advisor_user(advisor_last_name):
    from django.contrib.auth.models import User
    try:
        advisor = User.objects.get(last_name=advisor_last_name, groups__name='tch')
        return advisor
    except User.DoesNotExist:
        print(f"辅导员 '{advisor_last_name}' 不存在或不属于 'tch' 组。")
        return None

def create_student(username, password, last_name, email, assigned_class, advisor):
    from django.contrib.auth.models import User
    from django.db import IntegrityError
    from leave.models import StudentProfile

    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            last_name=last_name,
            email=email,
            is_active=True,
        )
        stu_group = get_or_create_group('stu')
        user.groups.add(stu_group)

        # 确保 StudentProfile 关联正确
        if hasattr(user, 'studentprofile'):
            user.studentprofile.assigned_class = assigned_class
            user.studentprofile.advisor = advisor
            user.studentprofile.save()

        print(f"成功创建学生用户: {username}，关联班级: {assigned_class.name}，辅导员: {advisor.last_name}")
    except IntegrityError:
        print(f"用户名已存在，跳过: {username}")
    except Exception as e:
        print(f"创建学生用户时出错: {e}")

def main():
    setup_django()
    print("=== 手动导入学生数据脚本 ===\n")

    default_password = '123456'  # 默认密码，可根据需要修改

    while True:
        print("请依次输入学生的以下信息（输入 'q' 退出）：")

        # 输入学号
        username = input("学号: ").strip()
        if username.lower() == 'q':
            break
        if not username:
            print("学号不能为空。请重新输入。\n")
            continue

        # 输入姓名
        last_name = input("姓名: ").strip()
        if last_name.lower() == 'q':
            break
        if not last_name:
            print("姓名不能为空。请重新输入。\n")
            continue

        # 输入班级
        class_name = input("班级: ").strip()
        if class_name.lower() == 'q':
            break
        if not class_name:
            print("班级不能为空。请重新输入。\n")
            continue

        # 检查班级是否存在
        from leave.models import Class
        try:
            assigned_class = Class.objects.get(name=class_name)
            print(f"找到班级: {class_name}")
        except Class.DoesNotExist:
            print(f"班级 '{class_name}' 不存在。")
            create_cls = input("是否要创建这个班级？（y/n）: ").strip().lower()
            if create_cls == 'y':
                description = input("请输入班级描述（可选，直接回车跳过）: ").strip()
                assigned_class = get_or_create_class(class_name, description)
                if not assigned_class:
                    print("创建班级失败，请重新输入学生信息。\n")
                    continue
            else:
                print("无法关联班级，请重新输入学生信息。\n")
                continue

        # 输入辅导员姓名
        advisor_last_name = input("辅导员姓名（姓）: ").strip()
        if advisor_last_name.lower() == 'q':
            break
        if not advisor_last_name:
            print("辅导员姓名不能为空。请重新输入。\n")
            continue

        advisor = get_advisor_user(advisor_last_name)
        if not advisor:
            print("无法找到有效的辅导员，请重新输入学生信息。\n")
            continue

        # 输入电子邮箱（可选）
        email = input("电子邮箱（可选，直接回车跳过）: ").strip()

        # 创建学生
        create_student(
            username=username,
            password=default_password,
            last_name=last_name,
            email=email,
            assigned_class=assigned_class,
            advisor=advisor
        )

        print("\n学生信息已处理完成。\n")

        # 是否继续添加
        cont = input("是否继续添加下一个学生？（y/n）: ").strip().lower()
        if cont != 'y':
            break
        print("\n" + "-"*40 + "\n")

    print("\n=== 数据导入完成，脚本结束。 ===")

if __name__ == "__main__":
    main()
