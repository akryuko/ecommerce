from django import template
from products.models import Product
from urllib.parse import urlencode, parse_qs, urlparse


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


@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return 0  # Return 0 if there's an error
    

@register.filter
def remove_query_param(query_string, param_to_remove):
    query_params = parse_qs(query_string)
    if param_to_remove in query_params:
        del query_params[param_to_remove]
    return urlencode(query_params, doseq=True)