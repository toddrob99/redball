<%page args="gamePk" />
## Probable Pitchers
<%
    def playerLink(name, personId):
        return '[{}](http://mlb.mlb.com/team/player.jsp?player_id={})'.format(name,str(personId))

    awayPitcher = data[gamePk]['schedule']['teams']['away'].get('probablePitcher',{})
    awayPitcherData = data[gamePk]['gumbo']["liveData"]["boxscore"]["teams"]['away']['players'].get('ID'+str(awayPitcher.get('id','')),{'person':{'fullName':'TBD'}})
    homePitcher = data[gamePk]['schedule']['teams']['home'].get('probablePitcher',{})
    homePitcherData = data[gamePk]['gumbo']["liveData"]["boxscore"]["teams"]['home']['players'].get('ID'+str(homePitcher.get('id','')),{'person':{'fullName':'TBD'}})
%>\
||Probable Pitcher (Season Stats)|Report|
|:--|:--|:--|
|[${data[gamePk]['gumbo']["gameData"]["teams"]['away']['teamName']}](${data[0]['teamSubs'].get(data[gamePk]['gumbo']["gameData"]["teams"]['away']['id'], data[0]['teamSubs'][0])})|\
${playerLink(awayPitcherData['person']['fullName'],awayPitcherData['person']['id']) if awayPitcherData['person']['fullName'] != 'TBD' else 'TBD'}\
% if awayPitcherData['person']['fullName'] != 'TBD':
 (${awayPitcherData['seasonStats']['pitching'].get('wins',0)}-${awayPitcherData['seasonStats']['pitching'].get('losses',0)}, ${awayPitcherData['seasonStats']['pitching'].get('era','0')} ERA, ${awayPitcherData['seasonStats']['pitching'].get('inningsPitched',0)} IP)|\
% else:
|\
% endif
${awayPitcher.get('note','No report posted.')}|
\
|[${data[gamePk]['gumbo']["gameData"]["teams"]['home']['teamName']}](${data[0]['teamSubs'].get(data[gamePk]['gumbo']["gameData"]["teams"]['home']['id'], data[0]['teamSubs'][0])})|\
${playerLink(homePitcherData['person']['fullName'],homePitcherData['person']['id']) if homePitcherData['person']['fullName'] != 'TBD' else 'TBD'}\
% if homePitcherData['person']['fullName'] != 'TBD':
 (${homePitcherData['seasonStats']['pitching'].get('wins',0)}-${homePitcherData['seasonStats']['pitching'].get('losses',0)}, ${homePitcherData['seasonStats']['pitching'].get('era','-')} ERA, ${homePitcherData['seasonStats']['pitching'].get('inningsPitched',0)} IP)|\
% else:
|\
% endif
${homePitcher.get('note','No report posted.')}|