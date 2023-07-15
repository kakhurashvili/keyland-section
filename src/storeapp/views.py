from django.shortcuts import render, redirect
from django.conf import settings
from storeapp.admin import CartitemsAdmin
from storeapp.utils import get_client_ip
from .models import Banner, InfoBox, Product, Cart, Cartitems, Category, SavedItem, Main_Category, Sub_Category, Visitor ,SavedItem ,Banner_second
from django.http import JsonResponse
from django.core import serializers
from .forms import AddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import uuid
from UserProfile.models import Address, EarningPoint
from .forms import UpdateUserForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from decimal import Decimal
import requests

def chat(request):
    return render(request, 'storeapp/chat.html')

def get_instagram_photos(request):
    url = f"https://api.instagram.com/v1/users/self/media/recent/?access_token={settings.INSTAGRAM_ACCESS_TOKEN}"
    print('url',url)
    response = requests.get(url)
    data = response.json()
    media = data['data']
    return render(request, 'media.html', {'media': media})


def index(request, main_category_slug=None, category_slug=None):
    session_id = request.session.get('nonuser')

    # Check if the cookie has been accepted
    cookie_accepted = request.COOKIES.get('cookieAccepted', False)

    # Get user's IP address
    ip_address = get_client_ip(request)

    # Send request to ipstack API
    access_key = ""  # Replace with your actual access key
    api_url = f'http://api.ipstack.com/{ip_address}?access_key={access_key}'
    response = requests.get(api_url)

    if response.status_code == 200:
        # Extract location data from API response
        location_data = response.json()
        country_code = location_data.get('country_code')
        region_name = location_data.get('region_name')
        city = location_data.get('city')
        ip = location_data.get('ip')
    else:
        # Default values if API request fails
        country_code = 'N/A'
        region_name = 'N/A'
        city = 'N/A'

    # Save visitor's data to the database
    # Check if IP address exists in Visitor model
    visitor = Visitor.objects.filter(ip_address=ip_address).first()
    if not visitor:
        # IP address does not exist, create a new Visitor object
        visitor = Visitor.objects.create(ip_address=ip_address, country=country_code)

    if session_id:
        try:
            cart = Cart.objects.get(session_id=session_id, completed=False)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(session_id=session_id, completed=False)
    else:
        session_id = str(uuid.uuid4())
        request.session['nonuser'] = session_id
        cart = Cart.objects.create(session_id=session_id, completed=False)

    cartitems = cart.cartitems_set.all()
    featured_categories = Main_Category.objects.filter(featured_product__isnull=False)
    print('featured_categories',featured_categories)
    featured_products = []
    print('featured_products',featured_products)

    for category in featured_categories:
        main_category = category.title
        products = category.featured_product.sub_category.products.all()
        
        for product in products:
            product_details = {
                'name': product.name,
                'category': main_category,
                'image_url': product.image.url,
                'price': product.price,
                'description': product.description
                # Add any additional fields you want to retrieve
            }
            featured_products.append(product_details)

    top_deals = Product.objects.filter(top_deal=True)

    print('top_deals',top_deals)
    main_category = None
    category = None

    if main_category_slug and category_slug:
        main_category = get_object_or_404(Main_Category, slug=main_category_slug)
        category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.all()
    banners = Banner.objects.all()
    banner_second = Banner_second.objects.first()
    info_boxes = InfoBox.objects.all()
    print('banner_second',banner_second)
    context = {
        'top_deals': top_deals,
        'featured_categories': featured_categories,
        'banners':banners,
        'banner_second':banner_second,
        'info_boxes':info_boxes,
        'products': products,
        'cart': cart,
        'cartitems': cartitems,
        'main_category': main_category,
        'category': category,
        'country_code': country_code,
        'region_name': region_name,
        'city': city,
        'ip': ip,
        'cookie_accepted': cookie_accepted  # Pass the cookie status to the template
    }

    response = render(request, 'storeapp/index.html', context)

    # Set the cookie if it hasn't been accepted
    if not cookie_accepted:
        response.set_cookie('cookieAccepted', False)

    return response




    
