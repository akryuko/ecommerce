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

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_cost': total_price,
    })

@login_required
def add_to_cart(request, product_id):
    # Get the current cart from session or create an empty cart if not exist
    cart = request.session.get('cart', {})

    print(f"Cart before adding: {cart}")  # Debugging line

    # Ensure all values in the cart are integers (in case there was an invalid entry)
    cart = {key: int(value) if isinstance(value, int) else 0 for key, value in cart.items()}

    # Convert product_id to string (to handle it as a key in the cart dictionary)
    product_id_str = str(product_id)

    try:
        # Check if the product exists
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        # If the product doesn't exist, return an error
        return JsonResponse({'error': 'Product not found'}, status=404)

    # Update the cart count for the product
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    
    # Save the updated cart to the session
    request.session['cart'] = cart
    request.session.modified = True  # Ensure the session is marked as modified for saving

    # Get the total count of items in the cart
    cart_count = sum(cart.values())

    print(f"Cart after adding: {cart}")  # Debugging line


    # Return the cart count as a JSON response
    return JsonResponse({'cart_count': cart_count})



def reduce_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] -= 1
        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

def update_cart(request, product_id):
    """Update item quantity or remove item from the cart."""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    action = request.POST.get('action')
    if product_id_str in cart:
        if action == 'increase':
            cart[product_id_str] += 1
        elif action == 'decrease':
            if cart[product_id_str] > 1:
                cart[product_id_str] -= 1
            else:
                del cart[product_id_str]
    
    request.session['cart'] = cart
    return JsonResponse({'cart_count': sum(cart.values())})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
    
    return JsonResponse({'cart_count': sum(cart.values())})


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


def update_cart(request, product_id):
    """Update item quantity or remove item from the cart."""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    # Check for actions from POST request
    action = request.POST.get('action')
    if product_id_str in cart:
        if action == 'decrease':
            if cart[product_id_str] > 1:
                cart[product_id_str] -= 1
            else:
                del cart[product_id_str]  # Remove item if quantity is 0
        elif action == 'remove':
            del cart[product_id_str]  # Remove item completely

    # Save updated cart in session
    request.session['cart'] = cart
    return redirect('cart')  # Redirect back to the Cart page


def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.all()
    
    # Prepare data for the cart items
    cart_items = []
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity,
            })
        except Product.DoesNotExist:
            continue

    # Pass the items and total cost to the template
    total_cost = sum(item['total_price'] for item in cart_items)
    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
    })


def get_cart_count(request):
    # Assuming the cart is stored in the session
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())  # Sum the quantities of all items in the cart
    return JsonResponse({'cart_count': cart_count})



def checkout(request):
    # Fetch cart data to display on the checkout page
    cart_items = []  # Replace with actual logic to fetch cart items
    total_cost = 0  # Replace with logic to calculate total cost

    # Render the checkout template
    return render(request, 'products/checkout.html', {'cart_items': cart_items, 'total_cost': total_cost})

