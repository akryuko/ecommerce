from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('cart/', views.view_cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('product_list/', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('product_list/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),  # Add this line
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('reduce_from_cart/<int:product_id>/', views.reduce_from_cart, name='reduce_from_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get_cart_count/', views.get_cart_count, name='get_cart_count'),


]
