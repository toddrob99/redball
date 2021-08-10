<%
    if not len(data["standings"]):
        return
    divTeams = sorted([x for x in data["standings"] if next((True for y in data["otherDivisionTeams"] if x["team"]["id"] == y["id"] or x["team"]["id"] == data["myTeam"]["id"]), False)], key=lambda t: t['division']['rank'])
%>\
${'##'} Standings
|${data["myTeam"]["divisionFullName"]} Rank|Team|Wins|Losses|Ties|Win%|
|:--|:--|:--|:--|:--|:--|
## ${"\n".join([f"|{x['standings']['data'][0]['divisionRank']}|{x['abbr']}|{x['standings']['data'][0]['overallWins']}|{x['standings']['data'][0]['overallLosses']}|{x['standings']['data'][0]['overallTies']}|{x['standings']['data'][0]['overallWinPct']}|" for x in sortedDivStandings])}
${"\n".join([f"|{x['division']['rank']}|{x['team']['fullName']}|{x['overall']['wins']}|{x['overall']['losses']}|{x['overall']['ties']}|{x['overall']['winPct']}|" for x in divTeams])}