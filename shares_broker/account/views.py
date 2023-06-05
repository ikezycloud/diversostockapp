from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import SignUpForm, SignInForm, ProfileForm, ResetPwd
from .models import Order, Shares, Profile
from django.contrib.auth import authenticate

from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import ProfileSerializer
from account.serializers import OrderSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.core.serializers import serialize


from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
import requests
from django.core.serializers.json import DjangoJSONEncoder

from dotenv import load_dotenv
import os
load_dotenv()

# This function converts a given price from USD to a specified currency using an external API. If API call is successful,
# the function returns the converted price.

def get_excr(cur, pr):
    res = requests.request("GET", f"https://v6.exchangerate-api.com/v6/6036df45f3f882e9f2032fe0/latest/USD").json()
    if res['result'] == 'success':
        return res['conversion_rates'][cur] * pr
    else:
        return pr * 0.8322

# Handles user sign-up requests. Creates a new user account and updates the user's profile with the selected currency if
# the form data is valid. Renders the sign-up form with error messages if the form data is invalid. Upon successful
# account creation, redirects the user to the login page.

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.get(user=user.id)
            profile.ucurrency = form.data['ucurrency']
            profile.save()
            print('profile updated - ', profile.ucurrency)
            token = Token.objects.create(user=user)
            print(token.key)
            # login(request, user)
            return redirect('account:login')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

# user login/authenticaion view
# Handles user login requests. If the HTTP method is POST, the function validates the sign-in form data, logs in the user
# if the form is valid, and redirects the user to the home page with a success message. If the HTTP method is not POST,
# the function renders the login page with an empty sign-in form.
#  
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

# view to logged out current user
def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('account:login')
        return redirect('account:login')
    
    return redirect('account:login')

# password reset view/method
# This function handles the password reset requests. It checks if the user is authenticated, verifies the old password,
# and updates the password with a new one. If the password reset is successful, the user is redirected to the login page;
# otherwise, error messages are displayed.

def reset_pwd(request):
    if request.method == 'POST':
        old = request.POST['old_pwd']
        print(request.user)
        if request.user.is_authenticated:
            user = authenticate(username=request.user, password=old)
            if user:
                new = request.POST['new_pwd']
                renew = request.POST['renew_pwd']
                if new == renew:
                    user.set_password(new)
                    user.save()
                    print(request.user)
                    messages.success(request, 'Password Updated Successgully!', extra_tags='success')
                else:
                    messages.error(request, 'New and Confirm Password dose not match', extra_tags='danger')
                    return render(request, 'account/reset_pwd.html')
            else:
                messages.error(request, 'User Authentication Error!', extra_tags='danger')
                return render(request, 'account/reset_pwd.html')
        else:
            messages.error(request, 'Please Login First!', extra_tags='danger')
    else:
        return render(request, 'account/reset_pwd.html')
    
    return redirect("account:login")

# Edit Profile View
# This view function updates user profiles on valid form submission, else re-renders the form with error messages.
# The function renders the profile form with the current user details if the HTTP method is not POST.
# If the specified user does not exist, the user is redirected to the home page.

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

class ProfileView(ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet):
        queryset = Profile.objects.all()
        serializer_class = ProfileSerializer
        print(queryset)
        print(serializer_class)


# shares buying view
# This view handles user buy orders for shares.
# If authenticated and form is valid, a new Order instance is created or an existing Order instance is updated with the new quantity and price.
# The user's balance is updated and the number of available shares is decreased.
# If the user doesn't have enough balance, an error message is displayed. If the user isn't authenticated, they're redirected to the login page.

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
            if customer.balance >= get_excr(customer.ucurrency, (share_price * quantity)):
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
                    order.save()

                excr = get_excr(customer.ucurrency, (share_price * quantity))
                print(excr)
                customer.balance -= excr
                customer.save()
                share.no_of_shares -= quantity
                share.save()
                order.save()
                
                messages.success(request, f'You have bought ({quantity}) Shares of {ticker}. Successfully!')
                return redirect('home')
            else:
                messages.error(request, "You Don't have Enough Balance to Puchase this amount of Shares!", extra_tags='danger')
                return redirect('home')
    else:
        messages.error(request, 'To Buy a Share, Please Login First!', extra_tags='danger')
        return redirect('account:login')

# user's shares dashboard view
# This function generates a dashboard view that displays a user's orders and relevant stock data.
# It retrieves the user's orders from the database, retrieves stock data from the Finnhub API for each order, and stores the data in a dictionary.
# If there are no orders, an error message is added to the response. The HTML template is rendered with the dictionary as the context.
 
def dashboard(request, username):
    user_id = request.user.id
    print(user_id)
    data = Order.objects.filter(customer=user_id)
    orders = {}
    print(data)
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

# user shares selling view
# This view handles user sell orders for shares.
# If authenticated and form is valid, an existing Order instance is updated with the new quantity and price.
# The user's balance is updated and the number of available shares is increased.
# If the user isn't authenticated, they're redirected to the login page.
# If the user doesn't have enough shares, an error message is displayed.

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
            
            excr = get_excr(customer.ucurrency, (share_price * quantity))
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