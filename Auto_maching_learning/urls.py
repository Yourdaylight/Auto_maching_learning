"""Auto_maching_learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ModelSelection import model_selection_views
from django.urls import path, include
import ModelSelection.urls, UserAuthority.urls
import Engines.engine_urls
from django.conf.urls import url

urlpatterns = [
    path('', include(ModelSelection.urls)),
    path('admin/', admin.site.urls),
    path('model_selection/', include(ModelSelection.urls, namespace='model_selection')),
    path('user_authority/', include(UserAuthority.urls, namespace='user_authority')),
    path('engine/', include(Engines.engine_urls, namespace="engine"))

]
