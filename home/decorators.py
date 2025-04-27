from django.http import HttpResponseForbidden
from functools import wraps

from django.shortcuts import redirect
from functools import wraps



def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')  # Redirect to login if not authenticated
            
            if request.user.role != required_role:
                return redirect_based_on_role(request.user)  # Redirect unauthorized users
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def redirect_based_on_role(user):
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'general-user':
        return redirect('general_user_dashboard')
    elif user.role == 'approver':
        return redirect('approver_dashboard')
    return redirect('login')