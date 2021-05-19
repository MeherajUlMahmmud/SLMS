from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_publisher:
            return redirect('publisher-dashboard')
        elif request.user.is_authenticated and request.user.is_student:
            return redirect('student-dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
