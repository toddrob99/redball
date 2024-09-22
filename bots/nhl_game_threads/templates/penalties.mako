## Penalties
<%
    if not data["game"].get("summary", {}).get("penalties", []):
        return

    something_to_do = False
    for x in data["game"].get("summary", {}).get("penalties", []):
        if len(x.get("penalties", [])):
            something_to_do = True

    if not something_to_do:
        return

    ordDict = {1:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},2:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},3:{1:'1st',2:'2nd',3:'3rd',4:'OT1',5:'OT2',6:'OT3',7:'OT4',8:'OT5'}}
    periodOrd = ordDict[data["game"]["gameType"]]
    sevs = {"MIN": "Minor", "MAJ": "Major", "BEN": "Bench", "GAM": "Game Misconduct"}
%>
${'##'} Penalty Summary
|Per./Time|Team|Type|Description|
|:--|:--|:--|:--|
% for per in data["game"]["summary"]["penalties"]:
%   for p in per.get("penalties", []):
<%
    desc = (p.get("descKey", "").title() + " - ") if p.get("descKey") else ""
    if p.get("committedByPlayer"):
        desc += f"Committed by {p['committedByPlayer']}. "
    if p.get("drawnBy"):
        desc += f"Drawn by {p['drawnBy']}. "
    if p.get("servedBy"):
        desc += f"Served by {p['servedBy']}."
%>\
|${periodOrd[per.get("period", per.get("periodDescriptor", {}).get("number"))]}\
${(' ' + p.get('timeInPeriod')) if per.get('periodDescriptor', {}).get('periodType') != 'SO' else ''}|\
[${p['teamAbbrev']["default"]}](${data['teamSubs'].get(p['teamAbbrev']["default"], '')})|\
${p['duration']}:00 ${sevs.get(p['type'], "")}|\
${desc}|
%   endfor
% endfor
