from django.contrib import admin
from .models import Product, Order, OrderItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description')  # Include the 'id' field
    search_fields = ('name', 'price')

admin.site.register(Product, ProductAdmin)



# Define InlineAdmin for OrderItem
class OrderItemInline(admin.TabularInline):  # You can use admin.StackedInline instead
    model = OrderItem
    extra = 0  # No blank rows for adding new items unless you explicitly want them
    fields = ('product', 'quantity', 'price')

# Register the main Order model with InlineAdmin for related OrderItems
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'email',
        'phone',
        'address',
        'city',
        'state',
        'postal_code',
        'payment_method',
        'total_cost',
        'created_at',
    )
    search_fields = ['email', 'phone', 'city']
    list_filter = ['created_at', 'payment_method']
    inlines = [OrderItemInline]  # Link OrderItem to Order's admin interface

# Register the Order model to the Django admin
admin.site.register(Order, OrderAdmin)