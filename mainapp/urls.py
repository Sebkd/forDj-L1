from django.contrib import admin
from django.urls import path, include

from .views import products
from myShop.views import index

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('<int:pk>/', products, name='category'),
]
