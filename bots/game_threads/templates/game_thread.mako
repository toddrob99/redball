<%
    from datetime import datetime
    import pytz
%>\
## Header: Team names with links to team subs and matchup image, followed by game date
${'#'}<%include file="matchup.mako" args="dateFormat='%a, %b %d'" />

## Game status: show detailed state and then list first pitch time if game hasn't started yet and isn't final
${'###'}Game Status: ${data[gamePk]['schedule']['status']['detailedState']} \
% if data[gamePk]['schedule']['status'].get('reason') and len(data[gamePk]['schedule']['status']['reason']) > 0 and data[gamePk]['schedule']['status']['reason'] not in data[gamePk]['schedule']['status']['detailedState']:
due to ${data[gamePk]['schedule']['status']['reason']} \
% endif
% if data[gamePk]['gameTime']['utc'] > datetime.utcnow().replace(tzinfo=pytz.utc) and data[gamePk]['schedule']['status']['abstractGameCode'] != 'F':
- First Pitch is scheduled for ${data[gamePk]['gameTime']['myTeam'].strftime('%I:%M %p %Z')}

% elif (data[gamePk]['schedule']['status']['abstractGameCode'] == 'L' and data[gamePk]['schedule']['status']['statusCode'] != 'PW') or (data[gamePk]['schedule']['status']['abstractGameCode'] == 'F' and data[gamePk]['schedule']['status']['codedGameState'] not in ['C','D']):
## Game status is live and not warmup, so include info about inning and outs on the game status line
- <%include file="score.mako" />\
% if data[gamePk]['schedule']['status']['abstractGameCode'] != 'F':
## Only include inning if game is in progress (status!=F since we're already inside the other condition)
 - ${data[gamePk]['schedule']['linescore']['inningState']} of the ${data[gamePk]['schedule']['linescore']['currentInningOrdinal']} \
% endif
${'- ' + str(data[gamePk]['schedule']['linescore']['outs']) + ' out' + ('s' if data[gamePk]['schedule']['linescore']['outs'] != 1 else '') if data[gamePk]['schedule']['linescore']['outs'] < 3 else ''}

## current pitcher/batter matchup, count, on deck, in hole -- or due up
% endif

## Broadcasts, gameday link, (strikezone map commented out since it doesn't seem to have data), (game notes commented out due to new press pass requirement)
<%include file="game_info.mako" />

## Game status is not final or live (except warmup), include standings, probable pitchers, lineups if posted
% if (data[gamePk]['schedule']['status']['abstractGameCode'] != 'L' or data[gamePk]['schedule']['status']['statusCode'] == 'PW') and data[gamePk]['schedule']['status']['abstractGameCode'] != 'F':
% if data[0]['myTeam']['seasonState'] == 'regular':
<%include file="standings.mako" />
% endif

<%include file="probable_pitchers.mako" />

<%include file="lineups.mako" args="boxStyle=settings.get('Game Thread',{}).get('BOXSCORE_STYLE','wide')" />
% endif


## If game status is final, or live and not warmup, include boxscore, scoring plays, highlights, and linescore
% if (data[gamePk]['schedule']['status']['abstractGameCode'] == 'L' and data[gamePk]['schedule']['status']['statusCode'] != 'PW') or data[gamePk]['schedule']['status']['abstractGameCode'] == 'F':
<%include file="boxscore.mako" args="boxStyle=settings.get('Game Thread',{}).get('BOXSCORE_STYLE','wide')" />

<%include file="scoring_plays.mako" />

<%include file="highlights.mako" />

<%include file="linescore.mako" />
% endif

% if data[0]['myTeam']['seasonState'] != 'post:in':
## division scoreboard
${'###Around the Division' if any(x for x in data[0]['leagueSchedule'] if data[0]['myTeam']['division']['id'] in [x['teams']['away']['team'].get('division',{}).get('id'), x['teams']['home']['team'].get('division',{}).get('id')] and x['gamePk'] != gamePk) else 'Around the Division: There are no other division teams playing!'}
<%include file="division_scoreboard.mako" args="gamePk=gamePk" />
% else:
## league scoreboard
${'###Around the League' if any(x for x in data[0]['leagueSchedule'] if x['gamePk'] != gamePk) else 'Around the League: There are no other games!'}
<%include file="league_scoreboard.mako" args="gamePk=gamePk" />
% endif

## no-no/perfecto watch
<%include file="no-no_watch.mako" />


## configurable footer text
${settings.get('Game Thread',{}).get('FOOTER','')}
