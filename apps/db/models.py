from django.db import models

class BaseModel(models.Model):
    create_date = models.DateField(auto_now_add=True,verbose_name="创建时间",help_text="创建时间")
    update_date = models.DateTimeField(auto_now=True,verbose_name="修改时间",help_text="修改时间")
    is_delete = models.BooleanField(default=False,verbose_name="逻辑删除",help_text="逻辑删除")

    class Meta:
        abstract = True