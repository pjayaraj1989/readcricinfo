from functions import*

years_range = range(2011,2015)
years = [str(year) for year in years_range]

player = 'ed cowan'
tournaments = GetTournaments(years)
scores = GetScoreCards(tournaments, years)
     
#now sort based on tournament type
scores = GetMatchesByType(scores, 'test')

dismissals = GetDismissals(player, scores)

#process each dismissal
dismissals = ProcessDismissal(player, dismissals)

print (len(dismissals))
op = GetStatistics(dismissals)
print (op)

'''
bowlers = GetBowlers(dismissals)
'''