def category(request, main_category_slug=None, category_slug=None, sub_category_slug=None):
    if main_category_slug is None:
        main_categories = Main_Category.objects.all()
        products = Product.objects.all()  # Retrieve all products
        context = {
            'main_categories': main_categories,
            'products': products,
        }
        return render(request, 'storeapp/category.html', context)

    main_category = get_object_or_404(Main_Category, slug=main_category_slug)
    category = None
    sub_category = None
    products = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, main_category=main_category)
        if sub_category_slug:
            sub_category = get_object_or_404(Sub_Category, slug=sub_category_slug, category=category)
            products = sub_category.products.all()
        else:
            sub_category_ids = Sub_Category.objects.filter(category=category).values_list('id', flat=True)
            products = Product.objects.filter(sub_category__in=sub_category_ids)
    else:
        category_ids = Category.objects.filter(main_category=main_category).values_list('id', flat=True)
        sub_category_ids = Sub_Category.objects.filter(category_id__in=category_ids).values_list('id', flat=True)
        products = Product.objects.filter(sub_category__in=sub_category_ids)

    main_categories = Main_Category.objects.filter(slug=main_category_slug)  # Fetch only the current main category

    context = {
        'category': category,
        'main_category': main_category,
        'sub_category': sub_category,
        'products': products,
        'main_categories': main_categories,
    }

    return render(request, 'storeapp/category.html', context)




def detail(request, slug, sku=None):
    product = get_object_or_404(Product, slug=slug)

    if sku and product.sku != sku:
        product = get_object_or_404(Product, sku=sku)

    session_id = request.session.get('nonuser')
    if session_id:
        try:
            cart = Cart.objects.get(session_id=session_id, completed=False)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(session_id=session_id, completed=False)
    else:
        cart = None

    similar_products = Product.objects.filter(sub_category__category=product.sub_category.category).exclude(slug=product.slug)
    counter = 0

    try:
        saveitem = SavedItem.objects.get(product=product)
        counter = 1
    except SavedItem.DoesNotExist:
        saveitem = None
    except SavedItem.MultipleObjectsReturned:
        saveitem = None  # or handle the multiple objects scenario accordingly

    recently_viewed_products = None
    if 'recently_viewed' in request.session:
        if slug in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(slug)

        recently_viewed_products = Product.objects.filter(slug__in=request.session['recently_viewed'])
        request.session['recently_viewed'].insert(0, slug)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [slug]

    request.session.modified = True
    percentage = int((Decimal(product.old_price) - product.price) / Decimal(product.old_price) * 100)

    inventory_total = product.inventory
    
    sub_category = product.sub_category
    category = sub_category.category
    main_category = category.main_category
    cartitems = cart.cartitems_set.all() if cart else []
    context = {
        'product': product,
        'cart': cart,
        'saveitem': saveitem,
        'counter': counter,
        'recently_viewed_products': recently_viewed_products,
        'similar_products': similar_products,
        'inventory_total': inventory_total,
        'sku': product.sku,
        'cartitems': cartitems,
        'percentage': percentage,
        'sub_category': sub_category,
        'main_category': main_category,
        'category': category,

    }

    return render(request, 'storeapp/detail.html', context)






def product_quick_view(request, slug, sku):
    # Retrieve the product based on the slug and sku
    product = get_object_or_404(Product, slug=slug, sku=sku)
    percentage = int((Decimal(product.old_price) - product.price) / Decimal(product.old_price) * 100)

    context = {
        'product': product,
        'percentage':percentage,
    }
    return render(request, 'storeapp/ajax/product-quick-view.html', context)


