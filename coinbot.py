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
        price += coin(1)
        price += '```'
        await client.send_message(message.channel, price)
    elif message.content.startswith('!bye'):
        await client.send_message(message.channel, '```GFY```')
    elif message.content.startswith(('!eth','!ETH', '!ethereum', '!Ethereum')):
        price = '```Ethereum: $'
        price += coin(2)
        price += '```'
        await client.send_message(message.channel, price)
    elif message.content.startswith(('!coin', '!all', '!COIN', '!Coin')):
        price = coin(-1)
        await client.send_message(message.channel, price)
        

        
def coin( x ):
    if x == 1:
        current = float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy').json()['data']['amount'])
        current = round(current/2,2)
        return str(current)
    elif x == 2:
        current = float(requests.get('https://api.coinbase.com/v2/prices/ETH-USD/sell').json()['data']['amount']) + float(requests.get('https://api.coinbase.com/v2/prices/ETH-USD/buy').json()['data']['amount'])
        current = round(current/2,2)
        return str(current)
    else:
        all = '```Bitcoin:   $'
        all += coin(1)
        all += "\nEthereum:  $"
        all += coin(2)
        all += '```'
        return all
 
client.run(KEY)