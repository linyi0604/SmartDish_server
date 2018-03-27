from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^checkNewOrder$', views.checkNewOrder),    # 检查是否来了新的订单
    url(r'^finishOrder$', views.finishOrder),    # 用户完成订单结算
    url(r'^orderManage$', views.orderManage),    # 用户订单管理
]