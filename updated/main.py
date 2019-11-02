from functions import*

years_range = range(2004,2005)
years = [str(year) for year in years_range]

player = 'sachin tendulkar'
tournaments = GetTournaments(years)
scores = GetScoreCards(tournaments, years)
dismissals = GetDismissals(player, scores)
#process each dismissal
dismissals = ProcessDismissal(player, dismissals)

