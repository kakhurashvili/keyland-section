import re
from django.contrib import messages
from django.shortcuts import render, redirect
from UserProfile import models
from datetime import datetime, timedelta, timezone, date

from UserProfile.models import Address , EarningPoint
from .forms import CreateUserForm
from storeapp.models import Cart
from django.contrib.auth import authenticate, login, logout
from storeapp.forms import AddressForm
# from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('account')  # Redirect the user to the account page if already authenticated

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Account Created! You can Login')
            return redirect('signin')

    context = {'form': form}
    return render(request, 'UserProfile/signup.html', context)

def signin(request):

    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            cart.owner = request.user.customer
            cart.save()
            return redirect('checkout')
           
        else:
            messages.info(request, 'Invalid credentials')
            
    
    print(cart.owner)
    context = {'cart':cart}
    return render(request, 'UserProfile/login.html', context)

@login_required(login_url='account')
def changeAddress(request):
    customer = request.user.customer
    address = Address.objects.get(customer=customer)
    form = AddressForm(instance=address)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.customer = customer
            new_address.save()
            return redirect('checkout')
    context = {'form':form}
    return render(request, 'UserProfile/updateaddress.html', context)
    

def signout(request):
    logout(request)
    return redirect('index')


from decimal import Decimal  # Add this import statement

@login_required
def earning_points(request):
    customer = request.user
    earning_points = EarningPoint.get_customer_earning_points(customer)
    # Calculate today's points for the customer
    today_points = EarningPoint.objects.filter(customer_point=customer, date=date.today()).values_list('points', flat=True).first()

    total_balance = EarningPoint.objects.filter(customer_point=customer).aggregate(total_balance=models.Sum('balance'))['total_balance']
    balance_dollars = Decimal(total_balance / 100) if total_balance is not None else Decimal(0)
    print('today_points',today_points)
    context = {
        'earning_points': earning_points,
        'today_points': today_points,

        'total_balance': total_balance,
        'balance_dollars':balance_dollars
    }
    
    return render(request, 'storeapp/earning_points.html', context)









