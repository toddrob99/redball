<%
    from datetime import datetime 
    prefix = settings.get("Post Game Thread", {}).get("TITLE_PREFIX","")
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
The ${data[0]['myTeam']['teamName']} Game is ${data[gamePk]['schedule']['status']['detailedState']}\
% else:
% if data[gamePk]['schedule']['teams']['home']['score'] == data[gamePk]['schedule']['teams']['away']['score']:
## Tie
The ${data[0]['myTeam']['teamName']} tied the ${data[gamePk]['oppTeam']['teamName']} with a score of ${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}-${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}\
% elif data[gamePk]['schedule']['teams']['home']['score'] > data[gamePk]['schedule']['teams']['away']['score']:
## Home Team Won
% if data[gamePk]['homeAway'] == 'home':
## Home Win
The ${data[0]['myTeam']['teamName']} defeated the ${data[gamePk]['oppTeam']['teamName']} by a score of ${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}-${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}\
% else:
## Home Loss
The ${data[0]['myTeam']['teamName']} fell to the ${data[gamePk]['oppTeam']['teamName']} by a score of ${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}-${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}\
% endif
% elif data[gamePk]['schedule']['teams']['away']['score'] > data[gamePk]['schedule']['teams']['home']['score']:
## Away Team Won
% if data[gamePk]['homeAway'] == 'away':
## Road Win
The ${data[0]['myTeam']['teamName']} defeated the ${data[gamePk]['oppTeam']['teamName']} by a score of ${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}-${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}\
% else:
## Road Loss
The ${data[0]['myTeam']['teamName']} fell to the ${data[gamePk]['oppTeam']['teamName']} by a score of ${data[gamePk]['schedule']['teams']['home' if data[gamePk]['homeAway']=='away' else 'away']['score']}-${data[gamePk]['schedule']['teams'][data[gamePk]['homeAway']]['score']}\
% endif
% else:
## Unknown game state, use generic <TeamName> Post Game Thread title
${data[0]['myTeam']['teamName']} Post Game Thread\
% endif
% endif
\
 - ${data[gamePk]['gameTime']['myTeam'].strftime('%a, %b %d @ %I:%M %p %Z')}