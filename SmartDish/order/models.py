from db.base_model import BaseModel
from django.db import models
from customer_user.models import CustomerUserInfo
from utils.common import TIME_DELAY

class OrderNoAdmin(models.Manager):
    '''订单标管理器'''

    def check_new_order(self,username):
        '''检查用户是否有新的未看到的订单'''
        obj_list = self.filter(re_user__username=username,is_payed=False,is_checked=False)
        if obj_list:
            return True
        else:
            return False

    def finish_one_obj(self, orderId):
        '''完成一个订单的结算'''
        order = self.get(id = orderId)
        order.is_payed = True
        order.save()

    def get_order_list_by_user_and_sort(self,userID,startTime,endTime,keyWord,isPayed):
        from re_user.models import ReUserInfo
        from datetime import timedelta
        if startTime and endTime:
            orderList = OrderNo.objects.filter(re_user=ReUserInfo.objects.get(id=userID),create_time__gte=startTime,create_time__lte=endTime)
        elif startTime and not endTime:
            orderList = OrderNo.objects.filter(re_user=ReUserInfo.objects.get(id=userID), create_time__gte=startTime)
        elif not startTime and endTime:
            orderList = OrderNo.objects.filter(re_user=ReUserInfo.objects.get(id=userID),create_time__lte=endTime)
        else:
            orderList = OrderNo.objects.filter(re_user=ReUserInfo.objects.get(id=userID))
        if isPayed is not None:
            orderList = orderList.filter(is_payed=isPayed)
        orderList = orderList.order_by("-create_time")
        for o in orderList:
            o.is_checked = True
            o.save()
            o.create_time = (o.create_time+timedelta(hours=TIME_DELAY)).strftime("%Y-%m-%d %H:%M:%S")

        return orderList

    def add_one_order(self, username,cart_list):
        '''添加一条订单'''
        re_user = cart_list[0].dish.dish_type.re_user
        count = 0
        price = 0
        for c in cart_list:
            price += c.dish.dishPrice * c.count
            count += c.count
        obj = OrderNo(customer=CustomerUserInfo.objects.get_one_object_by_username(username),re_user=re_user,count=count,price=price)
        obj.save()
        return obj

class OrderNo(BaseModel):
    '''订单表'''
    customer = models.ForeignKey("customer_user.CustomerUserInfo",verbose_name="顾客")
    re_user = models.ForeignKey("re_user.ReUserInfo",verbose_name="餐厅")
    is_payed = models.BooleanField(default=False,verbose_name="是否结帐")
    count = models.IntegerField(default=0,verbose_name="商品总数量")
    price = models.FloatField(default=0,verbose_name="订单金额")
    is_checked = models.BooleanField(default=False,verbose_name="商家是否查看过")


    # 指定模型管理器
    objects = OrderNoAdmin()

    # 指定数据库表名称
    class Meta:
        db_table='order_no'



class OrderInfoAdmin(models.Manager):
    '''订单详情信息管理'''
    def get_order_info_list(self,orderList):
        '''通过orderNo编号查询订单详情信息'''
        orderInfoList = [{
            "orderNo":order,
            "orderInfo":self.filter(order=order),
        } for order in orderList ]

        return orderInfoList


    def add_by_order_and_cart_list(self, order, cart_list):
        '''通过菜品id列表添加订单信息'''
        for cart in cart_list:
            obj = OrderInfo(order=order, dish=cart.dish,count=cart.count)
            obj.save()


class OrderInfo(BaseModel):
    '''订单详细信息表'''
    order = models.ForeignKey("OrderNo",verbose_name="订购单")
    dish = models.ForeignKey("dish.DishInfo",verbose_name="菜品")
    count = models.IntegerField(default=0,verbose_name="菜品数量")


    # 指定模型管理器
    objects = OrderInfoAdmin()

    # 指定数据库表名称
    class Meta:
        db_table='order_info'
