import requests 
from bs4 import BeautifulSoup
import re

url=r'http://www.espncricinfo.com/ci/engine/series/index.html'
url_root=r'http://www.espncricinfo.com/'
url_static=r'static.espncricinfo.com'

def GetSeasons(url):
    links_final=[]
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    links = soup.findAll('a', href=True)
    links_final=[]
    for link in links:
        if 'ARCHIVE' in str(link):
            links_final.append(url_static + link['href'])
        else:
            links_final.append (url_root + link['href'])    
    return(links_final)


links_seasons = GetSeasons(url)

for l in links_seasons: print (l)