from my_framework.response import Response
from my_framework.auth import login_required, role_required
from my_framework.template_engine import render_template

routes = {}

def route(path):
    def wrapper(func):
        routes[path] = func
        return func
    return wrapper

def get_handler(path):
    return routes.get(path, None)

@route('/')
def home(request):
    context = {'title': 'Home'}
    return Response(body=render_template('index.html', context))

@route('/login')
def login(request):
    context = {'title': 'Login'}
    return Response(body=render_template('login.html', context))

@route('/dashboard')
@login_required
def dashboard(request):
    return Response(body=f'Welcome {request.user.username} to your dashboard!')

@route('/admin')
@role_required('admin')
def admin_dashboard(request):
    return Response(body=f'Welcome {request.user.username} to the admin dashboard!')
