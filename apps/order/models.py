from django.db import models
from apps.db.models import BaseModel
# Create your models here.

class OrderInfo(BaseModel):
    """订单模型类"""
    PAY_METHOD_CHOICES = (
        (1,"货到付款"),
        (2,"微信支付"),
        (3,"支付宝"),
        (4,"银联支付"),
    )

    ORDER_STATUS_CHOICES = (
        (1,"待支付"),
        (2,"待发货"),
        (3,"待收货"),
        (4,"待评论"),
        (5,"已完成"),
    )

    order_id = models.IntegerField(primary_key=True,verbose_name="订单id",help_text="订单id")
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="用户id", help_text="用户id")
    addr = models.ForeignKey("user.Address", on_delete=models.CASCADE, verbose_name="地址id", help_text="地址id")
    pay_meihod = models.SmallIntegerField(choices=PAY_METHOD_CHOICES,default=3,verbose_name="支付方式",help_text="支付方式")
    total_count = models.IntegerField(default=1,verbose_name="商品数量",help_text="商品数量")
    total_price = models.FloatField(verbose_name="支付金额",help_text="支付金额")
    transit_price = models.FloatField(verbose_name="运费",help_text="运费")
    order_status = models.SmallIntegerField(default=1,choices=ORDER_STATUS_CHOICES,verbose_name="支付状态",help_text="支付状态")
    trade_no = models.CharField(max_length=120,verbose_name="支付编码",help_text="支付编码")

    class Meta:
        db_table = "db_order_info"
        verbose_name = "订单"
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    """订单商品模型类"""
    order = models.ForeignKey("OrderInfo",on_delete=models.CASCADE)
    sku = models.ForeignKey("goods.GoodsSKU", on_delete=models.CASCADE)
    count = models.IntegerField(default=1,verbose_name="商品数量",help_text="商品数量")
    price = models.FloatField(verbose_name="商品价格",help_text="商品价格")
    comment = models.CharField(max_length=250,verbose_name="评论")

    class Meta:
        db_table = "db_order_goods"
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name



