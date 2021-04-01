from django.urls import path

from .user_authority_view import *

app_name = 'user_authority'
urlpatterns = [
    path('check_exist', check_exist),  # 注册校验用户是否存在
    path('send_code', send_code),  # 发送验证码
    path('regist', regist),  # 注册
    path('login', login),  # 登录
]

