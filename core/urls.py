from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('shop', views.shop, name='shop'),
    path('shop/category/<str:name>', views.category, name='category'),
    path('shop/category/product/<str:name>', views.product, name='product'),
    path('shop/add_cart/<str:name>', views.add_cart, name='add_cart'),
    path('shop/cart', views.cart, name='cart'),
    path('shop/delete_cart/<int:id>', views.delete_cart, name='delete_cart'),
    path('shop/category/product/review/<int:id>', views.add_review, name='add_review'),
    path('shop/search', views.search_shop, name='search'),
    path('shop/category/<str:name>/search', views.search_category, name='search_category')
]