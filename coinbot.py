import discord
import asyncio
import requests
from password import KEY
from decimal import *
from coinNews import coinNews

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


    
@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        await client.send_message(message.channel, '```!btc !bitcoin : to get the latest bitcoin price from coinbase \n!eth !ethereum : to get the latest Ethereum Price'+
        '\n!ltc !litecoin : to get the latest etherum price from Coinbase: \n!all : get latest eth btc ltc price \n!COIN_TICKER : to get the latest price of that coin'+
        '\n!news shows the latest cryptocurrency news```')
    elif message.content.startswith(('!btc', '!bitcoin', '!Bitcoin')):
        cost , change = coinBasePrice(1)
        price = '```Bitcoin: $'
        price += str(cost) + ' '
        price += str(change) + '%'
        price += '```'
        await client.send_message(message.channel, price)
    
    elif message.content.startswith(('!news', '!News')):
        c, b = coinNews()
        news = str(c)
        if message.content.endswith('-b'):
            news = str(b)
        await client.send_message(message.channel, news)   
       
    elif message.content.startswith('!bye'):
        await client.send_message(message.channel, '```GFY```')
        
    elif message.content.startswith(('!eth','!ETH', '!ethereum', '!Ethereum')):
        cost , change = coinBasePrice(2)
        price = '```Ethereum: $'
        price += str(cost) + ' '
        price += str(change) + '%'
        price += '```'
        await client.send_message(message.channel, price)
        
    elif message.content.startswith(('!ltc','!LTC', '!litecoin', '!LiteCoin')):
        cost , change = coinBasePrice(3)
        price = '```Litecoin: $'
        price += str(cost) + ' '
        price += str(change) + '%'
        price += '```'
        await client.send_message(message.channel, price)
        
    elif message.content.startswith(('!all')):
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
            
    elif message.content.startswith(('!')):
        t = str(message.content[1:])
        price = coinCapePrice(t.upper())
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
    
        
#CoinCap.io price
def coinCapePrice(t):
    try:
        coin = requests.get('http://coincap.io/page/' + t).json()['display_name']
        cost = requests.get('http://coincap.io/page/' + t).json()['price_usd']
        per = float(requests.get('http://coincap.io/page/' + t).json()['cap24hrChange'])
        if(float(cost) > 1):
            cost = round(float(cost),2)
        price = '```' + str(coin) + ': $'
        price += str(cost) + ' '
        price += str(per)+'%'
    except:
        price = '```Ticker Not Found'

    return price
        

client.run(KEY)
