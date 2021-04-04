from django.urls import path
from django.views.generic.base import TemplateView

from .model_selection_views import *

app_name = 'model_selection'
urlpatterns = [
    path('upload_dataset', upload_dataset),  # 上传数据集文件
    path('get_data_list', get_data_list),  # 获取数据集列表
    path('show_dataset', show_dataset),  # 预览数据集
    path('get_dataset_cols', get_dataset_cols), # 获取指定数据集的列名
    path('show_dataset_report', show_dataset_report),  # 预览数据报告
    path('get_methods', get_methods), # 获取生成代码的方法
    path('generate_code', generate_code),  # 生成代码
    path('export_code', export_code),  # 导出代码文件
    path('del_dataset', del_dataset),  # 删除数据集

]

