url_root = r'https://www.cricbuzz.com'
url_archives=url_root + r'/cricket-scorecard-archives'
import requests
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree
from lxml import html
import re

#remove duplicate entries
def RemoveDuplicates(mylist):
	output_entries = list(dict.fromkeys(mylist))
	return output_entries

def GetTournaments(years):
	tours=[]
	dom = lxml.html.fromstring(requests.get(url_archives).content)
	for x in dom.xpath('//a/@href'):
		link=url_root+x
		for year in years:
			if year in str(link):
				print ('Checking year ' + year)
				dom = lxml.html.fromstring(requests.get(link).content)
				for x in dom.xpath('//a/@href'):
					if year in str(x):
						tours.append(url_root + x)
	tours=RemoveDuplicates(tours)
	return tours
	
def GetScoreCards(tours, years):
	scorecards=[]
	for tour in tours:
		dom = lxml.html.fromstring(requests.get(tour).content)
		for x in dom.xpath('//a/@href'):
			for year in years:
				if 'cricket-scores' in str(x) and year in str(x):
					final_url = (url_root + x).replace('cricket-scores', 'live-cricket-scorecard')
					scorecards.append(final_url)
	scorecards=RemoveDuplicates(scorecards)
	return scorecards
	
def GetDismissals(player, scores):
	print ('Getting dismissals for player ' + player)
	output_entries = []
	for score in scores:
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
					if line.lstrip().lower().startswith(player):
						print ('Found in ' + score)
						output_entries.append(line)						
	#remove duplicate entries
	output_entries = RemoveDuplicates(output_entries)
	return output_entries
	
def ProcessDismissal(player, dismissals):
	output=[]
	for dismissal in dismissals:
		temp = dismissal.lower().split(player)[-1]
		temp=temp.lstrip(' ')
		print (temp)