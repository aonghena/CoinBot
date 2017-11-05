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
        price += coinPrice(1)
        price += '```'
        await client.send_message(message.channel, price)
    elif message.content.startswith('!bye'):
        await client.send_message(message.channel, '```GFY```')
    elif message.content.startswith(('!eth','!ETH', '!ethereum', '!Ethereum')):
        price = '```Ethereum: $'
        price += coinPrice(2)
        price += '```'
        await client.send_message(message.channel, price)
    elif message.content.startswith(('!ltc','!LTC', '!litecoin', '!LiteCoin')):
        price = '```Litecoin: $'
        price += coinPrice(3)
        price += '```'
        await client.send_message(message.channel, price)
    elif message.content.startswith(('!coin', '!all', '!COIN', '!Coin')):
        price = coinPrice(-1)
        await client.send_message(message.channel, price)
        

        
def coinPrice( x ):
    if x == 1:
        current = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy').json()['data']['amount'])
        current = round(current/2,2)
        return str(current)
    elif x == 2:
        current = float(requests.get('https://api.coinbase.com/v2/prices/ETH-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/ETH-USD/buy').json()['data']['amount'])
        current = round(current/2,2)
        return str(current)
    elif x ==3:
        current = float(requests.get('https://api.coinbase.com/v2/prices/LTC-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/LTC-USD/buy').json()['data']['amount'])
        current = round(current/2,2)
        return str(current)
    else:
        all = '```Bitcoin:   $'
        all += coinPrice(1)
        all += "\nEthereum:  $"
        all += coinPrice(2)
        all += '\nLitecoin:  $'
        all += coinPrice(3)
        all += '```'
        return all
 
client.run(KEY)