<%page args="gamePk=0" />
## Games across the league that are currently no-hitters or perfect (excluding current gamePk)
<%
    games = (x for x in data[0]['leagueSchedule'] if data[0]['myTeam']['id'] not in [x['teams']['away']['team']['id'], x['teams']['home']['team']['id']] and ((x['status']['abstractGameCode'] == 'L' and x['status']['statusCode'] != 'PW') or (x['status']['abstractGameCode'] == 'F' and x['status']['codedGameState'] not in ['C','D'])) and x.get('linescore',{}).get('currentInning',0) > 4 and (x['flags'].get('noHitter') or x['flags'].get('perfectGame')) and x['gamePk'] != gamePk)
%>
% for x in games:
% if x['flags'].get('perfectGame'):
${'###Perfect Game Alert'}

|${x['linescore']['inningState'][0] + ' ' + str(x['linescore']['currentInning']) if x['status']['abstractGameCode'] == 'L' else x['status']['detailedState']}|R|H|E|
|:--|:--|:--|:--|
|${x['teams']['away']['team']['teamName']}|${x['linescore']['teams']['away'].get('runs',0)}|${x['linescore']['teams']['away'].get('hits',0)}|${x['linescore']['teams']['away'].get('errors',0)}|
|${x['teams']['home']['team']['teamName']}|${x['linescore']['teams']['home'].get('runs',0)}|${x['linescore']['teams']['home'].get('hits',0)}|${x['linescore']['teams']['home'].get('errors',0)}|

% elif x['flags'].get('noHitter'):
${'###No-Hitter Alert'}

|${x['linescore']['inningState'][0] + ' ' + str(x['linescore']['currentInning']) if x['status']['abstractGameCode'] == 'L' else x['status']['detailedState']}|R|H|E|
|:--|:--|:--|:--|
|${x['teams']['away']['team']['teamName']}|${x['linescore']['teams']['away'].get('runs',0)}|${x['linescore']['teams']['away'].get('hits',0)}|${x['linescore']['teams']['away'].get('errors',0)}|
|${x['teams']['home']['team']['teamName']}|${x['linescore']['teams']['home'].get('runs',0)}|${x['linescore']['teams']['home'].get('hits',0)}|${x['linescore']['teams']['home'].get('errors',0)}|

% endif
% endfor
##${x['teams']['away']['team']['league']['abbreviation']}
##${x['teams']['away']['team']['division']['abbreviation']}
##${x['teams']['home']['team']['league']['abbreviation']}
##${x['teams']['home']['team']['division']['abbreviation']}
## codedGameState - Suspended: U, T; Cancelled: C, Postponed: D
##${x['status']['codedGameState']}
##${x['status']['abstractGameState']}
##${x['status']['abstractGameCode']}
##${x['status']['statusCode']}
##${x['flags']['noHitter']}
##${x['flags']['perfectGame']}
##((x['status']['abstractGameCode'] == 'L' and x['status']['statusCode'] != 'PW') or (x['status']['abstractGameCode'] == 'F' and x['status']['codedGameState'] not in ['C','D']))