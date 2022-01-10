from django.urls import path

from .views import products, product_detail

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('product_detail/<int:pk>/', product_detail, name='product_detail'),
]
