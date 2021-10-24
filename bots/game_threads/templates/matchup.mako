<%page args="gamePk,dateFormat='%a, %b %d @ %I:%M %p %Z'" />\
## Matchup header: Team names with links to team subs and matchup image, followed by game date
[${data[gamePk]['schedule']['teams']['away']['team']['teamName']}](${data[0]['teamSubs'].get(data[gamePk]['schedule']['teams']['away']['team']['id'], data[0]['teamSubs'][0])}) \
%if settings.get("Bot", {}).get("SUPPRESS_MATCHUP_IMAGE", False) or data[gamePk]['schedule']['teams']['away']['team']['fileCode'] + data[gamePk]['schedule']['teams']['home']['team']['fileCode'] == 'laatl':
@ \
%else:
[@](http://mlb.mlb.com/images/2017_ipad/684/${data[gamePk]['schedule']['teams']['away']['team']['fileCode'] + data[gamePk]['schedule']['teams']['home']['team']['fileCode']}_684.jpg) \
%endif
[${data[gamePk]['schedule']['teams']['home']['team']['teamName']}](${data[0]['teamSubs'].get(data[gamePk]['schedule']['teams']['home']['team']['id'], data[0]['teamSubs'][0])}) \
%if data[gamePk]['schedule']['doubleHeader'] == 'Y' and data[gamePk]['schedule']['gameNumber'] == 2:
- ${data[gamePk]['gameTime']['myTeam'].strftime('%a, %b %d')} - Doubleheader Game 2
%else:
- ${data[gamePk]['gameTime']['myTeam'].strftime(dateFormat)} \
%endif
%if data[gamePk]['schedule']['doubleHeader'] == 'S':
- Doubleheader Game ${data[gamePk]['schedule']['gameNumber']}
%endif