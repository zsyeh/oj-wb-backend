# leave/management/commands/export_leaves.py

import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from leave.models import Leave
from leave.serializers import LeaveSerializer
from rest_framework.renderers import JSONRenderer
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = '导出所有请假条记录到指定的 Excel 文件'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='指定输出的 Excel 文件路径，例如 /path/to/output.xlsx',
            required=True
        )

    def handle(self, *args, **options):
        output_path = options['output']

        # 确保指定的目录存在
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                self.stdout.write(self.style.SUCCESS(f"已创建目录: {output_dir}"))
            except Exception as e:
                raise CommandError(f"无法创建目录 {output_dir}: {e}")

        try:
            # 获取所有请假条记录，并预加载相关字段以优化查询
            all_leaves = Leave.objects.all().select_related(
                'student__studentprofile__assigned_class', 
                'advisor'
            )

            # 序列化请假条数据
            serializer = LeaveSerializer(all_leaves, many=True)
            serialized_data = serializer.data

            # 检查序列化数据是否为空
            if not serialized_data:
                self.stdout.write(self.style.WARNING("没有请假条记录可导出。"))
                return

            # 转换为 pandas DataFrame
            df = pd.DataFrame(serialized_data)

            # 选择需要的字段并重命名（根据需要调整）
            fields_to_include = [
                'id', 'student_number', 'student_name', 'student_class',
                'student_email', 'advisor_name', 'start_date', 'end_date',
                'reason', 'leave_time', 'status', 'approver'
            ]
            df = df[fields_to_include]

            # 重命名列标题（根据需要调整）
            df.rename(columns={
                'id': '请假条ID',
                'student_number': '学号',
                'student_name': '学生姓名',
                'student_class': '班级',
                'student_email': '学生邮箱',
                'advisor_name': '辅导员姓名',
                'start_date': '开始日期',
                'end_date': '结束日期',
                'reason': '请假理由',
                'leave_time': '申请时间',
                'status': '状态',
                'approver': '批准人'
            }, inplace=True)

            # 导出为 Excel 文件
            df.to_excel(output_path, index=False)

            # 获取当前北京时间，用于文件名
            beijing_tz = pytz.timezone('Asia/Shanghai')
            now_beijing = datetime.now(beijing_tz)
            filename = now_beijing.strftime('%Y%m%d_%H%M%S') + '.xlsx'

            self.stdout.write(self.style.SUCCESS(f"成功导出 {len(df)} 条请假记录到 {output_path}"))
        except Exception as e:
            raise CommandError(f"导出过程中出错: {e}")

