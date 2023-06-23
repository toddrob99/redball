% if data[0]['myTeam']['seasonState'] in ['pre','regular']:
${'**Around the Division**' if any(x for x in data[0]['leagueSchedule'] if data[0]['myTeam']['division']['id'] in [x['teams']['away']['team'].get('division',{}).get('id'), x['teams']['home']['team'].get('division',{}).get('id')]) else 'Around the Division: There are no other division teams playing!'}
<%include file="division_scoreboard.mako" />

% if data[0]['myTeam']['seasonState'] == 'regular':
<%include file="standings.mako" />
% endif
% elif data[0]['myTeam']['seasonState'] in ['off:before', 'off:after']:

% elif data[0]['myTeam']['seasonState'] in ['post:out', 'post:in']:
${'### Around the League' if len(data[0]['leagueSchedule']) else 'Around the League: There are no games today!'}
<%include file="league_scoreboard.mako" args="gamePk='off'"/>
% endif

## no-no/perfecto watch
<%include file="no-no_watch.mako" />

% if data[0]['myTeam']['seasonState'] not in ['post:out']:
<%include file="next_game.mako" />
% endif

${settings.get('Off Day Thread',{}).get('FOOTER','')}
