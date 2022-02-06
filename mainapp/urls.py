from django.urls import path

from .views import products, product_detail
from django.views.decorators.cache import cache_page

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    # path('category/<int:pk>/page/<int:page>/', products, name='page'), # to cached
    path('category/<int:pk>/page/<int:page>/', cache_page(3600)(products), name='page'),
    path('product_detail/<int:pk>/', product_detail, name='product_detail'),
]
