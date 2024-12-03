from django.shortcuts import redirect

def cart_counter(request):
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())
    return {"cart_count": cart_count}
