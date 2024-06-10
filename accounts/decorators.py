from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "You need to logout first")
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
