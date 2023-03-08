from django import template
from django.http import JsonResponse
from django.shortcuts import render
from account.models import Shares
from django.contrib import messages

from datetime import date, timedelta
from dotenv import load_dotenv
import os
load_dotenv()

import requests
import json

# stocks_list = ['AAPL', 'MSFT', 'TSLA', 'IBM', 'UBER', 'DIS', 'SBUX']
# stocks_list = ['AAPL', 'TSLA', 'IBM']
# def get_data():
#     val = {'AAPL': {'no_of_shares': 10, 'country': 'US', 'currency': 'USD', 'exchange': 'NASDAQ NMS - GLOBAL MARKET', 'finnhubIndustry': 'Technology', 'ipo': '1980-12-12', 'logo': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/AAPL.svg', 'marketCapitalization': 2434206.533142, 'name': 'Apple Inc', 'phone': '14089961010.0', 'shareOutstanding': 15821.9, 'ticker': 'AAPL', 'weburl': 'https://www.apple.com/', 'c': 151.36, 'd': -2.49, 'dp': -1.6185, 'h': 153.77, 'l': 151, 'o': 152.12, 'pc': 153.85, 't': 1676389539}, 
#             'MSFT': {'no_of_shares': 10,'country': 'US', 'currency': 'USD', 'exchange': 'NASDAQ NMS - GLOBAL MARKET', 'finnhubIndustry': 'Technology', 'ipo': '1986-03-13', 'logo': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/MSFT.svg', 'marketCapitalization': 2019652.8773719994, 'name': 'Microsoft Corp', 'phone': '14258828080.0', 'shareOutstanding': 7443.8, 'ticker': 'MSFT', 'weburl': 'https://www.microsoft.com/en-us', 'c': 270.13, 'd': -1.19, 'dp': -0.4386, 'h': 274.97, 'l': 270, 'o': 272.67, 'pc': 271.32, 't': 1676389555}, 
#             'TSLA': {'no_of_shares': 10,'country': 'US', 'currency': 'USD', 'exchange': 'NASDAQ NMS - GLOBAL MARKET', 'finnhubIndustry': 'Automobiles', 'ipo': '2010-06-09', 'logo': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/TSLA.svg', 'marketCapitalization': 615860.963791, 'name': 'Tesla Inc', 'phone': '15125168177.0', 'shareOutstanding': 3164.1, 'ticker': 'TSLA', 'weburl': 'https://www.tesla.com/', 'c': 197.3258, 'd': 2.6858, 'dp': 1.3799, 'h': 204.5, 'l': 189.45, 'o': 191.94, 'pc': 194.64, 't': 1676389547}, 
#             'IBM': {'no_of_shares': 10,'country': 'US', 'currency': 'USD', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 'finnhubIndustry': 'Technology', 'ipo': '1915-11-11', 'logo': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/IBM.svg', 'marketCapitalization': 124181.767081, 'name': 'International Business Machines Corp', 'phone': '19144991900.0', 'shareOutstanding': 904.126, 'ticker': 'IBM', 'weburl': 'https://www.ibm.com/', 'c': 135.67, 'd': -1.68, 'dp': -1.2232, 'h': 137.23, 'l': 135.635, 'o': 137.05, 'pc': 137.35, 't': 1676389538}, 
#             'UBER': {'country': 'US', 'currency': 'USD', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 'finnhubIndustry': 'Road & Rail', 'ipo': '2019-05-10', 'logo': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/UBER.svg', 'marketCapitalization': 66692.97899900001, 'name': 'Uber Technologies Inc', 'phone': '14156128582.0', 'shareOutstanding': 1994.41, 'ticker': 'UBER', 'weburl': 'https://www.uber.com', 'c': 33.5, 'd': 0.06, 'dp': 0.1794, 'h': 34.08, 'l': 32.7239, 'o': 33.11, 'pc': 33.44, 't': 1676389544}, 
#             'DIS': {'country': 'US', 'currency': 'USD', 'exchange': 'NEW YORK STOCK EXCHANGE, INC.', 'finnhubIndustry': 'Media', 'ipo': '1957-11-12', 'logo': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/DIS.svg', 'marketCapitalization': 196674.07533, 'name': 'Walt Disney Co', 'phone': '18185601000.0', 'shareOutstanding': 1826.81, 'ticker': 'DIS', 'weburl': 'https://thewaltdisneycompany.com/', 'c': 106.74, 'd': -0.92, 'dp': -0.8545, 'h': 108.43, 'l': 105.8205, 'o': 106.82, 'pc': 107.66, 't': 1676389559}, 
#             'SBUX': {'country': 'US', 'currency': 'USD', 'exchange': 'NASDAQ NMS - GLOBAL MARKET', 'finnhubIndustry': 'Hotels, Restaurants & Leisure', 'ipo': '1992-06-26', 'logo': 'https://static2.finnhub.io/file/publicdatany/finnhubimage/stock_logo/SBUX.svg', 'marketCapitalization': 124722.037441, 'name': 'Starbucks Corp', 'phone': '12064471575.0', 'shareOutstanding': 1149.3, 'ticker': 'SBUX', 'weburl': 'https://www.starbucks.com/', 'c': 107.11, 'd': -1.41, 'dp': -1.2993, 'h': 108.4652, 'l': 107.1, 'o': 107.93, 'pc': 108.52, 't': 1676389573}
#             }
#     return val

def home(request):
    stocks = {}
    key = os.environ.get('API_KEY')
    company = Shares.objects.all().values()
    news = {}
    print("Getting API Data")
    for stock in company:
    #     company = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={stock}&token={key}')
        ticker = stock['ticker']
        data = requests.get(f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={key}')
        data = json.loads(data.text)
        share_data = {**stock, **data}
        stocks[ticker] = share_data

    print(stocks)
    dt = date.today() - timedelta(days=1)
    print(dt)
    extras = requests.get(f'https://finnhub.io/api/v1/company-news?symbol=AAPL&from={dt}&to={dt}&token={key}').json()
    print(extras)
    context = {
        'stocks': stocks,
        'extras': extras
    }

    return render(request, 'home.html', context)


def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)

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