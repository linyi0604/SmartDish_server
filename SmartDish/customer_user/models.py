from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash
from dish.models import DishInfo
import random

class CustomerRecordAdmin(models.Manager):
    '''用户浏览菜品轨迹'''
    def login(self, old_username,user):
        '''登陆用户删除旧的浏览轨迹'''
        old_step_list = self.filter(username=old_username)
        for n in old_step_list:
            self.add_one_step(n.dish.id,user.username)
        for o in old_step_list:
            o.delete()

    def add_one_step(self,dish_id,username):
        # if self.filter(username=username,dish_id=dish_id):
        #     return

        if len(self.filter(username=username)) >= 5:
            self.filter(username=username).order_by("create_time")[0].delete()

        dish = DishInfo.objects.get(id=dish_id)
        if username.startswith("notLogin"): # 未登录用户
            curCustomer = CustomerUserInfo.objects.filter(id = 1)
            if not curCustomer:
                curCustomer = CustomerUserInfo(id = 1)
                curCustomer.save()
            obj = CustomerRecord(dish=dish,
                                 isLogin=False,
                                 customer=curCustomer[0],
                                 username=username,
                                 dishFeature=dish.dishFeature)
            obj.save()
        else:
            obj = CustomerRecord(dish=dish,
                                 customer=CustomerUserInfo.objects.get(username=username),
                                 isLogin=True,
                                 username=username,
                                 dishFeature=dish.dishFeature)
            obj.save()

    def get_step_dish_list(self, username):
        '''获得某个用户的历史浏览轨迹'''
        step_list = self.filter(username=username)
        return [step.dish for step in step_list]

    def calculate_feature_to_dict(self,dish_list):
        feature_dict = {}
        for step in dish_list:
            features = step.dishFeature.split(",")
            for f in features:
                if f in feature_dict.keys():
                    feature_dict[f] += 1
                else:
                    feature_dict[f] = 1
        return feature_dict

    def get_recommend_list_from_dish_list(self,dish_list):
        user_favorite_dict = self.calculate_feature_to_dict(dish_list=dish_list)
        user_fav_top_list = sorted(user_favorite_dict.items(), key=lambda d: d[1], reverse=True)
        top_fav = [i[0] for i in user_fav_top_list[0:3]]

        recommend_list = DishInfo.objects.filter()
        res_list_list = [recommend_list]

        for i in top_fav:
            recommend_list = recommend_list.filter(dishFeature__contains=i)
            res_list_list.insert(0, recommend_list)

        r_list = []
        for i in res_list_list:
            if len(i) >= 50:
                k = [j for j in i]
                random.shuffle(k)
                return k
            r_list += i
        k = [j for j in r_list]
        random.shuffle(k)
        return k

    def get_recommend_list(self, username):
        '''获得该用户的推荐商品列表'''
        dish_list = self.get_step_dish_list(username=username)
        return self.get_recommend_list_from_dish_list(dish_list)

    def get_recommend_list_from_dish_id(self, dish_id):
        '''寻找与该道菜相似的菜品'''
        dish = DishInfo.objects.get(id=dish_id)
        feature_list = dish.dishFeature.split(",")[0:2]
        recommend_list = DishInfo.objects.filter(dishFeature__contains=feature_list[0]) \
                            .filter(dishFeature__contains=feature_list[1])
        if len(recommend_list)<9:
            recommend_list = DishInfo.objects.filter(dishFeature__contains=feature_list[0])

        k = [j for j in recommend_list]
        random.shuffle(k)
        return k

class CustomerRecord(BaseModel):
    '''用户浏览菜品轨迹'''
    isLogin = models.BooleanField(default=False,verbose_name="是否登陆用户")
    customer = models.ForeignKey("CustomerUserInfo",default="",verbose_name="顾客")
    username = models.CharField(default="",max_length=200,verbose_name="用户名")
    dish = models.ForeignKey("dish.DishInfo", verbose_name='菜品')
    dishFeature = models.CharField(max_length=500, default="", verbose_name="特点id列表")

    # 指定模型管理器
    objects = CustomerRecordAdmin()

    # 指定数据库表名称
    class Meta:
        db_table='customer_record'


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
