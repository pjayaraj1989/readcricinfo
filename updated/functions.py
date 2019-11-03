url_root = r'https://www.cricbuzz.com'
url_archives=url_root + r'/cricket-scorecard-archives'
import requests
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree
from lxml import html
import re
from collections import Counter

def Error_Exit(msg):
	print(msg)
	exit()

#remove duplicate entries
def RemoveDuplicates(mylist):
	output_entries = list(dict.fromkeys(mylist))
	return output_entries

def GetTournaments(years):
	tours=[]
	dom = lxml.html.fromstring(requests.get(url_archives).content)
	if dom is None:	Error_Exit('No data read')
	if len(dom.xpath('//a/@href')) is 0:	Error_Exit('No links found')	
	for x in dom.xpath('//a/@href'):
		link=url_root+x
		for year in years:
			if year in str(link):
				print ('Checking year ' + year)
				dom = lxml.html.fromstring(requests.get(link).content)
				for x in dom.xpath('//a/@href'):
					if year in str(x):
						tours.append(url_root + x)
	if len(tours) is 0:	Error_Exit('No tournaments found')
	tours=RemoveDuplicates(tours)
	return tours
	
def GetScoreCards(tours, years):
	scorecards=[]
	for tour in tours:
		dom = lxml.html.fromstring(requests.get(tour).content)
		for x in dom.xpath('//a/@href'):
			for year in years:
				if 'cricket-scores' in str(x) or 'live-cricket-scorecard' in str(x) and year in str(x):
					final_url = (url_root + x).replace('cricket-scores', 'live-cricket-scorecard')
					scorecards.append(final_url)
	scorecards=RemoveDuplicates(scorecards)
	return scorecards

def GetMatchesByType(scorecards, param):
	output=[]
	for scorecard in scorecards:
		if param is 'test':
			if 'test' in scorecard:
				output.append(scorecard)
	return output
	
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

def RemoveStrayChars(entry, stray_strings):
	for s in stray_strings:
		if s in entry:
			entry = entry.replace(s, ' ').lstrip(' ').rstrip(' ')
	return entry
	
def ProcessDismissal(player, dismissals):
	output=[]
	for dismissal in dismissals:
		entry=[]
		temp = dismissal.lower().split(player)[-1]
		temp=temp.lstrip(' ')
		#remove stray entries		
		temp = RemoveStrayChars(temp, ['(c)','(wk)','(c & wk)'])		
		token=r'[\d]+[\s]+[\d]+[\s]+[\d]+[\s]+[\d]+[\s]+[\d]+.[\d]+'
		stats = re.findall(token, temp)[0]
		if stats in temp:
			mode_of_dismissal = temp.split(stats)[0]
			entry.append(mode_of_dismissal)
			entry.append(stats)
			output.append(entry)
			#output[mode_of_dismissal] = stats
	return output

def GetStatistics(dismissals_processed):
	runs=0
	for d in dismissals_processed:
		run = d[-1].split(' ')[0]
		runs += int(run)	
	return runs

def GetBowlers(dismissals):
	bowlers=[]
	for d in dismissals:
		if ' b ' in d[0]:
			bowlers.append(d[0].split(' b ')[-1])	
		if 'run out' in d[0]:
			bowlers.append('run out')
		if 'not out' in d[0]:
			bowlers.append('not out')
	
	print (bowlers)
	'''
	c = Counter(bowlers)
	return (c)
	'''