from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
from django.http import JsonResponse


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


# View cart
@login_required
def view_cart(request):
    # Retrieve the current user's cart
    cart = Cart.objects.filter(user=request.user).first()
    return render(request, 'products/cart.html', {'cart': cart})


# Add to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Use session to store cart (this is just a basic example)
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1  # Increment the item count in the cart
    request.session['cart'] = cart

    # Get the cart count
    cart_count = sum(cart.values())

    return JsonResponse({'cart_count': cart_count})



# Remove from cart
@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# products/views.py
from django.shortcuts import render, redirect
from .forms import RegistrationForm

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
