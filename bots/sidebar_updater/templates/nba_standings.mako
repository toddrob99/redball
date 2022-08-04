<%
    from datetime import datetime
    if not len(standings.standings):
        return
    myConfStandings = [x for x in standings.standings if x.conference == my_team.team_info.team_conference][:num_to_show]
    conf_labels = {
        "East": "Eastern",
        "West": "Western",
    }
%>\
[](/redball/standings)\
${conf_labels.get(my_team.team_info.team_conference, my_team.team_info.team_conference)} Conference Standings
-------
|Team|W|L|GB|L10|Strk|
|:--|:-:|:-:|:-:|:-:|:-:|
${"\n".join([f"|{i+1} \
[{x.teamname}]({team_subs[x.teamid]})|\
{x.wins}|{x.losses}|{'-' if str(x.conferencegamesback) == '0.0' else x.conferencegamesback}|{x.l10.strip()}|{x.strcurrentstreak.replace(' ', '')}|" for i, x in enumerate(myConfStandings)])}

^Updated: ^${datetime.now().strftime("%Y-%m-%d ^%H:%M")}

[**Complete and Current NBA Standings**](https://www.espn.com/nba/standings)
[](/redball/standings)