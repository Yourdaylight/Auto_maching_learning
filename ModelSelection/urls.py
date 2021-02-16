from django.urls import path
from ModelSelection import views
from django.conf.urls import url
from django.views.generic.base import TemplateView
from .views import *
app_name = 'api'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('index/', TemplateView.as_view(template_name='index.html')),
    path('upload_dataset',upload_dataset),
    path('get_data_list',get_data_list),
    path('show_dataset',show_dataset),
    path('del_dataset',del_dataset),
    path('generate_code',generate_code)
]