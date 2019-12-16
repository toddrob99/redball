<%
    from datetime import datetime
    import tzlocal

    if len(data[0]['myTeam']['nextGame']):
        daysTilNextGame = (data[0]['myTeam']['nextGame']['gameTime']['bot'] - tzlocal.get_localzone().localize(datetime.today())).days
    else:
        daysTilNextGame = -1
%>
% if len(data[0]['myTeam']['nextGame']):
**Next ${data[0]['myTeam']['teamName']} Game**: \
${data[0]['myTeam']['nextGame']['gameTime']['myTeam'].strftime('%a, %b %d, %I:%M %p %Z')}\
${' @ ' + data[0]['myTeam']['nextGame']['teams']['home']['team']['teamName'] if data[0]['myTeam']['nextGame']['teams']['away']['team']['id']==data[0]['myTeam']['id'] else ' vs. ' + data[0]['myTeam']['nextGame']['teams']['away']['team']['teamName']}\
% if daysTilNextGame > 0:
 (${daysTilNextGame} day${'s' if daysTilNextGame>1 else ''})
% endif
% endif