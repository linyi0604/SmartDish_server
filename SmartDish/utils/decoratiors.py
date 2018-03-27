from  django.shortcuts import redirect
from django.http import HttpResponse
from utils.common import SECRET_KEY


# 检测用户是否登录 如果没有跳转到登录页面
def login_required(view_func):
    def wrapper(request,*args,**kwargs):
        if request.session.has_key("isLogin"):
            return view_func(request,*args,**kwargs)
        else:
            return redirect("/re_user/login/")
    return wrapper


# 检查是否是手机客户端发来的请求
def phone_required(func):
    def inner(request,*args,**kwargs):
        if request.GET.get("secret_key") == SECRET_KEY:
            return func(request,*args,**kwargs)
        else:
            return HttpResponse("非法入侵!")
    return inner