# decorators.py

from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def group_required(*group_names):
    """
    装饰器，用于检查用户是否属于指定的一个或多个用户组。
    
    参数:
        *group_names (str): 一个或多个用户组名称。
        
    使用示例:
        @api_view(['GET'])
        @group_required('tch', 'admin')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 检查用户是否已认证
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {'detail': 'Authentication credentials were not provided.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # 检查用户是否属于任何一个指定的组
            if not request.user.groups.filter(name__in=group_names).exists():
                return Response(
                    {'detail': 'You do not have permission to perform this action.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # 用户通过了权限检查，继续处理视图
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    return decorator
