from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Product, Cart, CartItem, Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal
from django.http import JsonResponse
from .forms import RegistrationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F
from django.contrib.auth import login
from .forms import ProfileForm
from .models import Profile


def home(request):
    # Get the sorting parameter from the request
    sort_by = request.GET.get('sort', 'name')  # Default to sorting by name
    allowed_sorting = {
        'name': 'name',
        'name_desc': '-name',
        'price': F('price').asc(),
        'price_desc': F('price').desc(),
    }
    sort_criteria = allowed_sorting.get(sort_by, 'name')

    # Get the search query from the request
    search_query = request.GET.get('q', '')  # Default to empty string if no search query

    # Query products, apply sorting and search filter
    products = Product.objects.all()
    
    if search_query:
        # Filter products by name (case-insensitive search)
        products = products.filter(name__icontains=search_query)

    # Apply sorting
    products = products.order_by(sort_criteria)

    # Get the cart items
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    cart_count = sum(cart.get(product.id, 0) for product in products)

    # Apply pagination
    paginator = Paginator(products, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # Pass the context to the template
    context = {
        'products': products,
        'cart_count': cart_count,
        'sort_by': sort_by,  # Pass the current sorting method
        'search_query': search_query,  # Pass the search query to maintain it in the form
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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})





def update_cart(request, product_id):
    """Update item quantity in the cart."""
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    # Check for actions from POST request
    action = request.POST.get('action')
    if product_id_str in cart:
        if action == 'increase':
            cart[product_id_str] += 1
        elif action == 'decrease':
            if cart[product_id_str] > 1:
                cart[product_id_str] -= 1
            else:
                del cart[product_id_str]
        elif action == 'remove':
            del cart[product_id_str]

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
    # Handle guest checkout scenario
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # Process guest checkout
            contact_first_name = request.POST.get('first_name')
            contact_last_name = request.POST.get('last_name')
            contact_email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            payment_method = request.POST.get('payment_method')

            # Decode cart data
            cart_data = request.POST.getlist('cart_data')
            parsed_cart_data = {}
            for data in cart_data:
                try:
                    product_id, quantity = map(int, data.split('-'))
                    parsed_cart_data[product_id] = quantity
                except ValueError:
                    continue  # Skip invalid entries

            # Calculate total cost from the decoded cart data
            total_cost = 0
            for product_id, quantity in parsed_cart_data.items():
                try:
                    product = Product.objects.get(id=product_id)
                    total_cost += product.price * quantity
                except Product.DoesNotExist:
                    continue  # Skip invalid products

            # Create order for guest user
            order = Order.objects.create(
                first_name=contact_first_name,
                last_name=contact_last_name,
                email=contact_email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code,
                payment_method=payment_method,
                total_cost=total_cost,
            )

            request.session['order_id'] = order.id  # Save the order_id in session


            # Create OrderItems
            for product_id, quantity in parsed_cart_data.items():
                try:
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )
                except Product.DoesNotExist:
                    continue  # Skip invalid items

            # Clear the session cart after order creation
            request.session['cart'] = {}
            request.session.modified = True

            # Redirect guest to account creation prompt
            return redirect('account_creation_prompt', order_id=order.id)
        else:
            # Display checkout page for guests
            cart = request.session.get('cart', {})
            cart_items = []
            total_cost = 0
            for product_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'total_price': product.price * quantity,
                    })
                    total_cost += product.price * quantity
                except Product.DoesNotExist:
                    continue  # Skip invalid products

            return render(request, 'products/checkout.html', {
                'cart_items': cart_items,
                'total_cost': total_cost,
            })

    else:
        # Authenticated user checkout process
        if request.method == 'POST':
            # Process order creation for authenticated user
            contact_first_name = request.POST.get('first_name')
            contact_last_name = request.POST.get('last_name')
            contact_email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postal_code = request.POST.get('postal_code')
            payment_method = request.POST.get('payment_method')

            # Decode cart data
            cart_data = request.POST.getlist('cart_data')
            parsed_cart_data = {}
            for data in cart_data:
                try:
                    product_id, quantity = map(int, data.split('-'))
                    parsed_cart_data[product_id] = quantity
                except ValueError:
                    continue  # Skip invalid entries

            # Calculate total cost from the decoded cart data
            total_cost = 0
            for product_id, quantity in parsed_cart_data.items():
                try:
                    product = Product.objects.get(id=product_id)
                    total_cost += product.price * quantity
                except Product.DoesNotExist:
                    continue  # Skip invalid products

            # Create order for authenticated user
            order = Order.objects.create(
                user=request.user,
                first_name=contact_first_name,
                last_name=contact_last_name,
                email=contact_email,
                phone=phone,
                address=address,
                city=city,
                state=state,
                postal_code=postal_code,
                payment_method=payment_method,
                total_cost=total_cost,
            )

            request.session['order_id'] = order.id  # Save the order_id in session


            # Create OrderItems for each product in the cart
            for product_id, quantity in parsed_cart_data.items():
                try:
                    product = Product.objects.get(id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )
                except Product.DoesNotExist:
                    continue  # Skip invalid items

            # Clear the session cart after order creation
            request.session['cart'] = {}
            request.session.modified = True

            # Redirect authenticated user to success page
            return redirect('order_success')

        else:
            # Show the checkout page for authenticated users
            cart = request.session.get('cart', {})
            cart_items = []
            total_cost = 0
            for product_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'total_price': product.price * quantity,
                    })
                    total_cost += product.price * quantity
                except Product.DoesNotExist:
                    continue  # Skip invalid products

            return render(request, 'products/checkout.html', {
                'cart_items': cart_items,
                'total_cost': total_cost,
            })



