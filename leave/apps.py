from django.apps import AppConfig
# leave/apps.py

from django.apps import AppConfig

class LeaveConfig(AppConfig):
    name = 'leave'

    def ready(self):
        import leave.signals  # 导入信号处理器


