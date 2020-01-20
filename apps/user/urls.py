from django.urls import path
from . import views


app_name = "user"
urlpatterns = [
    path("register/",views.RegisterView.as_view(),name="register"), #注册
    path("login/",views.LoginView.as_view(),name="login"), #登录
    path("active/<token>/",views.ActiveView.as_view(),name="active"), #注册激活
]
