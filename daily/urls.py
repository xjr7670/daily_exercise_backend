#-*- coding:utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update', views.receive_data, name='daily'),
    path('post_test', views.post_test, name='test'),
    path('get_data', views.get_data, name='get'),
    path('upload', views.upload, name='upload'),
]
