from bs4 import BeautifulSoup
import urllib.request
import re
from random import choice

def hangi_uudis():
    a = urllib.request.urlopen("https://uudised.err.ee/")
    data = a.read()
    soup = BeautifulSoup(data, features="html.parser")
    news = []
    for article in soup.find_all('article'):
        url = article.a['href']
        if url and (re.match("//uudised.err.ee/", url) or re.match("//www.err.ee/", url)):
            news += ["https:"+url]
            
    pick = choice(news)
    a = urllib.request.urlopen(pick)
    data = a.read()
    soup = BeautifulSoup(data, features="html.parser")
    
    lead = soup.find("div", class_="lead").p.get_text()
    title = soup.find("h1").get_text().strip("({{contentCtrl.commentsTotal}})")
    
    uudis = {'lead':lead,'title':title,'link':pick}
                
    return uudis
