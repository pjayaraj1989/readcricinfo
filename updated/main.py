from functions import*

years=['2003','2005']
tournaments = GetTournaments(years)
scores = GetScoreCards(tournaments, years)
dismissals = GetDismissals('sachin tendulkar', scores)
for d in dismissals:
	print (d)
