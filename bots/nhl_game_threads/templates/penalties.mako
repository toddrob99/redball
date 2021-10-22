## Penalties
<%
    if not len(data["game"]["liveData"]["plays"].get('penaltyPlays', [])):
        return
    else:
        plays = []
        for i in data["game"]["liveData"]["plays"]["penaltyPlays"]:
            play = next(
                (p for p in data["game"]["liveData"]["plays"]["allPlays"] if p["about"].get("eventIdx") == i and p["result"]["eventTypeId"]=="PENALTY"),
                None,
            )
            if play and play['result'].get('description'):
                plays.append(play)
%>
% if len(plays):
${'##'} Penalty Summary
|Per./Time|Team|Type|Description|
|:--|:--|:--|:--|
%   for p in plays:
|${f" {p['about']['ordinalNum']}{(' ' + p['about']['periodTime']) if p['about']['periodType'] != 'SHOOTOUT' else ''}"}|\
[${p['team']['triCode']}](${data['teamSubsById'].get(p['team']['id'], '')})|\
${p['result']['penaltyMinutes']}:00 ${p['result']['penaltySeverity']}|\
${p['result']['description']}|
%   endfor

% endif