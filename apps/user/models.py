from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.db.models import BaseModel
# Create your models here.
#
# #用户表
#
class User(AbstractUser,BaseModel):
    """用户模型类"""
    class Meta:
        db_table = "db_user"
#
class Address(models.Model):
    """地址模型类"""
    user = models.ForeignKey("User",verbose_name="所属账户",on_delete=models.CASCADE)
    receiver = models.CharField(max_length=30,verbose_name="收件人",help_text="收件人")
    addr = models.CharField(max_length=250,verbose_name="收货地址",help_text="收货地址")
    zip_code = models.CharField(max_length=6,null=True,verbose_name="邮箱编码",help_text="邮箱编码")
    phone = models.CharField(max_length=11,verbose_name="联系方式",help_text="联系方式")
    is_default = models.BooleanField(default=False,verbose_name="是否默认",help_text="是否默认")

    class Meta:
        db_table = "db_address"
        verbose_name = "地址"
        verbose_name_plural = verbose_name