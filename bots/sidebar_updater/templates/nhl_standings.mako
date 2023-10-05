<%
    from datetime import datetime
    if not len(standings):
        return
    myDivStandings = [x for x in standings if x.get("divisionAbbrev") == my_team.get("divisionAbbrev", "UNK")][:num_to_show]
%>\
[](/redball/standings)\
${my_team["divisionName"]} Division Standings
--------


|Rank|Team|W|L|OT|Pts|
|:--|:--|:--|:--|:--|:--|
% for x in myDivStandings:
|${x["divisionSequence"]}|\
[${next((t['commonName'] for t in all_teams if t['abbrev'] == x['teamAbbrev']['default']), x['teamAbbrev']['default'])}](${team_subs.get(x["teamAbbrev"]["default"], "")})|\
${x["wins"]}|${x["losses"]}|${x["otLosses"]}|${x["points"]}|
% endfor

^Updated: ^${datetime.now().strftime("%Y-%m-%d ^%H:%M")}[](/redball/standings)