## Scoring plays
<%
    if not len(data["game"]["liveData"]["plays"].get('scoringPlays', [])):
        pass#return
    else:
        plays = []
        for i in data["game"]["liveData"]["plays"]["scoringPlays"]:
            play = next(
                (p for p in data["game"]["liveData"]["plays"]["allPlays"] if p["about"].get("eventIdx") == i and p["result"]["eventTypeId"]=="GOAL"),
                None,
            )
            if play and play['result'].get('description'):
                plays.append(play)
%>
% if len(plays):
${'##'} Scoring Summary
%   for p in plays:
* ${f" {p['about']['ordinalNum']}{(' ' + p['about']['periodTime']) if p['about']['periodType'] != 'SHOOTOUT' else ''}"} - \
${p['team']['triCode']}\
${f"({p['result']['strength']['code']})" if p['result']['strength']['code'] != 'EVEN' else ''} - \
${p['result']['description']} \
%       if p['about']['periodType'] != "SHOOTOUT":
- ${str(max(p['about']['goals']['away'],p['about']['goals']['home']))+'-'+str(min(p['about']['goals']['away'],p['about']['goals']['home']))}${(' ' + data['game']['gameData']['teams']['away']['abbreviation'] if p['about']['goals']['away'] > p['about']['goals']['home'] else ' ' + data['game']['gameData']['teams']['home']['abbreviation']) if p['about']['goals']['away']!=p['about']['goals']['home'] else ''}
%       endif
%   endfor

% endif