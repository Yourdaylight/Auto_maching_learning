from django.urls import path
from django.views.generic.base import TemplateView

from .views import *

app_name = 'api'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('index/', TemplateView.as_view(template_name='index.html')),
    path('check_exist', check_exist),  # 注册校验用户是否存在
    path('send_code', send_code),  # 发送验证码
    path('regist', regist),  # 注册
    path('login', login),  # 登录
    path('upload_dataset', upload_dataset),  # 上传数据集文件
    path('get_data_list', get_data_list),  # 获取数据集列表
    path('show_dataset', show_dataset),  # 预览数据集
    path('get_dataset_cols', get_dataset_cols), # 获取指定数据集的列名
    path('show_dataset_report', show_dataset_report),  # 预览数据报告
    path('get_clean_methods', get_clean_methods), # 获取数据清洗方法用于前端展示
    path('del_dataset', del_dataset),  # 删除数据集
    path('generate_code', generate_code),  # 生成代码
    path('export_code', export_code),  # 导出代码文件

]

