## Scoring plays
<%
    if not data["game"].get("summary", {}).get("scoring", []):
        return

    something_to_do = False
    for x in data["game"].get("summary", {}).get("scoring", []):
        if len(x.get("goals", [])):
            something_to_do = True

    if not something_to_do:
        return

    def highlight_url(clip_id):
        return f"https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId={clip_id}"
    ordDict = {1:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},2:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},3:{1:'1st',2:'2nd',3:'3rd',4:'OT1',5:'OT2',6:'OT3',7:'OT4',8:'OT5'}}
    periodOrd = ordDict[data["game"]["gameType"]]
%>

${'##'} Scoring Summary
|Per./Time|Team|Description & Video Link|Score|
|:--|:--|:--|:--|
% for per in data["game"].get("summary", {}).get("scoring", []):
%   for p in per.get("goals", []):
<%
    assists = []
    for a in p.get("assists"):
        assists.append(f"{a['firstName']} {a['lastName']} ({a['assistsToDate']})")
    if not len(assists):
        assists_str = "unassisted"
    else:
        assists_str = f"assists: {', '.join(assists)}"
    desc = ""
    desc += f"{p['strength'].upper()} - " if p['strength'] != 'ev' else ''
    desc += f"Empty Net - " if p.get('goalModifier', '').upper == 'EN' else ''
    desc += f"{p['firstName']} {p['lastName']} ({p.get('goalsToDate', '-')}) {p.get('shotType', 'Unknown Shot Type')}, {assists_str}"
    if p.get("highlightClip"):
        desc = f"[{desc}]({highlight_url(p['highlightClip'])})"
%>\
|${periodOrd[per.get('period')]}\
${(' ' + p.get('timeInPeriod')) if per.get('periodDescriptor', {}).get('periodType') != 'SO' else ''}|\
[${p['teamAbbrev']}](${data['teamSubs'].get(p['teamAbbrev'], '')})|\
${desc}|\
%       if per.get('periodDescriptor', {}).get('periodType') != "SO":
${str(max(p['awayScore'],p['homeScore']))+'-'+str(min(p['awayScore'],p['homeScore']))} ${(data['game']['awayTeam']['abbrev'] if p['awayScore'] > p['homeScore'] else data['game']['homeTeam']['abbrev']) if p['awayScore'] != p['homeScore'] else ''}\
%       else:
SO\
%       endif
|
%   endfor
% endfor