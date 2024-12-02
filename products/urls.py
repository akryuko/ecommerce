from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product_list/', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('product_list/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),  # Add this line



]

