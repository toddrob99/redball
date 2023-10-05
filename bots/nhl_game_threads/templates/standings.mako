<%
    if not len(data["standings"]) or data["game"].get("gameType") != 2:
        return
    myDivStandings = [x for x in data["standings"] if x.get("divisionAbbrev") == data["myTeam"].get("divisionAbbrev", "UNK")]
%>\
${'##'} ${data["myTeam"]["divisionName"]} Standings
|Rank|Team|Wins|Losses|OT|Points|
|:--|:--|:--|:--|:--|:--|
% for x in myDivStandings:
|${x["divisionSequence"]}|\
[${x["teamName"]["default"]}]({data["teamSubs"][x["teamAbbrev"]]})|\
${x["wins"]}|${x["losses"]}|${x["otLosses"]}|${x["points"]}|
% endfor