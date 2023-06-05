from django import template
from django.http import JsonResponse
from django.shortcuts import render
from account.models import Shares, Order
from django.contrib import messages

from json import JSONDecodeError
from django.http import JsonResponse
from account.serializers import SharesSerializer, OrderSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from requests.exceptions import ConnectionError


from datetime import date, timedelta
from dotenv import load_dotenv
import os
load_dotenv()

import requests
import json

class SharesView(ListModelMixin,
        RetrieveModelMixin, 
        viewsets.GenericViewSet):
        queryset = Shares.objects.all()
        serializer_class = SharesSerializer
        print(queryset)
        print(serializer_class)

class OrdersView(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    # permission_classes = [permissions.IsAdminUser]
    # permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    print(queryset)
    print(serializer_class)

# home view
def home(request):
    stocks = {}
    key = os.environ.get('API_KEY')
    company = Shares.objects.all().values()
    print(company)
    news = []
    print("Getting API Data")
    for stock in company:
    #     company = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={stock}&token={key}')
        ticker = stock['ticker']
        data = None
        try:
            data = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={key}', timeout=1000)
            data = json.loads(data.text)
            if stock['c'] != float(data['c']) or stock['h'] != float(data['h']) or stock['l'] != float(data['l']) or stock['c'] != float(data['d']):
                Shares.objects.filter(id=stock['id']).update(c=data['c'], h=data['h'], l=data['l'], d=data['d'])
                print('price update ...')
        except ConnectionError as e:    # This is the correct syntax
            data = Shares.objects.filter(id=stock['id']).values()
            # print(e)
        
        print(data, '----------')

        share_data = {**stock, **data}
        stocks[ticker] = share_data
        extras = requests.get(f'https://finnhub.io/api/v1/company-news?symbol={ticker}&from={date.today()}&to={date.today()}&token={key}').json()
        if extras:
            print(extras[0])
            news.append(extras[0])

    print(stocks)
    context = {
        'stocks': stocks,
        'extras': news
    }

    return render(request, 'home.html', context)


def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)

# search view
def search(request):
    if request.method == 'POST':
        share_name = request.POST.get('ticker')
        print(share_name)
        stocks = dict()
        key = os.environ.get('API_KEY')
        try:
            company = Shares.objects.filter(name__icontains=share_name).values()
            print(company)
        except:
            company = []
        print("Getting API Data")
        for stock in company:
            ticker = stock['ticker']
            data = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={key}')
            data = json.loads(data.text)
            share_data = {**stock, **data}
            stocks[ticker] = share_data

        print(stocks)
        context = {
            'stocks': stocks
        }
        if not stocks:
            messages.error(request, "No records are available..")
        return render(request, 'search.html', context)
    else:
        return render(request, "search.html", {})