from functions import*

years_range = range(1985,2015)
years = [str(year) for year in years_range]

player = 'sachin tendulkar'
tournaments = GetTournaments(years)
scores = GetScoreCards(tournaments, years)

dismissals = GetDismissals(player, scores)
#process each dismissal
dismissals = ProcessDismissal(player, dismissals)

bowlers = GetBowlers(dismissals)
print (bowlers)
