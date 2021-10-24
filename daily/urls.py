#-*- coding:utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('daily', views.receive_data, name='daily'),
    path('page', views.show_html, name='html'),
    path('post_test', views.post_test, name='test'),
]
