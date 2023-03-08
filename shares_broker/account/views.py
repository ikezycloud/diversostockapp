from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import SignUpForm, SignInForm, ProfileForm
from .models import Order, Shares, Profile

import json
import requests
from django.core.serializers.json import DjangoJSONEncoder

from dotenv import load_dotenv
import os
load_dotenv()

# Get the current exchange rate for British Pounds
def get_excr(pr):
    res = requests.request("GET", f"https://v6.exchangerate-api.com/v6/6036df45f3f882e9f2032fe0/latest/USD").json()
    if res['result'] == 'success':
        return res['conversion_rates']["GBP"] * pr
    else:
        return pr * 0.8322

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})
 
def login_view(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            login(request, user)
            messages.success(request, 'Logged in Successfully')
            return redirect('home')
    else:
        form = SignInForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('account:login')

# Edit Profile View
def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('account:profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = ProfileForm(instance=user)
        return render(request, 'account/profile.html', context={'form': form})

    return redirect("home")


def buying(request):
    key = os.environ.get('API_KEY')
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.user.username)
            data = request.POST
            ticker = data.get("ticker", "0")
            print(type(ticker))
            quantity = float(data.get("quantity", "0"))
            print(type(quantity))
            user_id = request.user.id
            customer = Profile.objects.get(user=user_id)
            print(type(customer))
            share = Shares.objects.get(ticker=ticker)
            share_data = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={key}')
            share_data = json.loads(share_data.text)
            share_price = share_data['c']
            try:
                order = Order.objects.get(customer=customer, shares=share)
            except Order.DoesNotExist:
                order = None
                
            print(order)
            if not order:
                print('in if statement --------')
                print(share.name)
                order = Order(customer=customer, shares=share, quantity=quantity, price=share_price)
            else:
                print('else -----------')
                order.quantity += quantity
                order.price = share_price

            excr = get_excr(share_price * quantity)
            print(excr)
            customer.balance -= excr
            customer.save()
            share.no_of_shares -= quantity
            share.save()
            order.save()
            
            messages.success(request, f'You have bought ({quantity}) Shares of {ticker}. Successfully!')
            return redirect('home')
    else:
        messages.error(request, 'To Buy a Share, Please Login First!', extra_tags='danger')
        return redirect('account:login')

# To place the unique user's shares to their unique dashboard 
def dashboard(request, username):
    user_id = request.user.id
    print(user_id)
    data = Order.objects.filter(customer=user_id)
    orders = {}
    # print(context)
    for order in data:
        ticker = order.shares.ticker
        logo = Shares.objects.get(ticker=ticker).logo
        sdata = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={os.environ.get("API_KEY")}')
        sdata = json.loads(sdata.text)
        temp = {
            'username': order.customer.user.username,
            'ticker': ticker,
            'logo': logo,
            'quantity': order.quantity,
            'price': sdata['c'],
            'high': sdata['h'],
            'low': sdata['l'],
            'change': sdata['d'],
        }
        orders[ticker] = temp
    
    print(orders)
    context = {
        "orders": orders
    }
    if not orders:
        messages.error(request, "No Shares are available..")
    return render(request, 'account/dashboard.html', context)

def selling(request):
    key = os.environ.get('API_KEY')
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.user.username)
            data = request.POST
            ticker = data.get("ticker", "0")
            quantity = float(data.get("quantity", "0"))
            print(type(quantity))
            user_id = request.user.id
            customer = Profile.objects.get(user=user_id)
            print(type(customer))
            share = Shares.objects.get(ticker=ticker)

            share_data = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={key}')
            share_data = json.loads(share_data.text)
            share_price = share_data['c']
            
            order = Order.objects.get(customer=customer, shares=share)
            print(order)
            order.quantity -= quantity
            
            excr = get_excr(share_price * quantity)
            print(excr)
            customer.balance += excr
            customer.save()
            share.no_of_shares += quantity
            share.save()
            order.save()
                
            messages.success(request, f'You have sell ({quantity}) Shares of {ticker}. Successfully!')
            return redirect('home')
    else:
        messages.error(request, 'To Access this page Login First', extra_tags='danger')
        return redirect('account:login')