from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
from django.http import JsonResponse
from .forms import RegistrationForm


def home(request):
    # Get all products or any specific ones
    products = Product.objects.all()

    # Get the cart items (assuming you're using sessions)
    cart = request.session.get('cart', {})

    # Make sure cart is a dictionary and only contains integers as values
    if not isinstance(cart, dict):
        cart = {}

    # Sum the quantities of items in the cart
    cart_count = sum(cart.get(product.id, 0) for product in products)

    context = {
        'products': products,
        'cart_count': cart_count,  # Pass cart count to the template
    }
    return render(request, 'products/home.html', context)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity
            })
            total_price += product.price * quantity
        except Product.DoesNotExist:
            continue

    return render(request, 'products/cart.html', {'cart_items': cart_items, 'total_price': total_price})



@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart = {key: int(value) if isinstance(value, int) else 0 for key, value in cart.items()}  # Ensure valid data

    product_id_str = str(product_id)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart  # Persist cart in session
    request.session.modified = True  # Ensure session data is saved

    cart_count = sum(cart.values())

    return JsonResponse({'cart_count': cart_count})



# Remove from cart
@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = RegistrationForm()
    return render(request, 'products/register.html', {'form': form})
