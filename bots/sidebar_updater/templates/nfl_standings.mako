<%
    from datetime import datetime
    if not len(standings):
        return
    division_teams = [
        x
        for x in all_teams
        if x["divisionFullName"] == my_team["divisionFullName"]
    ]
    div_standings = sorted([x for x in standings if next((True for y in division_teams if x["team"]["id"] == y["id"]), False)], key=lambda t: t['division']['rank'])[:num_to_show]
%>\
[](/redball/standings)\
${my_team["divisionFullName"]} Standings
--------

|Team|W|L|T|Div|
|:--|:-:|:-:|:-:|:-:|
${"\n".join([f"|[{next((t['nickName'] for t in all_teams if t['id'] == x['team']['id']), x['team']['fullName'])}]({team_subs.get(next((t['nickName'] for t in all_teams if t['id'] == x['team']['id']), 'nfl'), '/r/nfl')})|\
{x['overall']['wins']}|{x['overall']['losses']}|{x['overall']['ties']}|{x['division']['wins']}-{x['division']['losses']}{('-' + str(x['division']['ties'])) if x['division']['ties'] else ''}|" for x in div_standings])}

^Updated: ^${datetime.now().strftime("%Y-%m-%d ^%H:%M")}[](/redball/standings)