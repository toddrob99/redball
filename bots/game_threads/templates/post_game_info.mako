<%page args="gamePk" />
${'###'}Links & Info
## Venue & weather
% if data[gamePk]['schedule'].get('weather') and len(data[gamePk]['schedule']['weather']):
* Weather conditions at ${data[gamePk]['schedule']['venue']['name']}: ${data[gamePk]['schedule']['weather']['temp']+'&#176;F' if data[gamePk]['schedule']['weather'].get('temp') else ''} ${'- ' + data[gamePk]['schedule']['weather']['condition'] if data[gamePk]['schedule']['weather'].get('condition') else ''} ${'- Wind ' + data[gamePk]['schedule']['weather']['wind'] if data[gamePk]['schedule']['weather'].get('wind') else ''}
% endif
* [MLB Gameday](https://www.mlb.com/gameday/${gamePk}/)
##* Game Notes: [${data[gamePk]['schedule']['teams']['away']['team']['teamName']}](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=${data[gamePk]['schedule']['teams']['away']['team']['fileCode']}), [${data[gamePk]['schedule']['teams']['home']['team']['teamName']}](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=${data[gamePk]['schedule']['teams']['home']['team']['fileCode']})
##* ${'[Strikezone Map](http://www.brooksbaseball.net/pfxVB/zoneTrack.php?month={}&day={}&year={}&game=gid_{})'.format(data[gamePk]['gameTime']['homeTeam'].strftime('%m'), data[gamePk]['gameTime']['homeTeam'].strftime('%d'), data[gamePk]['gameTime']['homeTeam'].strftime('%Y'), data[gamePk]['gumbo']['gameData']['game']['id'].replace('/','_').replace('-','_'))}
* ${'[Game Graphs](http://www.fangraphs.com/livewins.aspx?date={}&team={}&dh={}&season={})'.format( data[gamePk]['gameTime']['homeTeam'].strftime("%Y-%m-%d"), data[gamePk]['schedule']['teams']['home']['team']['teamName'].replace(' ','%20'), data[gamePk]['schedule']['gameNumber'] if data[gamePk]['schedule']['doubleHeader']!='N' else 0, data[gamePk]['gameTime']['homeTeam'].strftime('%Y'))}