def cart(request):
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems = cart.cartitems_set.all()
    context = {'cart':cart, 'cartitems': cartitems}
    return render(request, 'storeapp/cart.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def updateCart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pro_id = data['p_id']
            action = data['action']
            
            product = Product.objects.get(id=pro_id)
            cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
            cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)
            
            if action == 'add':
                cartitems.quantity += 1
            cartitems.save()
            
            msg = {
                'num_of_items': cart.num_of_items
            }
            return JsonResponse(msg)
        
        except (KeyError, ValueError, Product.DoesNotExist, Cart.DoesNotExist):
            # Handle specific exceptions here, e.g., return an error message or redirect
            return JsonResponse({'error': 'Invalid data or resource not found'}, status=400)

        except Exception as e:
            # Handle any other exceptions and log the error
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def updateQuantity(request):
    data = json.loads(request.body)
    product_id = data['id']
    quantity = data['qty']
    price = data['product_price']
    product = Product.objects.get(id=product_id)
   
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)

 # Check if the updated quantity exceeds the available inventory
    if int(quantity) > product.inventory:
        # Add an error message to the Django messages framework
        # Return an error response indicating the failure
        return JsonResponse({'error': 'Quantity exceeds available inventory.'}, status=400)
    
    cartitems.quantity = quantity

    if int(cartitems.quantity) == 0:
        cartitems.delete()
    cartitems.save()
    msg = {
        'num': cart.num_of_items,
        'qty': quantity,
        'price': price,
        'total': cart.cart_total
    }
   
    return JsonResponse(msg , safe=False)

def deleteCartitems(request):
    data = json.loads(request.body)
    # customer = request.user.customer
    product_id = data['id']
    product = Product.objects.get(id=product_id)
    # cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
    # cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)
    
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems = Cartitems.objects.filter(product=product, cart=cart)
    print(cartitems)
    cartitems.delete()
    # cartitems.save()    # if cartitems:
    #     print('mmmdkd')
    #     cartitems.delete()
    #     cartitems.save()
    return JsonResponse(str(cartitems), safe=False)
from django.db.models import F, Sum
from storeapp.models import Product, Cartitems
def calculate_total_price():
    # Retrieve the cart items from the database
    cart_items = Cartitems.objects.all()

    # Calculate the total price using the product prices and quantities
    total_price = cart_items.aggregate(
        total=Sum(F('product__old_price') * F('quantity'))
    )['total'] or 0

    return total_price
from django.shortcuts import render, redirect
from UserProfile import models

from UserProfile.models import EarningPoint
from django.contrib import messages

import base64
import hashlib
import hmac

from django.shortcuts import render, redirect
from UserProfile.models import  Address, EarningPoint
from django.contrib import messages
import requests

@login_required(login_url='signin')
def checkout(request):
    form = None
    cart = Cart.objects.get(session_id=request.session['nonuser'], completed=False)
    cartitems = cart.cartitems_set.all()
    customer = request.user.customer
    customer_address = Address.objects.filter(customer=customer)
    customer = request.user
    earning_points = EarningPoint.objects.filter(customer_point=customer).first()
    balance = earning_points.balance if earning_points else 0
    total_balance = EarningPoint.objects.filter(customer_point=customer).aggregate(total_balance=models.Sum('balance'))['total_balance']
    balance_dollars = Decimal(total_balance / 100) if total_balance is not None else Decimal(0)
    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Retrieve form data and process the shipping information
            # ...
            
            # Handle the use_points checkbox
            use_points = request.POST.get('use_points')
            if use_points:
                # Deduct the points from the balance
                points_to_deduct = cart.cart_total  # Assuming 1 point is equal to 1 unit of currency (e.g., dollar)
                if points_to_deduct > balance:
                    # Adjust the points to deduct if the balance is insufficient
                    points_to_deduct = balance

                # Calculate the deduction amount
                deduction_amount = Decimal(points_to_deduct / 100) if points_to_deduct is not None else Decimal(0)

                # Update the balance by deducting the points
                earning_points.balance -= deduction_amount
                earning_points.save()

            # Make a request to Unipay.com API to create an order
            create_order_url = "https://apiv2.unipay.com/custom/checkout/v1/createorder"
            secret_key = "I3Rz8QXBVPofKtucsenkW7g2n7aDwqBg"
            total_amount = cart.cart_total
            print('create_order_url',create_order_url)
            # Create the payload to send to Unipay.com API
            payload = {
                "Hash": "<calculate-hash-value>",
                "Amount": total_amount,
                "OrderID": str(cart.cart_id),
                # Include other required parameters as per Unipay.com API documentation
            }

            # Make a POST request to create the order
            response = requests.post(create_order_url, data=payload)

            if response.status_code == 200:
                # Order creation successful
                order_data = response.json()
                payment_url = order_data["payment_url"]

                # Store the Unipay transaction ID in the cart
                cart.unipay_transaction_id = order_data["transaction_id"]
                cart.save()

                return redirect(payment_url)
            else:
                # Order creation failed
                messages.error(request, 'Failed to create order. Please try again later.')

            # Redirect the user to the checkout page
            return redirect('checkout')
    else:
        form = AddressForm()
    
    context = {
        'form': form,
        'cart': cart,
        'cartitems': cartitems,
        'customer_address': customer_address,
        'balance': balance,
        'total_balance': total_balance,
        'balance_dollars': balance_dollars
    }
    return render(request, 'storeapp/checkout.html', context)

