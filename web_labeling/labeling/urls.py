from django.contrib import admin, auth
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
        path('<str:datas_name>/<str:data>', views.detail_labeling),
    
]

