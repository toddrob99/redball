## Scoring plays
<%
	sortedPlays = []
	if not len(data[gamePk]['gumbo']["liveData"]["plays"].get('scoringPlays', [])):
		return
	else:
		unorderedPlays = {}
		for i in data[gamePk]['gumbo']["liveData"]["plays"]["scoringPlays"]:
			play = next(
				(p for p in data[gamePk]['gumbo']["liveData"]["plays"]["allPlays"] if p.get("atBatIndex") == i),
				None,
			)
			if play and play['result'].get('description'):
				unorderedPlays.update({play["about"]["endTime"]: play})

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
