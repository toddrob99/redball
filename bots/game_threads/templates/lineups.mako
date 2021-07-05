<%page args="gamePk,boxStyle='wide'" />
<%
    def playerLink(name, personId):
        if name=='' or personId==0: return ''
        return '[{}](http://mlb.mlb.com/team/player.jsp?player_id={})'.format(name,str(personId))

    if not len(data[gamePk]['gumbo']['liveData']['boxscore']['teams']['away']['batters']) and not len(data[gamePk]['gumbo']['liveData']['boxscore']['teams']['home']['batters']):
        # lineups not posted
        return

    if not len(data[gamePk]['awayBattersVsProb']):
        # no stats against probable pitcher, or no probable pitcher announced
        # just list the lineups
        awayLineupOnly = True
    else:
        awayLineupOnly = False

    if not len(data[gamePk]['homeBattersVsProb']):
        # no stats against probable pitcher, or no probable pitcher announced
        # just list the lineups
        homeLineupOnly = True
    else:
        homeLineupOnly = False

    awayBatters = data[gamePk]['gumbo']['liveData']['boxscore']['teams']['away']['batters']
    homeBatters = data[gamePk]['gumbo']['liveData']['boxscore']['teams']['home']['batters']
%>\
% if boxStyle.lower() == 'wide':
    ## Wide Batting Boxes
<%
    ##Make sure the home and away batter lists are the same length
    while len(awayBatters) > len(homeBatters):
        homeBatters.append(0)

    while len(awayBatters) < len(homeBatters):
        awayBatters.append(0)
%>\
## Build the box
% if len(awayBatters):
|${data[gamePk]['schedule']['teams']['away']['team']['teamName']} Lineup${' vs. ' + playerLink(data[gamePk]['gumbo']["gameData"]["players"]['ID'+str(data[gamePk]['schedule']['teams']['home']['probablePitcher']['id'])]['boxscoreName'],data[gamePk]['schedule']['teams']['home']['probablePitcher']['id']) + '|AVG|OPS|AB|HR|RBI|K' if not awayLineupOnly else ''}|\
|${data[gamePk]['schedule']['teams']['home']['team']['teamName']} Lineup${' vs. ' + playerLink(data[gamePk]['gumbo']["gameData"]["players"]['ID'+str(data[gamePk]['schedule']['teams']['away']['probablePitcher']['id'])]['boxscoreName'],data[gamePk]['schedule']['teams']['away']['probablePitcher']['id']) + '|AVG|OPS|AB|HR|RBI|K' if not homeLineupOnly else ''}|
|${':--|'*(15 if not awayLineupOnly else 3)}
% for i in range(0,len(awayBatters)):
<%
    a = next((x for x in data[gamePk]['awayBattersVsProb'] if x['id']==awayBatters[i]),{})
    aStats = next((s['splits'][0]['stat'] for s in a.get('stats',{}) if s['type']['displayName']=='vsPlayerTotal' and s['group']['displayName']=='hitting'),{})
    h = next((x for x in data[gamePk]['homeBattersVsProb'] if x['id']==homeBatters[i]),{})
    hStats = next((s['splits'][0]['stat'] for s in h.get('stats',{}) if s['type']['displayName']=='vsPlayerTotal' and s['group']['displayName']=='hitting'),{})
