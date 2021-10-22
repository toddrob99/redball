## Scoring plays
<%
    if not len(data["game"]["liveData"]["plays"].get('scoringPlays', [])):
        return
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
|Per./Time|Team|Description & Video Link|Score|
|:--|:--|:--|:--|
%   for p in plays:
<%
    milestone = next((x for x in data["content"].get("media", {}).get("milestones", {}).get("items", []) if x["type"]=="GOAL" and x["highlight"]["type"]=="video" and str(x["period"])==str(p["about"]["period"]) and x["periodTime"]==p["about"]["periodTime"]), None)
    hdLink = next((v.get('url') for v in milestone.get('highlight', {}).get('playbacks',[]) if v.get('name')=='FLASH_1800K_896x504'),'')
    #hdLink = ""
%>\
|${f"{p['about']['ordinalNum']}{(' ' + p['about']['periodTime']) if p['about']['periodType'] != 'SHOOTOUT' else ''}"}|\
[${p['team']['triCode']}](${data['teamSubsById'].get(p['team']['id'], '')})|\
${f"{p['result']['strength']['code']} - " if p['result']['strength']['code'] != 'EVEN' else ''}\
${f"Empty Net - " if p['result']['emptyNet'] else ''}\
[${p['result']['description']}](${hdLink})|\
%       if p['about']['periodType'] != "SHOOTOUT":
${str(max(p['about']['goals']['away'],p['about']['goals']['home']))+'-'+str(min(p['about']['goals']['away'],p['about']['goals']['home']))}${(' ' + data['game']['gameData']['teams']['away']['abbreviation'] if p['about']['goals']['away'] > p['about']['goals']['home'] else ' ' + data['game']['gameData']['teams']['home']['abbreviation']) if p['about']['goals']['away']!=p['about']['goals']['home'] else ''}\
%       else:
SHOOTOUT\
%       endif
|
%   endfor

% endif