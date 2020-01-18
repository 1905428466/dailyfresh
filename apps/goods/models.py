from django.db import models
from apps.db.models import BaseModel

# Create your models here.

class GoodsType(BaseModel):
    """商品类型模型类"""
    name = models.CharField(max_length=30,verbose_name="商品种类",help_text="商品种类")
    logo = models.CharField(max_length=20,verbose_name="商品种类logo",help_text="商品种类logo")
    image = models.URLField(verbose_name="种类图片",help_text="种类图片")

    class Meta:
        db_table = "db_goods_type"
        verbose_name = "商品种类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """商品spu模型表"""
    name = models.CharField(max_length=20,verbose_name="商品spu名称",help_text="商品spu名称")
    detail = models.TextField(verbose_name="商品详情",help_text="商品详情")

    class Meta:
        db_table = "db_goods"
        verbose_name = "商品spu"
        verbose_name_plural = verbose_name


class GoodsSKU(BaseModel):
    """商品sku模型类"""
    status_choices = (
        (0,"下线"),
        (1,"上线"),
    )
    type = models.ForeignKey("GoodsType",on_delete=models.CASCADE,verbose_name="商品种类")
    goods = models.ForeignKey("Goods",on_delete=models.CASCADE,verbose_name="商品spu")
    name = models.CharField(max_length=30,verbose_name="商品名称",help_text="商品名称")
    desc = models.TextField(verbose_name="商品简介",help_text="商品简介")
    price = models.FloatField(verbose_name="商品价格",help_text="商品价格")
    unite = models.CharField(max_length=20,verbose_name="商品单位",help_text="商品单位")
    image = models.URLField(verbose_name="商品图片",help_text="商品图片")
    stock = models.IntegerField(verbose_name="商品库存",help_text="商品库存")
    sales = models.IntegerField(verbose_name="商品销量",help_text="商品销量")
    status = models.SmallIntegerField(default=1, choices=status_choices,verbose_name="商品状态",help_text="商品状态")


class GoodsImage(BaseModel):
    """商品图片模型类"""
    type = models.ForeignKey("GoodsSKU",on_delete=models.CASCADE)
    image = models.URLField(verbose_name="商品图片",help_text="商品图片")

    class Meta:
        db_table = "db_goods_image"
        verbose_name = "商品图片"
        verbose_name_plural = verbose_name


class IndexGoodsBanner(BaseModel):
    """首页轮播商品展示模型类"""
    image_priority = (
        (1,"第一级"),
        (2,"第二级"),
        (3,"第三级"),
        (4,"第四级"),
        (5,"第五级"),
        (6,"第六级"),
    )
    sku = models.ForeignKey("GoodsSKU",on_delete=models.CASCADE)
    image = models.URLField(verbose_name="轮播图图片",help_text="轮播图图片")
    index = models.SmallIntegerField(default=1,choices=image_priority,verbose_name="轮播图优先级",help_text="轮播图优先级")

    class Meta:
        db_table = "db_index_goods_banner"
        verbose_name = "首页轮播图"
        verbose_name_plural = verbose_name


class IndexTypeGoodsBanner(BaseModel):
    """首页分类商品展示模型表"""
    DISPLAY_TYPE_CHOICES = (
        (0,"文字"),
        (1,"图片")
    )
    goods_priority = (
        (1, "第一级"),
        (2, "第二级"),
        (3, "第三级"),
        (4, "第四级"),
        (5, "第五级"),
        (6, "第六级"),
    )
    sku = models.ForeignKey("GoodsSKU",on_delete=models.CASCADE)
    goodstype = models.ForeignKey("GoodsType",on_delete=models.CASCADE)
    display_type = models.SmallIntegerField(default=0,choices=DISPLAY_TYPE_CHOICES,verbose_name="展示类型",help_text="展示类型")
    index = models.SmallIntegerField(default=1,choices=goods_priority,verbose_name="轮播图优先级",help_text="轮播图优先级")

    class Meta:
        db_table = "db_index_type_goods_banner"
        verbose_name = "首页分类商品"
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):
    """首页促销活动表"""
    name = models.CharField(max_length=20,verbose_name="活动名称",help_text="活动名称")
    image = models.URLField(verbose_name="首页促销活动图片",help_text="首页促销活动图片")
    url = models.URLField(verbose_name="首页促销活动链接",help_text="首页促销活动链接")
    index = models.SmallIntegerField(verbose_name="首页促销活动图片优先级",help_text="首页促销活动图片优先级")

    class Meta:
        db_table = "db_index_promotion_banner"
        verbose_name = "首页促销活动"
        verbose_name_plural = verbose_name


