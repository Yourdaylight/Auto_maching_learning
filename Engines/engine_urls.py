from django.urls import path

from .engine_view import *

app_name = 'engine'

# urlpatterns = views2urls("Engines.engine_view")
urlpatterns = [
    # 校验清洗规则
    path('check_clean_condition', check_clean_condition),
    # 清洗完成的数据保存
    path('save_clean_data', save_clean_data),
    # 建模特征列检测
    path('check_mining_condition', check_mining_condition),
    # 运行生成的建模代码,并生成报告
    path('run_mining_code', run_mining_code)
]
