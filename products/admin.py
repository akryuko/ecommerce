from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description')  # Include the 'id' field
    search_fields = ('name', 'price')

admin.site.register(Product, ProductAdmin)