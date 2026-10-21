from django.shortcuts import render,redirect
from .models import Category,Product,Order,OrderItem
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import (login as auth_login,logout,authenticate)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def home(request):
    categories = Category.objects.all()
    products = Product.objects.select_related('category').all()

    # Search products by name
    keyword = request.GET.get('q', '').strip()
    if keyword:
        products = products.filter(name__icontains=keyword)

    # Filter products by category
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'keyword': keyword,
        'selected_category': category_id,
    })

@login_required
def product_detail(request,id):
    product=get_object_or_404(Product,id=id)
    
    return render(request,'product_detail.html',{'product':product})

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    if product.stock > 0:
        current_quantity = cart.get(product_id, 0)

        if current_quantity < product.stock:
            cart[product_id] = current_quantity + 1
            request.session['cart'] = cart
            messages.success(request, 'Product added to cart!')
        else:
            messages.warning(request, 'Available stock limit reached.')
    else:
        messages.error(request, 'Product is out of stock.')

    return redirect('cart')

@login_required
def cart(request):
    cart_items = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart_items.keys())

    items = []
    total = 0

    for product in products:
        quantity = cart_items.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal

        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'items': items,
        'total': total,
    })

@login_required
def update_cart(request, id):
    if request.method == 'POST':
        cart_items = request.session.get('cart', {})
        product_id = str(id)

        product = get_object_or_404(Product, id=id)

        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity <= 0:
            cart_items.pop(product_id, None)
        elif quantity <= product.stock:
            cart_items[product_id] = quantity
        else:
            messages.warning(
                request,
                f'Only {product.stock} items are available.'
            )

        request.session['cart'] = cart_items

    return redirect('cart')

@login_required
def remove_from_cart(request, id):
    if request.method == 'POST':
        cart_items = request.session.get('cart', {})
        cart_items.pop(str(id), None)
        request.session['cart'] = cart_items
        messages.success(request, 'Product removed from cart.')

    return redirect('cart')

@login_required
def checkout(request):
    cart_data = request.session.get('cart', {})

    if not cart_data:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if not customer_name or not address:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('checkout')

        if not phone.isdigit() or len(phone) != 10:
            messages.error(request, 'Enter a valid 10-digit phone number.')
            return redirect('checkout')

        try:
            with transaction.atomic():
                product_ids = [int(pid) for pid in cart_data.keys()]

                products = list(
                    Product.objects.select_for_update().filter(
                        id__in=product_ids
                    )
                )

                product_map = {str(p.id): p for p in products}

                # Check that every cart product still exists.
                if len(product_map) != len(set(cart_data.keys())):
                    messages.error(
                        request,
                        'A product in your cart is no longer available.'
                    )
                    return redirect('cart')

                order_lines = []
                total = 0

                # Validate quantities and stock before creating the order.
                for product_id, product in product_map.items():
                    quantity = int(cart_data[product_id])

                    if quantity <= 0 or quantity > product.stock:
                        messages.error(
                            request,
                            f'Insufficient stock for {product.name}.'
                        )
                        return redirect('cart')

                    subtotal = product.price * quantity
                    total += subtotal
                    order_lines.append((product, quantity))

                order = Order.objects.create(
                    customer=request.user if request.user.is_authenticated else None,
                    customer_name=customer_name,
                    phone=phone,
                    address=address,
                    total_amount=total,
                    status='Pending'
                )

                for product, quantity in order_lines:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )

                    product.stock -= quantity
                    product.save(update_fields=['stock'])

            # Clear the cart only after the transaction succeeds.
            request.session['cart'] = {}
            request.session.modified = True

            return render(
                request,
                'order_success.html',
                {'order': order}
            )

        except (ValueError, TypeError):
            messages.error(request, 'Your cart contains invalid quantities.')
            return redirect('cart')

    # Prepare items and total for the checkout page.
    products = Product.objects.filter(id__in=cart_data.keys())
    items = []
    total = 0

    for product in products:
        quantity = int(cart_data.get(str(product.id), 0))
        subtotal = product.price * quantity
        total += subtotal

        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'checkout.html', {
        'items': items,
        'total': total,
    })

def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')
  
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            messages.error(
                request,
                'Username and password are required.'
            )

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif len(password) < 8:
            messages.error(
                request,
                'Password must be at least 8 characters.'
            )

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(
                request,
                'Registration successful! Please log in.'
            )
            return redirect('login')

    return render(request, 'register.html')

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(
            request,
            'You have logged out successfully.'
        )

    return redirect('login')

    return redirect('login')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })
    
    

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if email and '@' not in email:
            messages.error(request, 'Please enter a valid email address.')
        else:
            request.user.email = email
            request.user.save(update_fields=['email'])
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

    return render(request, 'profile.html')
