    #This supports the most recent discord.py library.
import discord
import asyncio
import requests
import feedparser
import json
import datetime
from decimal import *
from password import KEY, IEX_TOKEN
from tabulate import tabulate
from discord.ext import commands
from xml.dom import minidom
import xml.etree.ElementTree as ET
    
all_markets_url = "https://www.predictit.org/api/marketdata/all/"

#maps market id to market name
market_names = {}
'''15
Who will win the 2020 Democratic presidential nomination?
3633
____
16
Who will win the 2020 Republican presidential nomination?
3653'''


r = requests.get(all_markets_url)
r.close()
markets = json.loads(r.content)["markets"]
print("STATUS")
print(r.status_code)
i = 0

print(markets[15]['name'])
print(markets[15]['contracts'][1])

for market in (markets[15]['contracts']):
    print(i)
    print(market['name'])
    print(market['lastTradePrice'])
    l = (((market['lastTradePrice']/market['lastClosePrice'])-1)*100)
    print("{:.2f}".format(l))
    print("____")
    i+=1
    if(i == 5):
        break