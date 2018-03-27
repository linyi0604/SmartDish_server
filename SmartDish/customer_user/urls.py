from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getDishPage$', views.getDishPage), # 获取菜品页面所有信息
    url(r'^getDishList$', views.getDishList), # 获取所有菜品列表


    url(r'^getOrderInfo$', views.getOrderInfo), # 获取某条订单详情信息
    url(r'^getOrder$', views.getOrder), # 获取订单清单
    url(r'^addOrder$', views.addOrder), # 购物车结算到订单
    url(r'^getTypeDishInfo$', views.getTypeDishInfo), # 获取餐厅菜单 分类 菜品 信息
    url(r'^getResInfo$', views.getResInfo), # 获取餐厅详细信息
    url(r'^searchRes$', views.searchRes), # 搜索菜品
    url(r'^searchDish$', views.searchDish), # 搜索菜品
    url(r'^deleteFavorite$', views.deleteFavorite), # 删除收藏夹中的商品
    url(r'^getFavorite$', views.getFavorite), # 获得收藏夹所有商品
    url(r'^checkFavorite$', views.checkFavorite), # 检查是否在收藏夹
    url(r'^addFavorite$', views.addFavorite), # 添加到收藏夹
    url(r'^updateCustomerInfo$', views.updateCustomerInfo), # 手机用户修改个人信息
    url(r'^deleteCartInfo$', views.deleteCartInfo), # 删除购物车中某商品
    url(r'^updateCartDishCount$', views.updateCartDishCount), # 修改购物车某条商品数量
    url(r'^getCart$', views.getCart), # 手机用户申请购物车数据
    url(r'^addCart$', views.addCart), # 手机用户添加购物车
    url(r'^register$', views.register), # 手机用户注册
    url(r'^login$', views.login), # 手机用户登陆

]