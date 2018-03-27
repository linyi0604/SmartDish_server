from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import *
from utils.decoratiors import login_required
from dish.models import DishType
# Create your views here.

# / 返回首页
def index(request):
    '''返回首页'''
    # 检查session 如果已经登过 直接跳转到管理页
    if request.session.has_key("isLogin"):
        return redirect("/re_user/adminPage/")
    return render(request,'re_user/index.html')

# /re_user/register
@require_http_methods(['GET','POST']) # 限制访问请求类型
def register(request):
    '''get返回注册页面 post完成注册逻辑'''
    if request.method == "GET": # 返回注册页面
        return render(request,"re_user/register.html")
    else: # 完成注册逻辑
        username = request.POST.get("username")
        password = request.POST.get("password")
        target = request.POST.get("target")

        # 发来ajax 验证用户名 是否重复 不重复返回ok 否则返回notOK
        if target == "check":
            user = ReUserInfo.objects.get_one_object_by_username(username=username)
            if not user:
                return JsonResponse(data={"res":"OK"})
            else:
                return JsonResponse(data={"res":"notOK"})

        # 用户名和密码保存到数据库
        try:
            user = ReUserInfo.objects.add_one_object(username,password)
            DishType.objects.add_one_object(userID = user.id,typename="默认")
        except Exception as e:
            print(str(e))
        # 注册后跳转登陆页面
        return redirect("/re_user/login")


# /re_user/login
@require_http_methods(['GET', 'POST'])  # 限制访问请求类型
def login(request):
    '''get返回登陆页面 post登陆逻辑'''
    if request.method == "GET":
        # 检查session 如果已经登过 直接跳转到管理页
        if request.session.has_key("isLogin"):
            return redirect("/re_user/adminPage/")
        return render(request,"re_user/login.html")
    else:
        '''
            用户名存在且密码正确返回OK
            否则返回notOK
        '''
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 进入数据库查询用户
        user = ReUserInfo.objects.get_one_object_by_username(username=username)
        if not user: # 没查到该用户
            return JsonResponse(data={"info": "notOK"})
        if user.password != get_hash(password): # 密码错误
            return JsonResponse(data={"info": "notOK"})

        # 给该用户设置session
        request.session["isLogin"] = True
        request.session["username"] = username
        request.session["userID"] = user.id
        request.session.set_expiry(0) # 退出浏览器 失效

        return JsonResponse(data={"info":"OK"})

# /re_user/logout/ 退出登录
@login_required
def logout(request):
    print(request)
    request.session.flush()

    return redirect("/")

# /re_user/adminPage/ 商家个人管理主页
@login_required
def adminPage(request):
    '''返回商家个人管理页面'''
    userID = request.session.get("userID")
    username = request.session.get("username")

    return render(request,"re_user/adminPage.html")

# /re_user/changePassword/  修改密码
@login_required
@require_http_methods(['GET', 'POST'])  # 限制访问请求类型
def changePassword(request):
    if request.method == "GET":
        return render(request,"re_user/changePassword.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 操作数据库 修改密码
        try:
            obj = ReUserInfo.objects.get_one_object_by_username(username=username)
            obj.password = get_hash(password)
            obj.save()
            request.session.flush()
            return JsonResponse({"msg": "OK"})
        except Exception as e:
            return JsonResponse({"msg":"修改失败:"+str(e)})


# /re_user/myRestaurant/ 用户餐厅信息编辑
@login_required
@require_http_methods(['GET', 'POST'])  # 限制访问请求类型
def myRestaurant(request):
    if request.method == "GET":
        username = request.session.get("username")
        try:
            obj = ReUserInfo.objects.get_one_object_by_username(username=username)
            context = {
                "name":obj.name,
                "phone":obj.phone,
                "address":obj.address,
                "detail":obj.detail,
                "image":obj.image,
            }
            return render(request, "re_user/myRestaurant.html",context=context)
        except Exception as e:
            return render(request, "re_user/myRestaurant.html")

    else:
        username = request.session.get("username")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        detail = request.POST.get("detail")
        image = request.FILES.get("resImage")

        try:
            ReUserInfo.objects.update_one_object(username=username,name=name,phone=phone,address=address,image=image,detail=detail)
            return redirect("/re_user/myRestaurant")
        except Exception as e:
            return JsonResponse({"msg": str(e)})









