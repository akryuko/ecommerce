from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def home(request):
    # You can select featured products or just show all products
    products = Product.objects.all()[:6]  # Display top 6 products for now (you can adjust this)
    return render(request, 'products/home.html', {'products': products})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


# View cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'products/cart.html', {'cart': cart})

# Add to cart
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    # Example logic: Add the product to the cart (using session for simplicity)
    cart = request.session.get('cart', [])
    cart.append({'product_id': product.id, 'name': product.name, 'price': product.price, 'quantity': 1})
    request.session['cart'] = cart
    
    return redirect('home')  # Redirect back to the home page after adding to cart



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
