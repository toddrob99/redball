<%page args="gamePk=0,include_wc=False,wc_num=5" />
## My team's division games
<%
    from datetime import datetime
    import pytz
    if isinstance(gamePk, int):
        gamePks = [gamePk]
    elif isinstance(gamePk, list):
        gamePks = [x for x in gamePk]
    else:
        gamePks = [0]
    if include_wc:
        wc_teams = []
        wc_temp = []
        for d in data[0]['standings'].values():
            for t in d["teams"]:
                if t.get("wc_rank") != "-" and int(t.get("wc_rank", 0)) <= wc_num:
                    wc_teams.append(t["team_id"])
                    wc_temp.append({"rank": t["wc_rank"], "id": t["team_id"], "name": t["name"]})
    divGames = [
        x for x in data[0]['leagueSchedule'] 
        if (
            data[0]['myTeam']['division']['id']
            in [
                x['teams']['away']['team'].get('division',{}).get('id'),
                x['teams']['home']['team'].get('division',{}).get('id')
            ] or (
                include_wc
                and data[0]['myTeam']['league']['id'] in [
                    x['teams']['away']['team'].get('league',{}).get('id'),
                    x['teams']['home']['team'].get('league',{}).get('id')
                ] and any(
                    True for i in wc_teams if i in [
                        x['teams']['away']['team'].get('id'),
                        x['teams']['home']['team'].get('id')
                    ]
                )
            )
        ) and x['gamePk'] not in gamePks
    ]
    if not len(divGames):
        if include_wc:
            title = 'Division & Wild Card Scoreboard: There are no other games!'
        else:
            title = 'Around the Division: There are no other division teams playing!'
    else:
        if include_wc:
            title = '###Division & Wild Card Scoreboard'
        else:
            title = '###Division Soreboard'
%>\
${title}
% for x in divGames:
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