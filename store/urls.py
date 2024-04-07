from django.urls import path
from .views import index, product_details, product_search

urlpatterns = [
    path('', index, name='index'),
    path('product_details/<int:pk>', product_details, name='product_details'),
    path('product_search/', product_search, name='product_search')
]