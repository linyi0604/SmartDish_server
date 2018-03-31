from db.base_model import BaseModel
from django.db import models
from utils.get_hash import get_hash
from SmartDish import settings
import os
from utils.resize_picture import ResizeImage



class ReUserInfoAdmin(models.Manager):
    '''商家用户的模型管理器'''
    def add_one_object(self,username,password):
        # 对密码进行加密存储
        obj = self.model(username=username,password=get_hash(password))
        obj.save()
        return obj
    def get_one_object_by_username(self,username):
        obj = self.filter(username=username)
        if not obj:
            return None
        return obj[0]
    def update_one_object(self, username, name, phone, address, image, detail):
        '''更新一条信息'''
        obj = self.get(username=username)
        obj.name = name
        obj.phone = phone
        obj.address = address
        obj.detail = detail
        obj.save()
        if image:
            # 先删除原来的照片
            try:
                imageDir = '%s/image/%s' % (settings.MEDIA_ROOT, obj.image)
                os.remove(imageDir)
            except Exception as e:
                print(str(e))
            # 再添加新的照片
            obj.image = str(obj.id) + "_res_" + image.name
            imageDir = '%s/image/%s' % (settings.MEDIA_ROOT, obj.image)
            try:
                with open(imageDir, 'wb') as pic:
                    for c in image.chunks():
                        pic.write(c)
                ResizeImage(imageDir)
            except Exception as e:
                print(e)
            obj.save()
    def get_type_dish_list(self,res_id):
        '''通过餐厅id 获取菜单信息 种类和菜品'''
        from dish.models import DishType
        from dish.models import DishInfo
        type_list = DishType.objects.filter(re_user__id = res_id)
        return type_list

class ReUserInfo(BaseModel):
    '''餐厅用户的基本信息'''
    username = models.CharField(unique=True,max_length=50,verbose_name="商家用户名")
    password = models.CharField(max_length=40, verbose_name='密码')
    name = models.CharField(max_length=100,verbose_name="餐厅名称")
    image = models.CharField(max_length=100,default="", verbose_name="图片路径")
    address = models.CharField(max_length=100,verbose_name="餐厅地址")
    phone = models.CharField(max_length=50,verbose_name="餐厅电话")
    detail = models.CharField(max_length=1000,verbose_name="餐厅介绍")
    sellCount = models.IntegerField(default=0,verbose_name="销量")
    grade = models.FloatField(default=0.0,verbose_name="评分")

    # 指定模型管理器
    objects = ReUserInfoAdmin()

    # 指定数据库表名称
    class Meta:
        db_table='restaurant_info'