from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # return redirect('login')
                return redirect('access_denied')
            if not request.user.groups.filter(name=group_name).exists():
                return redirect('access_denied')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator