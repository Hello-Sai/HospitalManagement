# from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages


def is_doctor(view):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.info(request,"Please Login to your Account")
            return redirect("home")
        elif not request.user.is_doctor:
            messages.info(request,"Doctors can only create blogs")
            return redirect("dashboard")
        else:
            return view(request,*args,**kwargs)
    return wrapper