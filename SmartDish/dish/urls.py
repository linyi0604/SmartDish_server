from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dish', views.dishManage),  # 用户菜品管理
    url(r'^typeManage', views.typeManage),  # 用户菜品分类管理
    url(r'^addType', views.addType),  # 用户添加菜品分类
    url(r'^deleteType', views.deleteType),  # 用户删除菜品分类
    url(r'^changeTypeName', views.changeTypeName),  # 用户修改菜品分类名称
    url(r'^addDish', views.addDish),  # 用户添加菜品
    url(r'^editDish', views.editDish),  # 用户编辑菜品


]