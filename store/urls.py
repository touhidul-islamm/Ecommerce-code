from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('product_details/<int:pk>', product_details, name='product_details'),
    path('product_search/', product_search, name='product_search'),

    path('add_to_cart/<pk>/', add_to_cart, name='add_to_cart'),
    path('cart_summary/', cart_summary, name='cart_summary'),
    path('remove_cart/<pk>/', remove_cart, name='remove_cart'),
    path('cart_increment/<pk>/', cart_increment, name='cart_increment'),
    path('cart_decriment/<pk>/', cart_decriment, name='cart_decriment'),
]