from bs4 import BeautifulSoup
import urllib.request
import re

def hangi_uudis():
    n = 0
    a = urllib.request.urlopen("https://leht.postimees.ee/")
    data = a.read()
    soup = BeautifulSoup(data, features="html.parser")
    for link in soup.find_all('a'):
        ilus_link = link.get('href')
        if n == 3:
            break
        if re.match("https://leht.postimees.ee", ilus_link):
            if re.match("https://leht.postimees.ee/section", ilus_link):
                x = False
            elif re.match("https://leht.postimees.ee/", ilus_link):
                if n == 2:
                    uudis = ilus_link
                    n += 1
                else:
                    n += 1
                
    return uudis
            