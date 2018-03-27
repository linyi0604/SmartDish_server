from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), # 返回商家首页
    url(r'^register', views.register), # 返回注册页面
    url(r'^login', views.login),    # 返回登陆页面
    url(r'^adminPage', views.adminPage),    # 返回商家个人管理页面
    url(r'^logout', views.logout),    # 用户注销登陆
    url(r'^changePassword', views.changePassword),    # 用户修改密码
    url(r'^myRestaurant', views.myRestaurant),    # 用户餐厅信息编辑
]