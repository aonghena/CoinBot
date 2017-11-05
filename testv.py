
import requests
import os
import sys
from datetime import datetime


sell_price = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy').json()['data']['amount'])
sell_price = round(sell_price/2,2)
stat = float(requests.get('https://api.gdax.com/products/BTC-USD/stats').json()['open'])
print (sell_price)
print(stat)
print(round(100*((sell_price/stat)-1),2))
print(round(100*((stat/sell_price)-1),2))