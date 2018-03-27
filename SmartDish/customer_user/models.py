from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash


class FavoriteAdmin(models.Manager):
    '''购物车模型管理'''
    def add_one_object(self,dish_id,username):
        obj = Favorite(dish_id=dish_id,customer = CustomerUserInfo.objects.get(username=username))
        obj.save()

    def delete_by_id(self,event_id):
        obj = self.get(id=event_id)
        obj.delete()

class Favorite(BaseModel):
    '''购物车'''
    customer = models.ForeignKey("CustomerUserInfo",verbose_name="顾客")
    dish = models.ForeignKey("dish.DishInfo", verbose_name='菜品')

    # 指定模型管理器
    objects = FavoriteAdmin()

    # 指定数据库表名称
    class Meta:
        db_table='favorite'


class CartAdmin(models.Manager):
    '''购物车的模型管理器'''
    def update_one_object(self,cart_id,count):
        ''' 更新购物车商品数量 '''
        obj = self.get(id = cart_id)
        obj.count = count
        obj.save()

    def add_to_cart(self, username, dish_id):
        '''添加某商品到购物车'''
        customer = CustomerUserInfo.objects.get_one_object_by_username(username)
        # 检查是否已经在购物车里
        cart = self.filter(dish_id=dish_id,customer=customer)
        if cart: # 如果该用户购物车有该商品 就增加一个
            cart = cart[0]
            cart.count = cart.count + 1
            cart.save()
        else:   # 如果没有 就心增加一条数据
            cart = Cart(customer=customer,dish_id=dish_id)
            cart.save()
        return cart

    # 获取某用户的购物车列表
    def get_cart_info(self,username):
        cart_info = self.filter(customer__username=username,is_payed=False)
        return cart_info

    def delete_by_id_list(self,id_list):
        '''通过id列表删除购物车中商品'''
        obj_list = self.filter(id__in = id_list )
        for obj in obj_list:
            obj.delete()

    def delete_by_username_and_dish_id_list(self,username,dish_id_list):
        '''通过用户名和菜品id 删除购物车中的商品'''
        customer = CustomerUserInfo.objects.get_one_object_by_username(username)
        for i in dish_id_list:
            obj = self.get(customer=customer,dish_id=i)
            obj.delete()



class Cart(BaseModel):
    '''购物车'''
    customer = models.ForeignKey("CustomerUserInfo",verbose_name="顾客")
    dish = models.ForeignKey("dish.DishInfo", verbose_name='菜品')
    count = models.IntegerField(default=1,verbose_name="商品数量")
    is_payed = models.BooleanField(default=False,verbose_name="是否结帐")


    # 指定模型管理器
    objects = CartAdmin()

    # 指定数据库表名称
    class Meta:
        db_table='cart'


class CustomerUserInfoAdmin(models.Manager):
    '''顾客用户的模型管理器'''
    def add_one_object(self,username,password):
        user = CustomerUserInfo(username=username,password=get_hash(password))
        user.save()

    def get_one_object_by_username(self, username):
        user = self.filter(username=username)
        if user:
            return user[0]
        else:
            return None

    def update_one_object(self,username,password,name,phone,detail):
        '''更新一条用户的基本信息'''
        obj = self.get(username=username)
        obj.password = get_hash(password)
        obj.name = name
        obj.phone = phone
        obj.detail = detail
        obj.save()


class CustomerUserInfo(BaseModel):
    '''餐厅用户的基本信息'''
    username = models.CharField(unique=True,max_length=50,verbose_name="顾客用户名")
    password = models.CharField(max_length=40, verbose_name='密码')
    name = models.CharField(max_length=100,verbose_name="客户昵称 姓名")
    phone = models.CharField(max_length=50,verbose_name="电话号码")
    detail = models.CharField(max_length=1000,verbose_name="自我介绍")

    # 指定模型管理器
    objects = CustomerUserInfoAdmin()

    # 指定数据库表名称
    class Meta:
        db_table='customer_info'
