from django.conf.urls import url

from app01 import views

urlpatterns = [

    url(r'^add/', views.user_add, name='add'),
    url(r'change/(\d+)/', views.user_change, name='change'),
    url(r'delete/(\d+)/', views.user_delete, name='delete'),
    url(r'', views.index),
]