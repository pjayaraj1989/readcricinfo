from functions import*

years_range = range(2004,2005)
years = [str(year) for year in years_range]

player = 'rahul dravid'
tournaments = GetTournaments(years)
scores = GetScoreCards(tournaments, years)
dismissals = GetDismissals(player, scores)
#process each dismissal
dismissals = ProcessDismissal(player, dismissals)

bowlers = GetBowlers(dismissals)
print (bowlers)

'''
bowlers=[]
for k in dismissals.keys():
	if ' b ' in k:
		bowlers.append(k.split(' b ')[-1])
		
print (bowlers)
'''