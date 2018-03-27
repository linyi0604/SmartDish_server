from django.db import models

#模型的抽象基类

class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False,verbose_name='删除标记')  #verbose_name指定名称
    create_time = models.DateTimeField(auto_now_add=True)   #创建时间   创建的时候更新
    update_time = models.DateTimeField(auto_now=True)   #修改的时候更新

    class Meta:
        abstract = True #说明这个类是一个抽象模型