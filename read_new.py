url_root = r'https://www.cricbuzz.com'
url_archives=url_root + r'/cricket-scorecard-archives'
import requests
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree
from lxml import html
import pandas as pd

def GetTournaments(year):
	tours=[]
	dom = lxml.html.fromstring(requests.get(url_archives).content)
	for x in dom.xpath('//a/@href'):
		link=url_root+x
		if year in str(link):
			#print (link)
			dom = lxml.html.fromstring(requests.get(link).content)
			for x in dom.xpath('//a/@href'):
				if year in str(x):
					#print (url_root + x)
					tours.append(url_root + x)
	return tours

def GetScoreCards(year):
	scorecards=[]
	tours = GetTournaments(year)
	for tour in tours:
		dom = lxml.html.fromstring(requests.get(tour).content)
		for x in dom.xpath('//a/@href'):
			if 'cricket-scores' in str(x) and year in str(x):
				final_url = (url_root + x).replace('cricket-scores', 'live-cricket-scorecard')
				#print (final_url)
				scorecards.append(final_url)
	return scorecards

year='2011'
scores=GetScoreCards(year)
print (scores)

resp = requests.get(scores[0])
tree=html.fromstring(resp.content)

