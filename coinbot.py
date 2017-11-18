import discord
import asyncio
import requests
from password import KEY
from decimal import *
from coinNews import coinNews

'''
CoinBase/GDAX: Bitcoin/Etherum/Litcoin prices
CoinMarketCap: Other CryptoCoins price
IEXPrice: Stock ticker price
google news rss feed: News

#####

Cryptonator, and CoinCap methods are 
below, but not in use, If you would
like to switch out CoinMarketCap data
for one of them, just go to l 93ish
to switch
'''

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='Cipher'))

@client.event
async def on_message(message):
    if message.content.lower().startswith(('!help','<@' + client.user.id + ">")):
        help = '```!btc !bitcoin : to get the latest bitcoin price from coinbase \n!eth !ethereum : to get the latest Ethereum Price'
        + '\n!ltc !litecoin : to get the latest etherum price from Coinbase: \n!all : get latest eth btc ltc price '
        + '\n!COIN_TICKER : to get the latest price of the coin' 
        + '\n$STOCK_TICKER : to get the latest price of the ticker'
        + '\n!news shows the latest cryptocurrency news```'
        await client.send_message(message.channel, help)
    elif message.content.startswith(('!btc', '!bitcoin', '!Bitcoin')):
        cost , change = coinBasePrice(1)
        price = '```Bitcoin: $'
        price += str(cost) + ' '
        price += str(change) + '%'
        price += '```'
        await client.send_message(message.channel, price)
    
    elif message.content.lower().startswith('!news'):
        c, b = coinNews()
        news = str(c)
        if message.content.lower().endswith('-b'):
            news = str(b)
        await client.send_message(message.channel, news)   
       
    elif message.content.lower().startswith('!bye'):
        await client.send_message(message.channel, '```Bye```')
        
    elif message.content.lower().startswith(('!eth', '!ethereum')):
        cost , change = coinBasePrice(2)
        price = '```Ethereum: $'
        price += str(cost) + ' '
        price += str(change) + '%'
        price += '```'
        await client.send_message(message.channel, price)
        
    elif message.content.lower().startswith(('!ltc', '!litecoin')):
        cost , change = coinBasePrice(3)
        price = '```Litecoin: $'
        price += str(cost) + ' '
        price += str(change) + '%'
        price += '```'
        await client.send_message(message.channel, price)
        
    elif message.content.lower().startswith(('!all')):
        cost , change = coinBasePrice(1)
        all = '```Bitcoin:   $'
        all += str(cost) + '  ' 
        all += str(change) + '%'
        cost , change = coinBasePrice(2)
        all += "\nEthereum:  $"
        all += str(cost) + '   ' 
        all += str(change) + '%'
        cost , change = coinBasePrice(3)
        all += '\nLitecoin:  $'
        all += str(cost) + '    ' 
        all += str(change) + '%'
        all += '```'
        await client.send_message(message.channel, all)
            
    #Gets price of all other cryptocurrencies 
    elif message.content.startswith(('!')):
        t = str(message.content[1:])
        ############################
        '''' currently not in use, but if you would like to switch out 
        where you get your coin data from just un-comment the provider you want
        and comment the previous used one
        '''
        #price = coinCapPrice(t.upper())
        #price = cryptonatorPrice(t)
        #############################

        price = coinMarketCapPrice(t.upper())
        price += '```'
        await client.send_message(message.channel, price)

    #Get price of stock ticker
    elif message.content.startswith(('$')):
        t = str(message.content[1:])
        price = IEXPrice(t.upper())
        price += '```'
        await client.send_message(message.channel, price)

#coinbase/GDAX price       
def coinBasePrice(x):
    TWOPLACES = Decimal(10) ** -2 
    if x == 1:
        current = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot').json()['data']['amount'])
        per = round(((current/float(requests.get('https://api.gdax.com/products/BTC-USD/stats').json()['open']))-1)*100,2)
    elif x == 2:
        current = float(requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot').json()['data']['amount'])
        per = round(((current/float(requests.get('https://api.gdax.com/products/ETH-USD/stats').json()['open']))-1)*100,2)
    elif x ==3:
        current = float(requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot').json()['data']['amount'])
        per = round(((current/float(requests.get('https://api.gdax.com/products/LTC-USD/stats').json()['open']))-1)*100,2)
    current = Decimal(current).quantize(TWOPLACES)
    per = Decimal(per).quantize(TWOPLACES)
    return current, per
    
#coinmarketcap
def coinMarketCapPrice(t):
    loc = -1
    coinInfo = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=1500').json()
    for list in coinInfo:
        if list['symbol'] == t:
            loc = 0
            coin = list['name']
            cost = list['price_usd']
            per = list['percent_change_24h']
            break
    if(loc == -1):
        price = '```Ticker Not Found'
        return price
    price = '```' + str(coin) + ': $'
    price += str(cost) + ' '
    price += str(per)+'%'
    return price

#IEXPrice for Stocks
def IEXPrice(t):
    try:
        stockInfo = requests.get('https://api.iextrading.com/1.0/stock/'+ (t)+  '/quote').json()
        company = stockInfo['companyName']
        cost = stockInfo['latestPrice']
        per = stockInfo['change']
        price = '```' + str(company) + ' $'
        price += str(cost) + ' '
        price += str(per) + '%'
    except:
        price = '```Ticker Not Found'
    return price

#CoinCap.io price
def coinCapPrice(t):
    try:
        coinInfo = requests.get('http://coincap.io/page/' + t).json()
        coin = coinInfo['display_name']
        cost = coinInfo['price_usd']
        per = float(coinInfo['cap24hrChange'])
        if(float(cost) > 1):
            cost = round(float(cost),2)
        price = '```' + str(coin) + ': $'
        price += str(cost) + ' '
        price += str(per)+'%'
    except:
        price = '```Ticker Not Found'

    return price
    
#cryptonator price
def cryptonatorPrice(t):
    try:
        coinInfo = requests.get('https://api.cryptonator.com/api/ticker/' + (t)+ '-usd').json()
        coin = coinInfo['ticker']['base']
        cost = coinInfo['ticker']['price']
        if(float(cost) > 1):
            cost = round(float(cost),2)
        price = '```' + str(coin) + ': $'
        price += str(cost)
    except:
        price = '```Ticker Not Found'
    return price


client.run(KEY)
