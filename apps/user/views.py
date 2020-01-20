import re
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.views import View
from django.core.mail import send_mail

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from dailyfresh.settings import SECRET_KEY,EMAIL_FROM
from user.models import User
from . import constant
from celery_tasks.tasks import send_register_active_email
# Create your views here.
class RegisterView(View):
    def get(self,request):
        """显示注册页面"""
        return render(request,"register.html")

    def post(self,request):
        """进行注册处理"""
        #1、获取参数
        user_name = request.POST.get("user_name")   #用户名
        pwd = request.POST.get("pwd")   #密码
        cpwd = request.POST.get("cpwd") #确认密码
        email = request.POST.get("email")   #邮箱
        allow = request.POST.get("allow")   #同意

        #2、校验参数
        if not all([user_name, pwd, cpwd, email]):   #参数是否为空
            return render(request,"register.html",context={"errmsg":"请把信息填写完整哦"})

        if not ((len(user_name) >= 5) and (len(user_name) <= 20)):
            return render(request, "register.html", context={"errmsg": "用户名最少5位，最大20位"})

        if not ((len(pwd) >= 8) and (len(pwd) <= 20)): #密码长度
            return render(request,"register.html",context={"errmsg":"密码最少8位，最大20位"})

        if not (pwd == cpwd):   #密码和确认密码不相同
            return render(request,"register.html",context={"errmsg":"密码和确认密码不一致哦"})

        if not re.match(r"^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$",email):    #判断邮箱格式
            return render(request,"register.html",context={"errmsg":"邮箱格式有误哦"})

        if not (allow == "on"): #网站协议
            return render(request,"register.html",context={"errmsg":"请同意协议哦"})

        #判断用户输入用户是否已经存在
        user = User.objects.filter(username=user_name)
        if user:
            return render(request,"register.html",context={"errmsg":"用户名已经注册，请重新输入"})

        #3、业务逻辑

        try:
            user = User.objects.create_user(username=user_name,password=pwd,email=email,is_active=0)   #保存数据
        except Exception as e:
            return render(request, "register.html", context={"errmsg": "服务器超时，请稍候再试"})

        #发送激活邮件，包含激活链接：http://127.0.0.1:8888/user/active/1
        #激活链接中需要包含用户的身份信息，并且把身份信息进行加密

        #加密用户的身份信息，生成激活token
        serializer = Serializer(SECRET_KEY,constant.MAILBOX_ACTIVATION_TIME)    #加密对象
        info = {constant.USER_MAILBOX: user.id}  #用户身份
        token = serializer.dumps(info).decode("UTF-8")  #加密

        #发送邮件
        send_register_active_email.delay(user_name,token,email)

        #4、返回数据
        return redirect(reverse("goods:index"))


class ActiveView(View):
    """用户激活"""
    def get(self,request,token):
        """进行用户激活"""
        #进行解密，获取要激活的用户信息
        serializer = Serializer(SECRET_KEY, constant.MAILBOX_ACTIVATION_TIME)
        try:
            info = serializer.loads(token)
            user_id = info[constant.USER_MAILBOX]

            #根据id获取用户信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            #跳转到登陆页面
            return redirect(reverse("user:login"))
        except Exception as e:
            #激活链接已过期
            return HttpResponse("激活链接已过期")


class LoginView(View):
    """登录"""
    def get(self,request):
        """显示登录页面"""
        return render(request,"login.html")