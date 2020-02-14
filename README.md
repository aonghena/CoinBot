# CoinBot
This is a CryptoCurrency/Stock Bot for Discord.
Supports 1200+ cryptocurrencies.
Supports Stock tickers


#### Versions:<br>
coinbotV1.py: used for python 3.5+ and discord.py 1.0.0+<br>
coinbot.py: if your using a lower version python and discord V.<br>





#### Usage:<br>
!help: Command Info
  
  
!all: Bitcoin, Ethereum, Litecoin, Bitcoin Cash  price/24hr change. (removed in coinbaseV1.py)
  
  
!news: Return two of the most recent news articles related to cryptocurrency
  
!prez, !dprez, !rprez - PredictIt Market info
      
!COINTICKER: COINTICKER price/24 hr change<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example: !BTC: Bitcoin price/24 hr change.
    
  
$STOCKTICKER: STOCKTICKER price/24 hr change.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example: $AAPL: Apple Share price/24 hr change
  
@Coinbot params: Generates Users list of coins and stocks<br>
populate by adding either a coin name !, or adding a stock ticker $  
populate by adding either a coin name !, or adding a stock ticker $  
clear list by adding clear in the param<br>  
Example: @coinbot $AAPL !BTC :<br>  
| Name       | Price    | Change   |<br>
|------------|----------|----------|<br>
| Bitcoin    | $8030.00 | -3.35%   |<br>
| Apple Inc. | $186.99  | -0.63%   |<br>
  
  
@coinbot clear: removes list
  
  
  
  



#### Setup:<br>
`git clone https://github.com/aonghena/CoinBot.git`<br>
`pip install discord.py`<br>
`pip install feedparser`<br>
`pip install tabulate`<br>
Create an account and generate and IEXCloud token.<br>
Generate a discord token <a href="https://discordapp.com/developers/applications/me">here</a><br>
Add both discord token and IEXCloud token to password.py<br>
Then go and replace Client_ID_Key with yours:<br>
https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_GOES_HERE&scope=bot&permissions=0<br>
<br>
<br>
If you can't get generate the token, there are tons of examples online that probably do a better job
at explanning how to do it.
<br>

  
  
  
  
 ____________________________________________
<a href="https://developers.coinbase.com/">Coinbase</a>
<br>
<a href="https://api.coinmarketcap.com">CoinMarketCap</a>
<br>
<a href="https://iextrading.com/">IEX</a>
<br>
<a href="http://stockcharts.com/">StockCharts</a>
<br>
<a href="https://cryptohistory.org/">CryptoHistory</a>
<br>
<a href="https://www.predictit.org">PredictIt</a>


