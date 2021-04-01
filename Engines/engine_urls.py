from django.urls import path
from .engine_view import *

app_name = 'engine'
urlpatterns = [
    path('check_clean_condition', check_clean_condition),
]

