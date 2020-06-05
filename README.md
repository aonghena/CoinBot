# CoinBot
This is a Cryptocurrency/Stock Bot for Discord.  
Supports 1200+ cryptocurrencies.  
Supports Stock tickers.  
Supports Predict It Presedential Election Contracts  


#### Versions:<br>
coinbotV1.py: python 3.5+ and discord.py V1.0.0+<br>
coinbot.py: pytthon < 3.4 discord.py < V1.0 (not maintained).<br>





#### Usage:<br>
!help: Command Info
  
  
!COINTICKER: COINTICKER price/24 hr change<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example: !BTC<br>
    ![example](https://i.imgur.com/kgFLGHQ.png)  <br>
  
$STOCKTICKER: STOCKTICKER price/24 hr change.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example: $AAPL<br>
    ![example](https://imgur.com/XLdSgSch.png)  <br>
  
!STATEABBREVATION: STATE COVID INFORMATION.<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Example: !NY<br>
    ![example](https://imgur.com/a/ZMxaULL.png)  <br>
  
!news: Return two of the most recent news articles related to cryptocurrency
  
!prez, !dprez, !rprez - PredictIt Market info


#### Setup:<br>
`git clone https://github.com/aonghena/CoinBot.git`<br>
`pip install -r requirements.txt`<br><br>    
Create an account and generate a <a href="https://iexcloud.io/">IEXCloud token</a>.<br>
Create an account and generate a <a href="https://coinmarketcap.com/api/">Coin Market Cap token</a>.<br>
Generate a <a href="https://discordapp.com/developers/applications/me">Discord token</a><br>
Add these tokens to the password.py file<br>
Then go to the URL below and add the bot to your server (replace Client_ID_Key with yours):<br>
https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_GOES_HERE&scope=bot&permissions=0
Finally Run the bot: `python coinbotV1.py`
<br> 
You should be all set!
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
<br>
<a href="https://covidtracking.com">CovidTracking</a>