def order_success(request):
    # Retrieve the order ID from the session
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('home')  # Redirect if no order ID found

    # Fetch the order and related order items
    order = get_object_or_404(Order, id=order_id)
    order_items = order.order_items.all()  # Use the correct related name

    return render(request, 'products/order_success.html', {
        'order': order,
        'order_items': order_items,
    })


def account_creation_prompt(request, order_id):
    # Get the order based on the provided order_id
    order = Order.objects.get(id=order_id)
    
    # Use 'order_items' to get the related items for this order
    order_items = order.order_items.all()  # 'order_items' is the related_name in the OrderItem model

    if request.method == 'POST':
        # Create the user account using the form
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user and log them in
            user = form.save()
            login(request, user)

            # Link the guest order to the new user account
            order.user = user
            order.save()

            # Redirect to order success page or dashboard
            return redirect('order_success')

    else:
        form = UserCreationForm()

    # Render the account_creation_prompt page with the order and items context
    context = {
        'order': order,
        'order_items': order_items,
        'form': form,
    }
    return render(request, 'products/account_creation_prompt.html', context)



def faq(request):
    faqs = [
        {
            "question": "What is My Ecommerce Store?",
            "answer": "My Ecommerce Store is your one-stop-shop for the freshest and best-quality food items delivered right to your doorstep."
        },
        {
            "question": "How can I place an order?",
            "answer": "Browse through our products, add your desired items to the cart, and proceed to checkout to place an order."
        },
        {
            "question": "What payment methods are accepted?",
            "answer": "We accept credit/debit cards, PayPal, and other secure payment options."
        },
        {
            "question": "Can I cancel or modify my order?",
            "answer": "Yes, you can modify or cancel your order before it is shipped. Please contact customer support for assistance."
        },
        {
            "question": "Do you offer same-day delivery?",
            "answer": "Yes, we offer same-day delivery for orders placed before 12 PM in select locations."
        },
        {
            "question": "How can I track my order?",
            "answer": "You can track your order using the tracking link sent to your email after the order is confirmed."
        },
        {
            "question": "What is your return policy?",
            "answer": "We offer a hassle-free return policy for damaged or incorrect items. Contact us within 24 hours of delivery."
        }
    ]
    return render(request, 'products/faq.html', {'faqs': faqs})


def about(request):
    context = {
        'store_description': "Welcome to My Ecommerce Store! We specialize in providing high-quality, fresh food products straight to your door. Our mission is to make online grocery shopping easy, convenient, and enjoyable. From farm-fresh produce to your favorite snacks, we’ve got it all.",
        'image_url': 'images/about.webp'  # Path to the static image
    }
    return render(request, 'products/about.html', context)


def terms(request):
    context = {
        'title': "Terms and Conditions",
        'content': """
            Welcome to My Ecommerce Store! By using our website, you agree to the following terms and conditions:
            
            1. **Use of Website**: You agree to use this website for lawful purposes only. 
            
            2. **Privacy**: We are committed to protecting your privacy. Please review our Privacy Policy for details.
            
            3. **Product Availability**: All products are subject to availability. Prices and availability may change without notice.
            
            4. **Payments**: All payments must be made in full before orders are processed.
            
            5. **Shipping and Delivery**: We aim to deliver your orders on time, but delays may occur due to unforeseen circumstances.
            
            6. **Returns and Refunds**: Please refer to our Returns Policy for information on returns and refunds.
            
            7. **Intellectual Property**: All content, logos, and trademarks are the property of My Ecommerce Store.
            
            8. **Limitation of Liability**: We are not liable for any indirect or consequential losses arising from the use of our website.
            
            9. **Changes to Terms**: We may update these terms and conditions from time to time. It is your responsibility to check this page regularly.
            
            Thank you for choosing My Ecommerce Store!
        """
    }
    return render(request, 'products/terms.html', context)



@login_required
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')  # Fetch user's orders
    return render(request, 'products/user_profile.html', {'user': user, 'orders': orders})