from my_framework.response import Response


def home_handler(request):
    return Response(body='Hello, this is the home page!')

def dashboard_handler(request):
    return Response(body=f'Welcome {request.user.username} to your dashboard!')

def admin_dashboard_handler(request):
    return Response(body=f'Welcome {request.user.username} to the admin dashboard!')
