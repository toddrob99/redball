<%
    from datetime import datetime
    prefix = settings.get("Game Thread", {}).get("TITLE_PREFIX","Game Thread:")
    dateFormat = settings.get("Game Thread", {}).get("DATE_FORMAT","%a, %b %d @ %I:%M %p %Z")
    dhDateFormat = settings.get("Game Thread", {}).get("DATE_FORMAT_DH","%a, %b %d")
%>\
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
%if data[gamePk]['schedule'].get('seriesDescription') and data[gamePk]['schedule'].get('gameType') not in ['R','I','S','E']:
${data[gamePk]['schedule']['seriesDescription'] + ' '}\
${'Game ' + str(data[gamePk]['schedule']['seriesGameNumber']) + ' - ' if data[gamePk]['schedule'].get('seriesGameNumber') and data[gamePk]['schedule'].get('gamesInSeries',1) > 1 else '- '}\
%endif
%if data[0]["myTeam"].get("allStarStatus"):
${data[gamePk]['schedule']['teams']['away']['team']['teamName']} @ ${data[gamePk]['schedule']['teams']['home']['team']['teamName']}\
%else:
${data[gamePk]['schedule']['teams']['away']['team']['teamName']} (${data[gamePk]['schedule']['teams']['away']['leagueRecord']['wins']}-${data[gamePk]['schedule']['teams']['away']['leagueRecord']['losses']})\
 @ ${data[gamePk]['schedule']['teams']['home']['team']['teamName']} (${data[gamePk]['schedule']['teams']['home']['leagueRecord']['wins']}-${data[gamePk]['schedule']['teams']['home']['leagueRecord']['losses']})\
%endif
%if data[gamePk]['schedule']['doubleHeader'] == 'Y' and data[gamePk]['schedule']['gameNumber'] == 2:
 - ${data[gamePk]['gameTime']['myTeam'].strftime(dhDateFormat)} - Doubleheader Game 2
%else:
 - ${data[gamePk]['gameTime']['myTeam'].strftime(dateFormat)}
%endif
%if data[gamePk]['schedule']['doubleHeader'] == 'S':
 - Doubleheader Game ${data[gamePk]['schedule']['gameNumber']}
%endif