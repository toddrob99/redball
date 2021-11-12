<%
    from datetime import datetime
    if not len(standings):
        return
    myDivStandings = next((
        x["teamRecords"]
        for x in standings
        if x["division"]["id"] == my_team["division"]["id"]
    ), [])[:num_to_show]
%>\
[](/redball/standings)\
${my_team["division"]["nameShort"]} Division Standings
--------

|Team|W|L|OT|Pts|
|:--|:-:|:-:|:-:|:-:|
${"\n".join([f"|[{x['team']['name']}]({team_subs[x['team']['id']]})|\
{x['leagueRecord']['wins']}|{x['leagueRecord']['losses']}|{x['leagueRecord']['ot']}|{x['points']}|" for x in myDivStandings])}

^Updated: ^${datetime.now().strftime("%Y-%m-%d ^%H:%M")}[](/redball/standings)