from django.urls import path
import orderapp.views as orderapp

app_name = 'orderapp'

urlpatterns = [
    path('', orderapp.OrderList.as_view(), name='order_list'),
    path('forming/complete/<int:pk>/', orderapp.order_forming_complete, name='order_forming_complete'),
    path('create/', orderapp.OrderCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', orderapp.OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', orderapp.OrderUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', orderapp.OrderDelete.as_view(), name='order_delete'),
    path('product/<int:pk>/price', orderapp.get_product_price),
]
