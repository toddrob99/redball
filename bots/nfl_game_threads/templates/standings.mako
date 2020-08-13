<%
    if not len(data["standings"]):
        return
    unsortedDivStandings = {x["standings"]["data"][0]["divisionRank"]: x for x in data["standings"] if x["division"]["abbr"] == data["myTeam"]["division"]["abbr"]}
    sortedDivStandings = [unsortedDivStandings[x] for x in sorted(unsortedDivStandings)]    
%>\
${'##'} Standings
|${sortedDivStandings[0]["division"]["abbr"]} Rank|Team|Wins|Losses|Ties|Win%|
|:--|:--|:--|:--|:--|:--|
${"\n".join([f"|{x['standings']['data'][0]['divisionRank']}|{x['abbr']}|{x['standings']['data'][0]['overallWins']}|{x['standings']['data'][0]['overallLosses']}|{x['standings']['data'][0]['overallTies']}|{x['standings']['data'][0]['overallWinPct']}|" for x in sortedDivStandings])}