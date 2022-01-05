<%
    from datetime import datetime
    if not standings.get(my_team['division']['id']):
        return
%>\
[](/redball/standings)\
## Standings for myTeam's division only:
${my_team['division']['nameShort']} Standings
--------

|Team|Wins|Losses|GB|
|:--|:-:|:-:|:-:|
% for t in standings[my_team['division']['id']]['teams'][:num_to_show]:
|[${next((x['teamName'] for x in all_teams if x['id'] == t['team_id']), t['name'])}](${team_subs[t['team_id']]})|${t['w']}|${t['l']}|${t['gb']}|
% endfor
^Updated: ^${datetime.now().strftime("%Y-%m-%d ^%H:%M")}[](/redball/standings)
