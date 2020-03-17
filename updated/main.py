from functions import*

years_range = range(2014,2015)
years = [str(year) for year in years_range]

player = 'mitchell starc'
tournaments = GetTournaments(years)
scores = GetScoreCards(tournaments, years)
     
#now sort based on tournament type
scores = GetMatchesByType(scores, 'test')

dismissals = GetDismissals(player, scores)

#process each dismissal
dismissals = ProcessDismissal(player, dismissals)

print ('{0} Dismissals'.format(str (len(dismissals))))
for d in dismissals:    print (d)

op = GetStatistics(dismissals)
print ('Total Runs: {0}'.format(op))

#bowlers = GetBowlers(dismissals)
