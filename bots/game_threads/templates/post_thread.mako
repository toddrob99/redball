<%
    from datetime import datetime
    import pytz
%>\
## Header: Team names with links to team subs and matchup image, followed by game date
${'#'}<%include file="matchup.mako" args="dateFormat='%a, %b %d'" />

## Game status: show detailed state and final score
${'###'}Game Status: ${data[gamePk]['schedule']['status']['detailedState']} \
- <%include file="score.mako" />

## Weather, gameday link, (strikezone map commented out since it doesn't seem to have data), (game notes commented out due to new press pass requirement)
<%include file="post_game_info.mako" />

<%include file="boxscore.mako" args="boxStyle=settings.get('Post Game Thread',{}).get('BOXSCORE_STYLE','wide')" />

<%include file="scoring_plays.mako" />

<%include file="highlights.mako" />

<%include file="linescore.mako" />

% if data[0]['myTeam']['seasonState'].startswith('post'):
## league scoreboard during post season
${'###Around the League' if any(x for x in data[0]['leagueSchedule'] if x['gamePk'] != gamePk) else 'Around the League: There are no other games!'}
<%include file="league_scoreboard.mako" args="gamePk=gamePk" />
% else:
## division scoreboard during pre and regular season
${'###Around the Division' if any(x for x in data[0]['leagueSchedule'] if data[0]['myTeam']['division']['id'] in [x['teams']['away']['team'].get('division',{}).get('id'), x['teams']['home']['team'].get('division',{}).get('id')] and x['gamePk'] != gamePk) else 'Around the Division: There are no other division teams playing!'}
<%include file="division_scoreboard.mako" args="gamePk=gamePk" />
% endif

## no-no/perfecto watch - whole league
<%include file="no-no_watch.mako" />

## Next game
<%include file="next_game.mako" />

## Configurable footer text
${settings.get('Post Game Thread',{}).get('FOOTER','')}
