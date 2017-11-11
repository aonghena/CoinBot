import feedparser

def coinNews():
    bitcoin = feedparser.parse("https://news.google.com/news/rss/search/section/q/bitcoin/bitcoin?hl=en&gl=US&ned=us/.rss")
    crypto = feedparser.parse("https://news.google.com/news/rss/search/section/q/cryptocurrency/cryptocurrency?hl=en&gl=US&ned=us/.rss")
    
    bitcoinLinks = []
    cryptoLinks = []
    
    for post in crypto.entries:
        cryptoLinks.append(post.link)
        
    for post in bitcoin.entries:
        bitcoinLinks.append(post.link)

    
    return cryptoLinks[0] + '\n' + cryptoLinks[1], bitcoinLinks[0] + '\n' + bitcoinLinks[1]
