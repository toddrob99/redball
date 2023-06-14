## loop through gamePks for game info, pass gamePk into each template
% for pk in (x for x in data.keys() if x!=0):
% if data[pk]['schedule'].get('seriesDescription') and data[pk]['schedule'].get('gameType') not in ['R','I','S','E']:
${'# ' + data[pk]['schedule']['seriesDescription'] + ' '}\
${'Game ' + str(data[pk]['schedule']['seriesGameNumber']) + ' - ' if data[pk]['schedule'].get('seriesGameNumber') and data[pk]['schedule'].get('gamesInSeries',1) > 1 else '- '}\
% else:
${'### '}\
% endif
<%include file="matchup.mako" args="gamePk=pk,dateFormat='%I:%M %p %Z'" />

## Game status: show detailed state and then list first pitch time if game hasn't started yet and isn't final
${'### '}Game Status: ${data[pk]['schedule']['status']['detailedState']} \
% if data[pk]['schedule']['status'].get('reason') and len(data[pk]['schedule']['status']['reason']) > 0 and data[pk]['schedule']['status']['reason'] not in data[pk]['schedule']['status']['detailedState']:
due to ${data[pk]['schedule']['status']['reason']} \
% endif

## Broadcasts, gameday link, (strikezone map commented out since it doesn't seem to have data), (game notes commented out due to new press pass requirement)
<%include file="game_info.mako" args="gamePk=pk" />

## probable pitchers
<%include file="probable_pitchers.mako" args="gamePk=pk" />

## lineups vs. probable pitchers
<%include file="lineups.mako" args="gamePk=pk,boxStyle=settings.get('Game Day Thread',{}).get('BOXSCORE_STYLE','wide')" />

## probable pitchers vs. teams
% endfor

<%
    wc_standings = settings.get('Game Day Thread',{}).get('WILDCARD_STANDINGS', False)
    wc_scoreboard = settings.get('Game Day Thread',{}).get('WILDCARD_SCOREBOARD', False)
    wc_num = settings.get('Game Day Thread',{}).get('WILDCARD_NUM_TO_SHOW', 5)
%>\
% if data[0]['myTeam']['seasonState'] == 'regular' and data[pk]['schedule']['gameType'] == "R":
<%include file="standings.mako" args="include_wc=wc_standings,wc_num=wc_num"/>
% endif

% if data[0]['myTeam'].get('division'):  # will skip for All Star teams
% if data[0]['myTeam']['seasonState'] != 'post:in':
## division scoreboard
<%include file="division_scoreboard.mako" args="gamePk=list(data.keys()),include_wc=wc_scoreboard,wc_num=wc_num" />
% else:
## league scoreboard
${'###  Around the League' if any(x for x in data[0]['leagueSchedule'] if x['gamePk'] not in data.keys()) else 'Around the League: There are no other games!'}
<%include file="league_scoreboard.mako" args="gamePk=list(data.keys())" />
% endif
% endif

## Configurable footer text
${settings.get('Game Day Thread',{}).get('FOOTER','')}
