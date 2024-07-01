import functools
from my_framework.response import Response
from my_framework.crud import get_user_by_id

def login_required(handler):
    @functools.wraps(handler)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response(body='Unauthorized', status=401)
        user = get_user_by_id(user_id)
        if not user:
            return Response(body='Unauthorized', status=401)
        request.user = user
        return handler(request, *args, **kwargs)
    return wrapper

def role_required(role):
    def decorator(handler):
        @functools.wraps(handler)
        def wrapper(request, *args, **kwargs):
            if not request.user or request.user.role != role:
                return Response(body='Forbidden', status=403)
            return handler(request, *args, **kwargs)
        return wrapper
    return decorator
