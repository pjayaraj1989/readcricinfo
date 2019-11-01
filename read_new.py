url_root = r'https://www.cricbuzz.com'
url_archives=url_root + r'/cricket-scorecard-archives'
import requests
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree
from lxml import html

year='2011'

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

def GetDismissals(player):
	output_entries = []
	scores=GetScoreCards(year)	
	for score in scores:
		#print (score)
		request = requests.get(score)
		soup = BeautifulSoup(request.text, 'html.parser')	
		ids = ["innings_1","innings_2","innings_3","innings_4"]
		for id in ids:
			s = soup.find(id=id)
			if s is not None:
				text = s.get_text(separator='')
				output = text.split('Extras')[0]
				output = output.split('Batsman')[-1]
				output = output.split('R B 4s 6s SR')[-1]
				lines=output.split('      ')
				for line in lines:
					if player in line.lower():
						output_entries.append(line)
	return output_entries

entries = GetDismissals('sachin tendulkar')
for entry in entries:
	print (entry)