<%page args="gamePk" />
${'###'}Links & Info
* [MLB Gameday](https://www.mlb.com/gameday/${gamePk}/)
##* Game Notes: [${data[gamePk]['schedule']['teams']['away']['team']['teamName']}](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=${data[gamePk]['schedule']['teams']['away']['team']['fileCode']}), [${data[gamePk]['schedule']['teams']['home']['team']['teamName']}](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=${data[gamePk]['schedule']['teams']['home']['team']['fileCode']})
##* ${'[Strikezone Map](http://www.brooksbaseball.net/pfxVB/zoneTrack.php?month={}&day={}&year={}&game=gid_{})'.format(data[gamePk]['gameTime']['homeTeam'].strftime('%m'), data[gamePk]['gameTime']['homeTeam'].strftime('%d'), data[gamePk]['gameTime']['homeTeam'].strftime('%Y'), data[gamePk]['gumbo']['gameData']['game']['id'].replace('/','_').replace('-','_'))}
* ${'[Game Graphs](http://www.fangraphs.com/livewins.aspx?date={}&team={}&dh={}&season={})'.format( data[gamePk]['gameTime']['homeTeam'].strftime("%Y-%m-%d"), data[gamePk]['schedule']['teams']['home']['team']['teamName'].replace(' ','%20'), data[gamePk]['schedule']['gameNumber'] if data[gamePk]['schedule']['doubleHeader']!='N' else 0, data[gamePk]['gameTime']['homeTeam'].strftime('%Y'))}
* ${f"[Savant Gamefeed](https://baseballsavant.mlb.com/gamefeed?gamePk={gamePk})"}
% for n in range(1, 6):
%   if settings.get('Post Game Thread',{}).get(f'LINK_{n}',''):
* [${settings['Post Game Thread'][f'LINK_{n}'].split("|")[0]}](${settings['Post Game Thread'][f'LINK_{n}'].split("|")[1].replace('gamePk', str(gamePk))})
%   endif
% endfor