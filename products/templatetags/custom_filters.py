from django import template
from products.models import Product

register = template.Library()

@register.filter
def get_item_name(products, product_id):
    """Retrieve product name by ID."""
    try:
        return products.get(id=product_id).name
    except Product.DoesNotExist:
        return "Unknown Product"

@register.filter
def get_item_price(products, product_id):
    """Retrieve product price by ID."""
    try:
        return products.get(id=product_id).price
    except Product.DoesNotExist:
        return 0.00

@register.filter
def get_item_image(products, product_id):
    """Retrieve product image URL by ID."""
    try:
        return products.get(id=product_id).image.url
    except Product.DoesNotExist:
        return ""
