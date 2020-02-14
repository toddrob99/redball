<%
    from datetime import datetime
    prefix = settings.get("Game Thread", {}).get("TITLE_PREFIX","Game Thread:")
%>\
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
%if data[gamePk]['schedule'].get('seriesDescription') and data[gamePk]['schedule'].get('gameType') not in ['R','I','S','E']:
${data[gamePk]['schedule']['seriesDescription'] + ' '}\
${'Game ' + str(data[gamePk]['schedule']['seriesGameNumber']) + ' - ' if data[gamePk]['schedule'].get('seriesGameNumber') and data[gamePk]['schedule'].get('gamesInSeries',1) > 1 else ''}\
%endif
${data[gamePk]['schedule']['teams']['away']['team']['teamName']} (${data[gamePk]['schedule']['teams']['away']['leagueRecord']['wins']}-${data[gamePk]['schedule']['teams']['away']['leagueRecord']['losses']})\
 @ ${data[gamePk]['schedule']['teams']['home']['team']['teamName']} (${data[gamePk]['schedule']['teams']['home']['leagueRecord']['wins']}-${data[gamePk]['schedule']['teams']['home']['leagueRecord']['losses']})\
 - ${data[gamePk]['gameTime']['myTeam'].strftime('%a, %b %d @ %I:%M %p %Z')}