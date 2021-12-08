from django.contrib import admin
from django.urls import path, include

from .views import products
from myShop.views import index

urlpatterns = [
    path('', products),

]