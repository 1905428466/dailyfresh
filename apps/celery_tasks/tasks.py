#使用celery
from celery import Celery
from django.core.mail import send_mail
import time

from dailyfresh.settings import EMAIL_FROM

#创建一个Celery类的实例对象
app = Celery("celery_tasks.tasks", broker="redis://127.0.0.1:6379/3")

#定义任务函数
@app.task()
def send_register_active_email(user_name,token,email):
    """发送激活有奖"""
    # 组织邮件信息
    subject = "来自邹栋的信息"  # 主题
    message = ""  # 内容
    sender = EMAIL_FROM
    receiver = [email]  # 目标邮箱
    html_message = "<h1>%s欢迎您成为该商品网站注册会员<h1/>请点击下面链接激活您的账户<br/><a href='http://127.0.0.1:8888/user/active/%s'>http://127.0.0.1:8888/user/active/%s<a/>" % (
    user_name, token, token)
    time.sleep(5)
    send_mail(subject, message, sender, receiver, html_message=html_message)  # 主题