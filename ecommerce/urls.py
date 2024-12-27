"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from products.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page at the root '/'
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', register, name='register'),  # Direct URL for register
    path('cart/', view_cart, name='cart'),  # Direct URL for cart
    path('product_list/', product_list, name='product_list'),  # Direct URL for product list
    path('auth/', include('django.contrib.auth.urls')),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('product_detail/<int:product_id>/', product_detail, name='product_detail'),  # Add this line
    path('update_cart/<int:product_id>/', update_cart, name='update_cart'),
    path('reduce_from_cart/<int:product_id>/', reduce_from_cart, name='reduce_from_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('get_cart_count/', get_cart_count, name='get_cart_count'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    path('faq/', faq, name='faq'),
    path('about/', about, name='about'),
    path('terms/', terms, name='terms'),
    path('account/creation_prompt/<int:order_id>/', account_creation_prompt, name='account_creation_prompt'),
    path('profile/', user_profile, name='user_profile'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
