<%page args="gamePk=0" />
## All MLB games (except current gamePk when applicable)
<%
    from datetime import datetime
    import pytz
    if isinstance(gamePk, int):
        gamePks = [gamePk]
    elif isinstance(gamePk, list):
        gamePks = [x for x in gamePk]
    else:
        gamePks = [0]
%>\
% for x in (x for x in data[0]['leagueSchedule'] if x['gamePk'] not in gamePks):
${x['teams']['away']['team']['abbreviation']} ${x['teams']['away'].get('score',0) if x['status']['abstractGameCode'] in ['L','F'] else ''} @ \
${x['teams']['home']['team']['abbreviation']} ${x['teams']['home'].get('score',0) if x['status']['abstractGameCode'] in ['L','F'] else ''} \
% if x['status']['statusCode'] == 'PW':
Warmup
% elif x['gameTime']['utc'] > datetime.utcnow().replace(tzinfo=pytz.utc) and x['status']['abstractGameCode'] != 'F':
${x['gameTime']['myTeam'].strftime('%I:%M %p %Z')}
% elif x['status']['abstractGameCode'] == 'L':
- ${x['linescore']['inningState']} ${x['linescore']['currentInning']}${((', ' + str(x['linescore']['outs']) + ' Out') + ('s' if x['linescore']['outs']!=1 else '')) if x['linescore']['inningState'] in ['Top','Bottom'] else ''}
% elif x['status']['abstractGameCode'] == 'F':
- ${x['status']['detailedState']}
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