<%
    if not len(data["standings"]):
        return
    divTeams = [x for x in data["standings"] if x["division"]["abbr"] == data["myTeam"]["division"]["abbr"]]
    #unsortedDivStandings = {x["standings"]["data"][0]["divisionRank"]: x for x in data["standings"] if x["division"]["abbr"] == data["myTeam"]["division"]["abbr"]}
    #sortedDivStandings = [unsortedDivStandings[x] for x in sorted(unsortedDivStandings)]
%>\
${'##'} Standings
|${data["myTeam"]["division"]["abbr"]} Rank|Team|Wins|Losses|Ties|Win%|
|:--|:--|:--|:--|:--|:--|
## ${"\n".join([f"|{x['standings']['data'][0]['divisionRank']}|{x['abbr']}|{x['standings']['data'][0]['overallWins']}|{x['standings']['data'][0]['overallLosses']}|{x['standings']['data'][0]['overallTies']}|{x['standings']['data'][0]['overallWinPct']}|" for x in sortedDivStandings])}
% for i in range(1, len(divTeams)+1):
% if len([x for x in divTeams if x['standings']['data'][0]['divisionRank'] == i]):
${"\n".join([f"|{x['standings']['data'][0]['divisionRank']}|{x['abbr']}|{x['standings']['data'][0]['overallWins']}|{x['standings']['data'][0]['overallLosses']}|{x['standings']['data'][0]['overallTies']}|{x['standings']['data'][0]['overallWinPct']}|" for x in divTeams if x['standings']['data'][0]['divisionRank'] == i])}
% endif
% endfor