## Scoring plays
<%
	sortedPlays = []
	if not data[gamePk]['schedule'].get('scoringPlays'):
		return
	else:
		unorderedPlays = {}
		for s in data[gamePk]['schedule']['scoringPlays']:
			if s['result'].get('description'):
				unorderedPlays.update({s['about']['endTime'] : s})

		for x in sorted(unorderedPlays):
			sortedPlays.append(unorderedPlays[x])
%>
% if len(sortedPlays) > 0:
|Inning|Scoring Play|Score|
|:--|:--|:--|
	% for p in sortedPlays:
|${p['about']['halfInning'][0:1].upper() + p['about']['halfInning'][1:]} ${str(p['about']['inning'])}|${p['result']['description']}|${str(max(p['result']['awayScore'],p['result']['homeScore']))+'-'+str(min(p['result']['awayScore'],p['result']['homeScore']))}${(' ' + data[gamePk]['schedule']['teams']['away']['team']['abbreviation'] if p['result']['awayScore'] > p['result']['homeScore'] else ' ' + data[gamePk]['schedule']['teams']['home']['team']['abbreviation']) if p['result']['awayScore']!=p['result']['homeScore'] else ''}|
	% endfor
% endif
