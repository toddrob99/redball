<%
    if not len(data["standings"].standings):
        return
    myDivStandings = [x for x in data["standings"].standings if x.division == data["myTeam"].team_info.team_division]
%>\
${'##'} ${data["myTeam"].team_info.team_division} Division Standings
|Rank|Team|Wins|Losses|Win %|Div GB|Conf|Div|
|:--|:--|:--|:--|:--|:--|:--|:--|
${"\n".join([f"|{x.divisionrank}|\
[{x.teamcity} {x.teamname}]({data['teamSubsById'][x.teamid]})|\
{x.wins}|{x.losses}|{x.winpct}|{x.divisiongamesback}|{x.conferencerecord.strip()}|{x.divisionrecord.strip()}|" for x in myDivStandings])}
