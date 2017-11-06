
import requests
import os
import sys
from datetime import datetime



sell_price = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy').json()['data']['amount'])
sell_price = round(sell_price/2,2)
stat = float(requests.get('https://api.gdax.com/products/BTC-USD/stats').json()['open'])
print (sell_price)
print(stat)
current = round(((sell_price/float(requests.get('https://api.gdax.com/products/BTC-USD/stats').json()['open']))-1)*100,2)
print(str(current))

#test
for x in range (0, 10):
    try:
        print(requests.get('https://api.stocktwits.com/api/2/streams/symbol/BTC.X.json').json()['messages'][x]['body'])
        if str(requests.get('https://api.stocktwits.com/api/2/streams/symbol/BTC.X.json').json()['messages'][x]['entities']['sentiment']) != 'null':
            print(requests.get('https://api.stocktwits.com/api/2/streams/symbol/BTC.X.json').json()['messages'][x]['entities']['sentiment'])
    except ValueError:
        print()
