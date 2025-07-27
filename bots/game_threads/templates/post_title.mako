<%
    from datetime import datetime 
    prefix = settings.get("Post Game Thread", {}).get("TITLE_PREFIX","")
    dateFormat = settings.get("Post Game Thread", {}).get("DATE_FORMAT","%a, %b %d @ %I:%M %p %Z")
    dhDateFormat = settings.get("Post Game Thread", {}).get("DATE_FORMAT_DH","%a, %b %d")
%>\
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
% if data[gamePk]['schedule'].get('seriesDescription') and data[gamePk]['schedule'].get('gameType') not in ['R','I','S','E']:
${data[gamePk]['schedule']['seriesDescription']}\
${' Game ' + str(data[gamePk]['schedule']['seriesGameNumber']) if data[gamePk]['schedule'].get('seriesGameNumber') and data[gamePk]['schedule'].get('gamesInSeries',1) > 1 else ''}\
 - \
% endif
\
% if data[gamePk]['schedule']['status']['codedGameState'] in ['U','T','C','D']:
## Exception Status (codedGameState - Suspended: U, T; Cancelled: C, Postponed: D)
${settings.get("Post Game Thread", {}).get("TITLE_PREFIX_EXCEPTION","")}The ${data[0]['myTeam']['teamName']} Game is ${data[gamePk]['schedule']['status']['detailedState']}\
% else:
% if data[gamePk]['schedule']['teams']['home']['score'] == data[gamePk]['schedule']['teams']['away']['score']:
## Tie
${settings.get("Post Game Thread", {}).get("TITLE_PREFIX_TIE","")}The ${data[0]['myTeam']['teamName']} tied the ${data[gamePk]['oppTeam']['teamName']} with a score of ${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}-${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}\
% elif data[gamePk]['schedule']['teams']['home']['score'] > data[gamePk]['schedule']['teams']['away']['score']:
## Home Team Won
% if data[gamePk]['homeAway'] == 'home':
## Home Win
${settings.get("Post Game Thread", {}).get("TITLE_PREFIX_HOME_WIN","")}The ${data[0]['myTeam']['teamName']} defeated the ${data[gamePk]['oppTeam']['teamName']} by a score of ${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}-${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}\
% else:
## Home Loss
${settings.get("Post Game Thread", {}).get("TITLE_PREFIX_HOME_LOSS","")}The ${data[0]['myTeam']['teamName']} fall to the ${data[gamePk]['oppTeam']['teamName']} by a score of ${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}-${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}\
% endif
% elif data[gamePk]['schedule']['teams']['away']['score'] > data[gamePk]['schedule']['teams']['home']['score']:
## Away Team Won
% if data[gamePk]['homeAway'] == 'away':
## Road Win
${settings.get("Post Game Thread", {}).get("TITLE_PREFIX_ROAD_WIN","")}The ${data[0]['myTeam']['teamName']} defeated the ${data[gamePk]['oppTeam']['teamName']} by a score of ${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}-${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}\
% else:
## Road Loss
${settings.get("Post Game Thread", {}).get("TITLE_PREFIX_ROAD_LOSS","")}The ${data[0]['myTeam']['teamName']} fall to the ${data[gamePk]['oppTeam']['teamName']} by a score of ${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}-${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}\
% endif
% else:
## Unknown game state, use generic <TeamName> Post Game Thread title
${data[0]['myTeam']['teamName']} Post Game Thread\
% endif
% endif
\
%if data[gamePk]['schedule']['doubleHeader'] == 'Y' and data[gamePk]['schedule']['gameNumber'] == 2:
 - ${data[gamePk]['gameTime']['myTeam'].strftime(dhDateFormat)} - Doubleheader Game 2
%else:
 - ${data[gamePk]['gameTime']['myTeam'].strftime(dateFormat)}\
%endif
%if data[gamePk]['schedule']['doubleHeader'] == 'S':
 - Doubleheader Game ${data[gamePk]['schedule']['gameNumber']}
%endif