def checkout_success(request):
    return render(request, 'storeapp/checkout_success.html')

# def calculate_hash(secret_key, order_id, order_total):
#     hash_string = f"{order_id}{order_total}{secret_key}"
#     digest = hmac.new(
#         secret_key.encode('utf-8'),
#         hash_string.encode('utf-8'),
#         hashlib.sha256
#     ).digest()
#     hash_value = base64.b64encode(digest).decode('utf-8')
#     return hash_value


@login_required(login_url='signin')
def account(request):
        ##point##
    customer = request.user
    earning_points = EarningPoint.get_customer_earning_points(customer)
    total_balance = EarningPoint.objects.filter(customer_point=customer).aggregate(total_balance=models.Sum('balance'))['total_balance']
    balance_dollars = Decimal(total_balance / 100) if total_balance is not None else Decimal(0)

    print('total_balance',earning_points)
    customer = request.user.customer
    address = Address.objects.filter(customer=customer)
    orders = Cart.objects.filter(owner=customer)
    print('request.user.customer',customer)

    print('orders',orders)
    context = {
        'customer': customer, 
        'address':address,
        'orders':orders,        
        'earning_points': earning_points,
        'total_balance': total_balance,
        'balance_dollars':balance_dollars
    }
    return render(request, 'storeapp/account.html', context)



@login_required(login_url='signin')
def confirmPayment(request):
    data = json.loads(request.body)
    total = float(data['total'])
    print(total)
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    print(cart.cart_total)
    if total == cart.cart_total:
        cart.completed = True
    else:
        messages.info(request, 'There is an issue with your purchase')
    cart.save()
    return JsonResponse('it is workking', safe=False)

@login_required(login_url='signin')
def saveItems(request):
    customer = request.user.customer
    saveitems = SavedItem.objects.filter(owner=customer)
    context = {'saveitems':saveitems}
    return render(request, 'storeapp/saveitem.html', context)


@login_required(login_url='signin')
def order(request):
    customer = request.user.customer
    orders = Cart.objects.filter(owner=customer)
    print('order',orders)
    context = {'orders':orders}
    return render(request, 'storeapp/order.html', context)


@login_required(login_url='signin')
def addSavedItems(request):
    if request.method=='POST':
        saveitems = None
        customer = request.user.customer
        data = json.loads(request.body)
        print("data",data)
        counter = data['counter']
        product_id = data['d']
        print("product_id",product_id)
        product = Product.objects.get(id=product_id)
        saveitems, created= SavedItem.objects.get_or_create(owner=customer, product=product)
        saveitems.added = 1
        saveitems.save()
        
        if counter == 0:
            new_counter = 0
            saveitems = SavedItem.objects.filter(owner=customer, product=product)
            saveitems.delete()
  
    if saveitems:
        print('mmmmmm')
        new_counter = 1
    else:
        print('00000000')
        new_counter = 0
        print("jhjj",new_counter)
    return JsonResponse(new_counter, safe=False)
 
def update_user_info(request):
    customer = request.user.customer
    form = UpdateUserForm(instance=customer)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect ('account')
    context = {'form': form}
    return render(request, 'storeapp/update_user.html', context)
    

def search(request):
    query = request.GET.get('search_query')
    products = Product.objects.filter(name__icontains=query)

    context = {
        'products': products,
        'query': query,

    }
    return render(request, 'storeapp/search.html', context)

