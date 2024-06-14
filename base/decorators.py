from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == 'adm':
                return redirect('admin_page')
            elif request.user.role == 'prof':
                return redirect('professor')
            else:
                return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_funct):
        def wrapper_func(request, *args, **kwargs):
            group = None
            
            if request.user.role == 'adm':
                group = 'admin'
            elif request.user.role == 'prof':
                group = 'professor'
            else:
                group = 'student'

            if group in allowed_roles:
                return view_funct(request, *args, **kwargs)
            else:
                return HttpResponse('<h2>You are not authorized</h2>')
        return wrapper_func
    return decorator