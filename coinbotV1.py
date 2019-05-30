#This supports the most recent discord.py library.
import discord
import asyncio
import requests
import feedparser
from decimal import *
from password import KEY
from tabulate import tabulate
from discord.ext import commands

#This is used for discord.py >= V1.0


'''
CoinBase: Crypto prices
CoinMarketCap: Other Crypto price
CryptoHistory: Crypto Charts
IEXPrice: Stock ticker price
StockCharts: Stock Charts
Google news rss feed: News
'''
description = '''Discord bot for fetching Crypto and Stock Prices in discord'''
bot = commands.Bot(command_prefix='[!,$]', description=description)

portfolio = {}

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if message.content.lower().startswith(('!help')):
        await message.channel.trigger_typing()
        help = ('```!all : get latest eth btc ltc bch price '
        + '\n!COIN_TICKER : to get the latest price of the coin' 
        + '\n$STOCK_TICKER : to get the latest price of the ticker'
        + '\n!news shows the latest cryptocurrency news!```')
        await message.channel.send(help)
    elif message.content.lower().startswith('<@' + str(bot.user.id) + '>'):
        t = (message.content.split(' '))
        await message.channel.trigger_typing()
        t.pop(0)
        if message.author in portfolio:
            portfolio[message.author].extend(t)
        else:
            portfolio[message.author] = []
            portfolio[message.author].extend(t)
        portfolio[message.author] = list(set(portfolio[message.author]))
        post = '```'
        name = []
        nCost = []
        nPer = []
        for st in portfolio[message.author]:
            newST = str(st[1:])
            if st.startswith('!'):
                coin, cost, per = coinMarketCapPrice(newST.upper())
                if(cost == -1):
                    portfolio[message.author].remove(st)
                else:
                    name.append(coin)
                    nCost.append('$'+cost) 
                    nPer.append(per+'%')
            elif st.startswith('$'):
                company, cost, per = IEXPrice(newST.upper())
                if(cost == -1):
                    portfolio[message.author].remove(st)
                else:
                    name.append(company)
                    nCost.append('$'+str(cost)) 
                    nPer.append(str(per)+'%')
            elif st == 'clear':
                portfolio[message.author].clear()
            else:
                portfolio[message.author].remove(st)

        table = zip(name, nCost, nPer)
        t = (tabulate(table, tablefmt='orgtbl'))
        t = '```' + t + '```'
        await message.channel.send(t)

     #Returns most recent news from google.
    ##2 of the most recent news articles  
    elif message.content.lower().startswith('!news'):
        await message.channel.trigger_typing()
        crypto = feedparser.parse("https://news.google.com/news/rss/search/section/q/cryptocurrency/cryptocurrency?hl=en&gl=US&ned=us/.rss")
        cryptoLinks = []
        for post in crypto.entries:
            cryptoLinks.append(post.link)
        await message.channel.send(str(cryptoLinks[0] + '\n' + cryptoLinks[1]))


    #Return all of the coinbase coin prices (No chart)
    elif message.content.lower().startswith(('!all')):
        await message.channel.trigger_typing()
        cost , change = coinBasePrice('BTC')
        all = '```Bitcoin:       $'
        all += str(cost) + '  ' 
        all += str(change) + '%'
        cost , change = coinBasePrice('ETH')
        all += "\nEthereum:      $"
        all += str(cost) + '   ' 
        all += str(change) + '%'
        cost , change = coinBasePrice('LTC')
        all += '\nLitecoin:      $'
        all += str(cost) + '    ' 
        all += str(change) + '%'
        cost , change = coinBasePrice('BCH')
        all += '\nBitcoin Cash:  $'
        all += str(cost) + '    ' 
        all += str(change) + '%'
        all += '```'        
        await message.channel.send(all)

    elif message.content.startswith("!"):
        await message.channel.trigger_typing()
        t = str(message.content[1:].split()[0])
        coin, cost, per = coinMarketCapPrice(t.upper())
        #If ticker not found
        if(cost == -1):
            await client.send_message(message.channel, '```Ticker Not Found```')
        else:
            #Gets proper conversion (Charts under .9$ generally don't work)
            if(float(cost) < .9):
                s = '-btc'
            else:
                s = '-usdt'
            #change colors of message if coin is currently up or down
            if(float(per) < 0):
                c = discord.Colour(0xCD0000)
            elif(float(per) > 0):
                c = discord.Colour(0x00ff00)
            else:
                c = discord.Colour(0xffffff)
            #get chart
            chart = 'https://cryptohistory.org/charts/light/' + t.lower() + s +'/7d/png'
            #Creates embeded message
            embedCoin = discord.Embed(title=coin, description=t.upper() + ": $" + cost + " " + per + "% ", color = (c) )
            embedCoin.set_image(url = chart)
            await message.channel.send(embed=embedCoin)

    elif message.content.startswith("$"):
        await message.channel.trigger_typing()
        t = str(message.content[1:].split()[0])
        company, cost, per = IEXPrice(t.upper())
        #If ticker is not found
        if(cost == -1):
            await client.send_message(message.channel, '```Ticker Not Found```')
        else:
            #change colors of message if stock is currently up or down
            if(float(per) < 0):
                c = discord.Colour(0xCD0000)
            elif(float(per) > 0):
                c = discord.Colour(0x00ff00)
            else:
                c = discord.Colour(0xffffff)
            #get chart (. is replace with / for things like brk.a)
            chart =  'http://c.stockcharts.com/c-sc/sc?s=' + t.upper().replace('.','/') + '&p=D&b=5&g=0&i=0'
            #Creates embeded message
            embed = discord.Embed(title=company, description=t.upper() + ": $" + str(cost) + " " + str(per) + "% ", color = (c) )
            embed.set_image(url = chart)
            await message.channel.send(embed=embed)

    







#coinbase price       
def coinBasePrice(x):
    TWOPLACES = Decimal(10) ** -2 
    current = float(requests.get('https://api.coinbase.com/v2/prices/' + x + '-USD/spot').json()['data']['amount'])
    per = round(((current/float(requests.get('https://api.pro.coinbase.com/products/' + x + '-USD/stats').json()['open']))-1)*100,2)
    current = Decimal(current).quantize(TWOPLACES)
    per = Decimal(per).quantize(TWOPLACES)
    return str(current), str(per)
    

#coinMarketCapPrice
#Return coin info
def coinMarketCapPrice(t):
    loc = -1
    try:
        coinInfo = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=1500').json()
        for list in coinInfo:
            if list['symbol'] == t:
                loc = 0
                coin = list['name']
                cost = list['price_usd']
                per = list['percent_change_24h']
                break
        cost, per = coinBasePrice(t)#gets coinbase price if avaliable 
    except:
        price = -1
    
    #if ticker not found
    if(loc == -1):
        price = -1
        return price, price, price
    return coin, cost, per


#IEXPrice
#Returns stock info
def IEXPrice(t):
    try:
        stockInfo = requests.get('https://api.iextrading.com/1.0/stock/'+ (t)+  '/quote').json()
        company = stockInfo['companyName']
        cost = stockInfo['latestPrice']
        per = stockInfo['changePercent']
        price = str(company) + ' $'
        price += str(round(float(cost),2)) + ' '
        price += str(round((float(per)*100),2)) + '%'
    except:
        #if ticker not found
        price = -1
        return price, price, price
    return company, round(float(cost),2), round((float(per)*100),2)


bot.run(KEY)
