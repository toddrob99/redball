<%
    from datetime import datetime
    import pytz
%>\
## Header: Team names with links to team subs and matchup image, followed by game date
${'# '}<%include file="matchup.mako" args="dateFormat='%a, %b %d'" />

## Game status: show detailed state and then list first pitch time if game hasn't started yet and isn't final
${'### '}Game Status: ${data[gamePk]['schedule']['status']['detailedState']} \
% if data[gamePk]['schedule']['status'].get('reason') and len(data[gamePk]['schedule']['status']['reason']) > 0 and data[gamePk]['schedule']['status']['reason'] not in data[gamePk]['schedule']['status']['detailedState']:
due to ${data[gamePk]['schedule']['status']['reason']} \
% endif
% if data[gamePk]['gameTime']['utc'] > datetime.utcnow().replace(tzinfo=pytz.utc) and data[gamePk]['schedule']['status']['abstractGameCode'] != 'F':
%if not (data[gamePk]['schedule']['doubleHeader'] == 'Y' and data[gamePk]['schedule']['gameNumber'] == 2):
- First Pitch is scheduled for ${data[gamePk]['gameTime']['myTeam'].strftime('%I:%M %p %Z')}

% endif
% elif (data[gamePk]['schedule']['status']['abstractGameCode'] == 'L' and data[gamePk]['schedule']['status']['statusCode'] != 'PW') or (data[gamePk]['schedule']['status']['abstractGameCode'] == 'F' and data[gamePk]['schedule']['status']['codedGameState'] not in ['C','D']):
## Game status is live and not warmup, so include info about inning and outs on the game status line
- <%include file="score.mako" /> \
% if data[gamePk]['schedule']['status']['abstractGameCode'] != 'F':
## Only include inning if game is in progress (status!=F since we're already inside the other condition)

% if data[gamePk]['schedule']['linescore']['inningState'] == "Middle" and data[gamePk]['schedule']['linescore']['currentInningOrdinal'] == "7th":
Seventh inning stretch\
% else:
${data[gamePk]['schedule']['linescore']['inningState']} of the ${data[gamePk]['schedule']['linescore']['currentInningOrdinal']}\
% endif
## current pitcher/batter matchup, count, on deck, in hole -- or due up
<%
    currentPlay = data[gamePk]['gumbo']["liveData"].get('plays',{}).get('currentPlay',{})
    offense = data[gamePk]['gumbo']["liveData"].get('linescore',{}).get('offense',{})
    defense = data[gamePk]['gumbo']["liveData"].get('linescore',{}).get('defense',{})
    outs =currentPlay.get('count',{}).get('outs','0')
    comingUpTeamName = data[gamePk]['schedule']['teams']['away']['team']['teamName'] if data[gamePk]['schedule']['teams']['away']['team']['id'] == offense.get('team',{}).get('id') else data[gamePk]['schedule']['teams']['home']['team']['teamName']
%>\
% if outs == 3:
% if offense.get('batter',{}).get('fullName'):
## due up batter is in the data, so include them
${' '}with ${offense.get('batter',{}).get('fullName','*Unknown*')}, \
${offense.get('onDeck',{}).get('fullName','*Unknown')}, \
and ${offense.get('inHole',{}).get('fullName','*Unknown')} \
due up for the ${comingUpTeamName}
% else:
## due up batter is not in the data, so just put the team name due up
with the ${comingUpTeamName} coming up to bat
% endif
% else:
## else condition from if outs == 3--inning is in progress, so list outs, runners, matchup, on deck, and in hole
## Outs
, ${data[gamePk]['schedule']['linescore']['outs']} out${'s' if data[gamePk]['schedule']['linescore']['outs'] != 1 else ''}\
<%
    runners = (
        "bases empty" if not offense.get('first') and not offense.get('second') and not offense.get('third')
        else "runner on first" if offense.get('first') and not offense.get('second') and not offense.get('third')
        else "runner on second" if not offense.get('first') and offense.get('second') and not offense.get('third')
        else "runner on third" if not offense.get('first') and not offense.get('second') and offense.get('third')
        else "runners on first and second" if offense.get('first') and offense.get('second') and not offense.get('third')
        else "runners on first and third" if offense.get('first') and not offense.get('second') and offense.get('third')
        else "runners on second and third" if not offense.get('first') and offense.get('second') and offense.get('third')
        else "bases loaded" if offense.get('first') and offense.get('second') and offense.get('third')
        else None
    )
    ondeck = offense.get('onDeck',{}).get('fullName')
    inthehole = offense.get('inHole',{}).get('fullName')
%>\
${(', ' + runners) if runners else ''}\
## Count
, ${currentPlay.get('count',{}).get('balls','0')}-${currentPlay.get('count',{}).get('strikes','0')} count \
## Matchup
with ${currentPlay.get('matchup',{}).get('pitcher',{}).get('fullName','*Unknown*')} pitching and ${currentPlay.get('matchup',{}).get('batter',{}).get('fullName','*Unknown*')} batting. \
## Ondeck
% if ondeck:
${ondeck} is on deck\
## In hole
% if inthehole:
, and ${inthehole} is in the hole.
% endif
% endif
% endif
% endif
% endif

${'### '} Trash Talk Thread Rules

* Trash talk stays in this thread only, retaliating in other subs will result in a permanent ban
* Fans of all teams are welcome!
* Trash talk != direct personal insults
* No rooting for injuries
* No politics
* Upvote good trash talk
* Don’t downvote just because someone roots for another team
* Flair up, or else you will be mocked for being naked

## Broadcasts, gameday link, (strikezone map commented out since it doesn't seem to have data), (game notes commented out due to new press pass requirement)
<%include file="game_info.mako" />

## Game status is not final or live (except warmup), include standings, probable pitchers, lineups if posted
% if (data[gamePk]['schedule']['status']['abstractGameCode'] != 'L' or data[gamePk]['schedule']['status']['statusCode'] == 'PW') and data[gamePk]['schedule']['status']['abstractGameCode'] != 'F':
% if data[0]['myTeam']['seasonState'] == 'regular' and data[gamePk]['schedule']['gameType'] == "R":
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
${'### Around the Division' if any(x for x in data[0]['leagueSchedule'] if data[0]['myTeam']['division']['id'] in [x['teams']['away']['team'].get('division',{}).get('id'), x['teams']['home']['team'].get('division',{}).get('id')] and x['gamePk'] != gamePk) else 'Around the Division: There are no other division teams playing!'}
<%include file="division_scoreboard.mako" args="gamePk=gamePk" />
% else:
## league scoreboard
${'### Around the League' if any(x for x in data[0]['leagueSchedule'] if x['gamePk'] != gamePk) else 'Around the League: There are no other games!'}
<%include file="league_scoreboard.mako" args="gamePk=gamePk" />
% endif

## no-no/perfecto watch
<%include file="no-no_watch.mako" />


## configurable footer text
${settings.get('Game Thread',{}).get('FOOTER','')}
