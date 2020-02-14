## loop through gamePks for game info, pass gamePk into each template
% for pk in (x for x in data.keys() if x!=0):
% if data[pk]['schedule'].get('seriesDescription') and data[pk]['schedule'].get('gameType') not in ['R','I','S','E']:
${'#' + data[pk]['schedule']['seriesDescription'] + ' '}\
${'Game ' + str(data[pk]['schedule']['seriesGameNumber']) + ' - ' if data[pk]['schedule'].get('seriesGameNumber') and data[pk]['schedule'].get('gamesInSeries',1) > 1 else ''}\
% else:
${'###'}\
% endif\
<%include file="matchup.mako" args="gamePk=pk,dateFormat='%I:%M %p %Z'" />

## Broadcasts, gameday link, (strikezone map commented out since it doesn't seem to have data), (game notes commented out due to new press pass requirement)
<%include file="game_info.mako" args="gamePk=pk" />

## probable pitchers
<%include file="probable_pitchers.mako" args="gamePk=pk" />

## lineups vs. probable pitchers
<%include file="lineups.mako" args="gamePk=pk,boxStyle=settings.get('Game Day Thread',{}).get('BOXSCORE_STYLE','wide')" />

## probable pitchers vs. teams
% endfor

% if data[0]['myTeam']['seasonState'] == 'regular':
<%include file="standings.mako" />
% endif

% if data[0]['myTeam']['seasonState'] != 'post:in':
## division scoreboard
${'###Around the Division' if any(x for x in data[0]['leagueSchedule'] if data[0]['myTeam']['division']['id'] in [x['teams']['away']['team']['division']['id'], x['teams']['home']['team']['division']['id']] and x['gamePk'] not in data.keys()) else 'Around the Division: There are no other division teams playing!'}
<%include file="division_scoreboard.mako" />
% else:
## league scoreboard
${'###Around the League' if any(x for x in data[0]['leagueSchedule'] if x['gamePk'] not in data.keys()) else 'Around the League: There are no other games!'}
<%include file="league_scoreboard.mako" args="gamePk=list(data.keys())" />
% endif


## Configurable footer text
${settings.get('Game Day Thread',{}).get('FOOTER','')}
