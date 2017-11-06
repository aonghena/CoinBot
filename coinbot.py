import discord
import asyncio
import requests
from password import KEY

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
        await client.send_message(message.channel, '```Bitcoin Price !btc, !bitcoin\nEthereum Price !eth, !ethereum\nBoth !coins, !all ```')
    elif message.content.startswith(('!btc', '!bitcoin', '!Bitcoin')):
        price = '```Bitcoin: $'
        price += str(coinPrice(1)) + ' '
        price += coinPercent(1) + '%'
        price += '```'
        await client.send_message(message.channel, price)
        
    elif message.content.startswith('!bye'):
        await client.send_message(message.channel, '```GFY```')
        
    elif message.content.startswith(('!eth','!ETH', '!ethereum', '!Ethereum')):
        price = '```Ethereum: $'
        price += str(coinPrice(2)) + ' '
        price += coinPercent(2) + '%'
        price += '```'
        await client.send_message(message.channel, price)
        
    elif message.content.startswith(('!ltc','!LTC', '!litecoin', '!LiteCoin')):
        price = '```Litecoin: $'
        price += str(coinPrice(3)) + ' '
        price += coinPercent(3) + '%'
        price += '```'
        await client.send_message(message.channel, price)
        
    elif message.content.startswith(('!coin', '!all', '!COIN', '!Coin')):
        all = '```Bitcoin:   $'
        all += str(coinPrice(1)) + '  ' 
        if message.content.endswith('-p'):
            all += coinPercent(1) + '%'
        all += "\nEthereum:  $"
        all += str(coinPrice(2)) + '   '
        if message.content.endswith('-p'):
            all += coinPercent(2) + '%'
        all += '\nLitecoin:  $'
        all += str(coinPrice(3)) + '    '
        if message.content.endswith('-p'):
            all += coinPercent(2) + '%'
        all += '```'
        await client.send_message(message.channel, all)

        
def coinPrice( x ):
    if x == 1:
        current = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy').json()['data']['amount'])
        current = round(current/2,2)
        return current
    elif x == 2:
        current = float(requests.get('https://api.coinbase.com/v2/prices/ETH-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/ETH-USD/buy').json()['data']['amount'])
        current = round(current/2,2)
        return current
    elif x ==3:
        current = float(requests.get('https://api.coinbase.com/v2/prices/LTC-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/LTC-USD/buy').json()['data']['amount'])
        current = round(current/2,2)
        return current
   

def coinPercent( x ):
    if x == 1:
        current = round(((coinPrice(1)/float(requests.get('https://api.gdax.com/products/BTC-USD/stats').json()['open']))-1)*100,2)
        return str(current)
    elif x == 2:
        current = round(((coinPrice(2)/float(requests.get('https://api.gdax.com/products/ETH-USD/stats').json()['open']))-1)*100,2)
        return str(current)
    elif x == 3:
        current = round(((coinPrice(3)/float(requests.get('https://api.gdax.com/products/LTC-USD/stats').json()['open']))-1)*100,2)
        return str(current)

client.run(KEY)
