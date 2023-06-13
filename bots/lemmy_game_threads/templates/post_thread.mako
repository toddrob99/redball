<%
    from datetime import datetime
    import pytz
%>\
## Header: Team names with links to team subs and matchup image, followed by game date
${'#'}<%include file="matchup.mako" args="dateFormat='%a, %b %d'" />

## Game status: show detailed state and final score
${'###'}Game Status: ${data[gamePk]['schedule']['status']['detailedState']} \
% if data[gamePk]['schedule']['status'].get('reason') and len(data[gamePk]['schedule']['status']['reason']) > 0 and data[gamePk]['schedule']['status']['reason'] not in data[gamePk]['schedule']['status']['detailedState']:
due to ${data[gamePk]['schedule']['status']['reason']} \
% endif
% if data[gamePk]['schedule']['status']['abstractGameCode'] == 'F' and data[gamePk]['schedule']['status']['codedGameState'] not in ['C','D']:
- <%include file="score.mako" />
% endif

## Weather, gameday link, (strikezone map commented out since it doesn't seem to have data), (game notes commented out due to new press pass requirement)
<%include file="post_game_info.mako" />

<%include file="boxscore.mako" args="boxStyle=settings.get('Post Game Thread',{}).get('BOXSCORE_STYLE','wide')" />

% if not settings.get('Post Game Thread',{}).get('SUPPRESS_SCORING_PLAYS', False):
<%include file="scoring_plays.mako" />

% endif
<%include file="highlights.mako" />

<%include file="linescore.mako" />

% if not settings.get('Post Game Thread',{}).get('SUPPRESS_DECISIONS', False):
<%include file="decisions.mako" />

% endif
% if data[0]['myTeam'].get('division'):  # will skip for All Star teams
% if data[0]['myTeam']['seasonState'].startswith('post'):
## league scoreboard during post season
${'###Around the League' if any(x for x in data[0]['leagueSchedule'] if x['gamePk'] != gamePk) else 'Around the League: There are no other games!'}
<%include file="league_scoreboard.mako" args="gamePk=gamePk" />
% else:
<%
    wc = settings.get('Game Thread',{}).get('WILDCARD_SCOREBOARD', False)
    wc_num = settings.get('Game Thread',{}).get('WILDCARD_NUM_TO_SHOW', 5)
%>\
## division scoreboard during pre and regular season
<%include file="division_scoreboard.mako" args="gamePk=gamePk,include_wc=wc,wc_num=wc_num" />
% endif
% endif

## no-no/perfecto watch - whole league
<%include file="no-no_watch.mako" />

## Next game
<%include file="next_game.mako" />

## Configurable footer text
${settings.get('Post Game Thread',{}).get('FOOTER','')}
