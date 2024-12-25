from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

        
class Leave(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # 学号
    start_date = models.DateTimeField()  # 请假开始时间
    end_date = models.DateTimeField()  # 请假结束时间
    reason = models.TextField()  # 请假理由
    leave_time = models.DateTimeField(auto_now_add=True)  # 请假申请时间
    status = models.IntegerField(default=0)  #状态机
    approver = models.TextField(blank=True)  # 批准人（操作人）批准/拒绝/销假
    advisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leaves_advised', limit_choices_to={'groups__name': 'tch'})  # 新增字段：带班辅导员
    reject_reason = models.CharField(max_length=255, null=True, blank=True)  # 拒绝理由


    def __str__(self):
        return f'{self.student.last_name} - {self.student.class_set.first().name} - {self.reason}'

"""
重构数据库日志：
把数据表缩小为一个
 使用状态机
 状态机的状态：
 0:未批准   
 1:已批准
 2:已驳回
 3:已销假
 4:待审核
 5:已审核
 
 不得不承认，脑子不清晰的时候，不要上来就写写写，要先想清楚再写
 要修改的地方
 1.请假的方法都要改
 2.查表的方法也要改

 """
"""
使用多表继承（Multi-Table Inheritance），为每个用户组创建独立的 Profile 模型。
"""
# 基类
class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,db_index=True)
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user}的详细信息'

# leave/models.py

class StudentProfile(BaseProfile):
    assigned_class = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='students')
    advisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', limit_choices_to={'groups__name': 'tch'})  # 关联辅导员，且只选择 'tch' 组的教师

    def __str__(self):
        return f"{self.user.username} 的学生信息"


class TeacherProfile(BaseProfile):
    department = models.CharField(max_length=100, null=True, blank=True)
    # 其他教师特有字段
    # 如：
    # office_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} 的教师信息"


# leave/models.py

class Class(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 班级名称，如 "电气2304"
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes') # 外键关联教师
    description = models.TextField(null=True, blank=True)  # 班级描述

    def __str__(self):
        return self.name