%>\
% if awayBatters[i] != 0:
|${i+1} ${playerLink(data[gamePk]['gumbo']["gameData"]["players"]['ID'+str(awayBatters[i])]['boxscoreName'],awayBatters[i]) + ' - ' + data[gamePk]['gumbo']['liveData']['boxscore']['teams']['away']['players']['ID'+str(awayBatters[i])]['position']['abbreviation']}|\
${str(aStats.get('avg','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('ops','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('atBats','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('homeRuns','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('rbi','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('strikeOuts','-'))+'|' if not awayLineupOnly else ''}\
% else:
${'||||||||' if not awayLineupOnly else '||'}\
% endif
% if homeBatters[i] != 0:
|${i+1} ${playerLink(data[gamePk]['gumbo']["gameData"]["players"]['ID'+str(homeBatters[i])]['boxscoreName'],homeBatters[i]) + ' - ' + data[gamePk]['gumbo']['liveData']['boxscore']['teams']['home']['players']['ID'+str(homeBatters[i])]['position']['abbreviation']}|\
${str(hStats.get('avg','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('ops','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('atBats','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('homeRuns','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('rbi','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('strikeOuts','-'))+'|' if not homeLineupOnly else ''}
% else:
${'||||||||' if not homeLineupOnly else '||'}
% endif
% endfor
% endif
% elif boxStyle.lower() == 'stacked':
## Stacked Batting Boxes
## Away
% if len(awayBatters):
|${data[gamePk]['schedule']['teams']['away']['team']['teamName']} Lineup${' vs. ' + playerLink(data[gamePk]['gumbo']["gameData"]["players"]['ID'+str(data[gamePk]['schedule']['teams']['home']['probablePitcher']['id'])]['boxscoreName'],data[gamePk]['schedule']['teams']['home']['probablePitcher']['id']) + '|AVG|OPS|AB|HR|RBI|K|' if not awayLineupOnly else '|'}
|${':--|'*(7 if not awayLineupOnly else 2)}
% for i in range(0,len(awayBatters)):
<%
    a = next((x for x in data[gamePk]['awayBattersVsProb'] if x['id']==awayBatters[i]),{})
    aStats = next((s['splits'][0]['stat'] for s in a.get('stats',{}) if s['type']['displayName']=='vsPlayerTotal' and s['group']['displayName']=='hitting'),{})
%>\
% if awayBatters[i] != 0:
|${i+1} ${playerLink(data[gamePk]['gumbo']["gameData"]["players"]['ID'+str(awayBatters[i])]['boxscoreName'],awayBatters[i]) + ' - ' + data[gamePk]['gumbo']['liveData']['boxscore']['teams']['away']['players']['ID'+str(awayBatters[i])]['position']['abbreviation']}|\
${str(aStats.get('avg','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('ops','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('atBats','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('homeRuns','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('rbi','-'))+'|' if not awayLineupOnly else ''}\
${str(aStats.get('strikeOuts','-')) if not awayLineupOnly else ''}|
% else:
|${'|'*(7 if not awayLineupOnly else 2)}
% endif
% endfor
% endif

## Home
% if len(homeBatters):
|${data[gamePk]['schedule']['teams']['home']['team']['teamName']} Lineup${' vs. ' + playerLink(data[gamePk]['gumbo']["gameData"]["players"]['ID'+str(data[gamePk]['schedule']['teams']['away']['probablePitcher']['id'])]['boxscoreName'],data[gamePk]['schedule']['teams']['away']['probablePitcher']['id']) + '|AVG|OPS|AB|HR|RBI|K|' if not homeLineupOnly else '|'}
|${':--|'*(7 if not homeLineupOnly else 2)}
% for i in range(0,len(homeBatters)):
<%
    h = next((x for x in data[gamePk]['homeBattersVsProb'] if x['id']==homeBatters[i]),{})
    hStats = next((s['splits'][0]['stat'] for s in h.get('stats',{}) if s['type']['displayName']=='vsPlayerTotal' and s['group']['displayName']=='hitting'),{})
%>\
% if homeBatters[i] != 0:
|${i+1} ${playerLink(data[gamePk]['gumbo']["gameData"]["players"]['ID'+str(homeBatters[i])]['boxscoreName'],homeBatters[i]) + ' - ' + data[gamePk]['gumbo']['liveData']['boxscore']['teams']['home']['players']['ID'+str(homeBatters[i])]['position']['abbreviation']}|\
${str(hStats.get('avg','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('ops','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('atBats','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('homeRuns','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('rbi','-'))+'|' if not homeLineupOnly else ''}\
${str(hStats.get('strikeOuts','-')) if not homeLineupOnly else ''}|
% else:
|${'|'*(7 if not homeLineupOnly else 2)}
% endif
% endfor
% endif
% endif
