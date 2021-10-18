<%
    if not len(data["standings"]):
        return
    myDivStandings = next((
        x["teamRecords"]
        for x in data["standings"]
        if x["division"]["id"] == data["myTeam"]["division"]["id"]
    ), [])
%>\
${'##'} ${data["myTeam"]["division"]["nameShort"]} Standings
|Rank|Team|Wins|Losses|OT|Points|
|:--|:--|:--|:--|:--|:--|
${"\n".join([f"|{x['divisionRank']}|{x['team']['name']}|{x['leagueRecord']['wins']}|{x['leagueRecord']['losses']}|{x['leagueRecord']['ot']}|{x['points']}|" for x in myDivStandings])}