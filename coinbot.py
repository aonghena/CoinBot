import discord
import asyncio
import requests
import feedparser
from decimal import *
from password import KEY
from tabulate import tabulate

'''
CoinBase/GDAX: Bitcoin/Etherum/Litcoin/BCash prices
CoinMarketCap: Other CryptoCoins price
CryptoHistory: Crypto Charts
IEXPrice: Stock ticker price
StockCharts: Stock Charts
Google news rss feed: News
'''

client = discord.Client()

#Holds User Portfolio
#This is used for individual lists that users can make when you
#@coinbot
portfolio = {}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(game=discord.Game(name='IEX'))

@client.event
async def on_message(message):
    
    #Replies with help info
    if message.content.lower().startswith(('!help')):
        await client.send_typing(message.channel)
        help = ('```!all : get latest eth btc ltc bch price '
        + '\n!COIN_TICKER : to get the latest price of the coin' 
        + '\n$STOCK_TICKER : to get the latest price of the ticker'
        + '\n!news shows the latest cryptocurrency news```')
        await client.send_message(message.channel, help)


    #@coinbot -params
    #params- 
    #!coinname (seperated by spaces) 
    #$stockname (seperated by spaces)
    #clear (removes current list)
    #example:
    #@coinbot $aapl !btc
    #| Name       | Price    | Change   |
    #|------------+----------+----------|
    #| Bitcoin    | $8030.00 | -3.35%   |
    #| Apple Inc. | $186.99  | -0.63%   |
    elif message.content.lower().startswith('<@' + client.user.id + '>'):
        t = (message.content.split(' '))
        await client.send_typing(message.channel)
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
        await client.send_message(message.channel, t)





    #Returns most recent news from google.
    ##2 of the most recent news articles  
    elif message.content.lower().startswith('!news'):
        await client.send_typing(message.channel)
        crypto = feedparser.parse("https://news.google.com/news/rss/search/section/q/cryptocurrency/cryptocurrency?hl=en&gl=US&ned=us/.rss")
        cryptoLinks = []
        for post in crypto.entries:
            cryptoLinks.append(post.link)
        await client.send_message(message.channel, str(cryptoLinks[0] + '\n' + cryptoLinks[1]))   

    #Return all of the coinbase coin prices (No chart)
    elif message.content.lower().startswith(('!all')):
        await client.send_typing(message.channel)
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
        await client.send_message(message.channel, all)

    


    #Gets price of cryptocurrencies aswell as charts (If found)
    elif message.content.startswith(('!')):
        await client.send_typing(message.channel)
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
            await client.send_message(message.channel, embed=embedCoin)

    #Get price of stock ticker and chart (If found)
    elif message.content.startswith(('$')):
        await client.send_typing(message.channel)
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
            #get chart (. is replace with / primarily for brk.a)
            chart =  'http://stockcharts.com/c-sc/sc?s=' + t.upper().replace('.','/') + '&p=D&b=5&g=0&i=0'
            #Creates embeded message
            embed = discord.Embed(title=company, description=t.upper() + ": $" + str(cost) + " " + str(per) + "% ", color = (c) )
            embed.set_image(url = chart)
            await client.send_message(message.channel, embed=embed)

#coinbase/GDAX price       
def coinBasePrice(x):
    TWOPLACES = Decimal(10) ** -2 
    current = float(requests.get('https://api.coinbase.com/v2/prices/' + x + '-USD/spot').json()['data']['amount'])
    per = round(((current/float(requests.get('https://api.gdax.com/products/' + x + '-USD/stats').json()['open']))-1)*100,2)
    current = Decimal(current).quantize(TWOPLACES)
    per = Decimal(per).quantize(TWOPLACES)
    return current, per
    

#coinMarketCapPrice
#Return coin info
def coinMarketCapPrice(t):
    #Gets GDAX price instead of using CoinMarketCap
    if(t == 'BTC'):
        return 'Bitcoin', str(coinBasePrice(t)[0]), str(coinBasePrice(t)[1])
    elif(t == 'ETH'):
        return 'Etherum', str(coinBasePrice(t)[0]),  str(coinBasePrice(t)[1])
    elif(t == 'LTC'):
        return 'Litecoin', str(coinBasePrice(t)[0]),  str(coinBasePrice(t)[1])
    elif(t == 'BCH'):
        return 'Bitcoin Cash', str(coinBasePrice(t)[0]),  str(coinBasePrice(t)[1])
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



client.run(KEY)