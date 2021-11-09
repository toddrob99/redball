<%page args="num_to_show=8" />
<%
    if not len(data["standings"].standings):
        return
    myDivStandings = [x for x in data["standings"].standings if x.division == data["myTeam"].team_info.team_division]
%>\
${'##'} ${data["myTeam"].team_info.team_division} Division Standings
|Rank|Team|W|L|Pct|GB|Div|Home|Away|L10|Strk|
|:-:|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
${"\n".join([f"|{x.divisionrank}|\
[{x.teamcity} {x.teamname}]({data['teamSubsById'][x.teamid]})|\
{x.wins}|{x.losses}|{x.winpct}|{'-' if str(x.divisiongamesback) == '0.0' else x.divisiongamesback}|{x.divisionrecord.strip()}|{x.home.strip()}|{x.road.strip()}|{x.l10.strip()}|{x.strcurrentstreak.strip()}|" for x in myDivStandings][:num_to_show])}
