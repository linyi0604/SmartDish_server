from django.db import models
from db.base_model import BaseModel
from re_user.models import ReUserInfo
from django.conf import settings
import os
from utils.resize_picture import ResizeImage

class DishFeatureTypeManager(models.Manager):
    pass

class DishFeatureType(BaseModel):
    '''菜品特点分类'''
    typeName = models.CharField(max_length=20,unique=True,verbose_name="特征分类名称")

    objects = DishFeatureTypeManager()

    class Meta:
        db_table = "dish_feature_type"

class DishFeatureManager(models.Manager):
    def get_feature_table(self):
        # featureTypeList = DishFeatureType.objects.all()

        featureTypeList = DishFeatureType.objects.exclude(typeName="其他")
        featureTable = { t:self.filter(featureType=t) for t in featureTypeList}
        return featureTable

    def get_name_str_list_from_id_str_list(self,id_str_list):
        id_list = filter( lambda x: x!="" , id_str_list.lstrip("l").rstrip("]").split(",") )
        obj_list = self.filter(id__in = id_list)
        name_list = [obj.featureName for obj in obj_list]
        name_str_list = " ".join(name_list)
        return name_str_list


class DishFeature(BaseModel):
    '''菜品特征表'''
    featureType = models.ForeignKey("DishFeatureType",verbose_name="特征类别")
    featureName = models.CharField(max_length=10,verbose_name="特征名称")

    objects = DishFeatureManager()

    class Meta:
        db_table = "dish_feature"


class DishTypeManager(models.Manager):
    '''商家用户的模型管理器'''
    def get_one_object_by_id(self,tid):
        obj = self.filter(id=tid)
        if not obj:
            return None
        else:
            return obj[0]

    def add_one_object(self,userID, typename):
        obj = DishType(re_user=ReUserInfo(id=userID),typeName=typename)
        obj.save()
        return obj

    def get_type_list(self,userID):
        obj_list = self.filter(re_user=ReUserInfo(id=userID))
        return obj_list

    def delete_one_object(self,tid):
        obj = self.get_one_object_by_id(tid=tid)
        dishList = DishInfo.objects.get_dish_list_by_type(obj)

        for dish in dishList:
            try:
                imageDir = '%s/image/%s' % (settings.MEDIA_ROOT, dish.dishImage)
                os.remove(imageDir)
            except Exception as e:
                print(str(e))

        if obj is not None:
            obj.delete()

    def change_one_object(self,typeID,typeName):
        obj = self.get_one_object_by_id(typeID)
        obj.typeName = typeName
        obj.save()
        return obj

class DishType(BaseModel):
    '''菜品分类'''
    re_user = models.ForeignKey("re_user.ReUserInfo",verbose_name="餐厅用户id")
    typeName = models.CharField(max_length=40, verbose_name='菜品分类名称')

    # 指定模型管理器
    objects = DishTypeManager()

    # 指定数据库表名称
    class Meta:
        db_table='dish_type'


class DishInfoManager(models.Manager):
    def update_sell_count(self,dishList):
        for dish in dishList:
            from order.models import OrderInfo
            dish.dishSellCount = len(OrderInfo.objects.filter(dish=dish))
            dish.save()
        return dishList

    def add_one_object(self,dish_type,dishName,dishPrice,dishImage,dishDetail,dishFeature):
        dish_type = DishType.objects.get_one_object_by_id(dish_type)
        obj = DishInfo(dish_type=dish_type,dishName=dishName,dishPrice=dishPrice,
                       dishDetail=dishDetail,dishFeature=",".join(dishFeature))
        obj.save()
        obj.dishImage = str(obj.id) +"_dish_"+ dishImage.name
        imageDir = '%s/image/%s' % (settings.MEDIA_ROOT, obj.dishImage)
        try:
            with open(imageDir, 'wb') as pic:
                for c in dishImage.chunks():
                    pic.write(c)
            ResizeImage(imageDir)
        except Exception as e:
            print(e)
        obj.save()
        return obj

    def get_dish_list_by_type(self,type):
        dishList = self.filter(dish_type = type)
        return dishList

    def get_dish_list_by_type_list(self, typeList):
        dishList = self.filter(dish_type__in=typeList)
        return dishList

    def get_dish_by_condition(self, userID,dishTypeID,dishName, *k, **kw):
        if dishTypeID == "all":
            dishList = self.get_dish_list_by_type_list(DishType.objects.get_type_list(userID))
        else:
            dishList = self.get_dish_list_by_type(type=DishType.objects.get(id=dishTypeID))
        if dishName is not None:
            dishList = dishList.filter(dishName__contains=dishName)
        self.update_sell_count(dishList)
        return dishList

    def update_one_object(self,dishID,dishName,dishType,dishImage,dishPrice,dishDetail,dishFeature):
        obj = self.get(id=dishID)
        obj.dishName=dishName
        obj.dish_type=DishType.objects.get(id=dishType)
        obj.dishPrice=dishPrice
        obj.dishDetail=dishDetail
        obj.dishFeature = ",".join(dishFeature)
        if dishImage:
            # 先删除原来的照片
            try:
                imageDir = '%s/image/%s' % (settings.MEDIA_ROOT, obj.dishImage)
                os.remove(imageDir)
            except Exception as e:
                print(str(e))
            # 再添加新的照片
            obj.dishImage = str(obj.id) + "_dish_" + dishImage.name
            imageDir = '%s/image/%s' % (settings.MEDIA_ROOT, obj.dishImage)
            try:
                with open(imageDir, 'wb') as pic:
                    for c in dishImage.chunks():
                        pic.write(c)
                ResizeImage(imageDir)
            except Exception as e:
                print(e)
        obj.save()

    def get_dish_list(self):
        return self.all()

class DishInfo(BaseModel):
    '''菜品信息'''
    dish_type = models.ForeignKey("DishType",verbose_name="菜品分类")
    dishName = models.CharField(max_length=100, verbose_name="菜品名称")
    dishPrice = models.FloatField(default=0.00,verbose_name="菜品价格")
    dishImage = models.CharField(max_length=100,verbose_name="图片路径")
    dishFeature = models.CharField(max_length=500,default="", verbose_name="特点id列表")
    dishDetail = models.CharField(max_length=5000,verbose_name="菜品介绍")
    dishSellCount = models.IntegerField(default=0,verbose_name="销量")
    dishGrade = models.FloatField(default=0.0,verbose_name="评分")

    objects = DishInfoManager()

    class Meta:
        db_table = "dish_info"