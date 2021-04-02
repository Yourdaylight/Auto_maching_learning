from django.urls import path
from .engine_view import *
from utils.views2urls import views2urls

app_name = 'engine'


# urlpatterns = views2urls("Engines.engine_view")
urlpatterns = [
    # 校验清洗规则
    path('check_clean_condition', check_clean_condition),
    # 清洗完成的数据保存
    path('save_clean_data', save_clean_data)
]

