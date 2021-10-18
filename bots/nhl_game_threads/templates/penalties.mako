## Penalties
<%
    if not len(data["game"]["liveData"]["plays"].get('penaltyPlays', [])):
        pass#return
    else:
        plays = []
        for i in data["game"]["liveData"]["plays"]["penaltyPlays"]:
            play = next(
                (p for p in data["game"]["liveData"]["plays"]["allPlays"] if p["about"].get("eventIdx") == i),
                None,
            )
            if play and play['result'].get('description'):
                plays.append(play)
%>
% if len(plays):
${'##'} Penalty Summary
%   for p in plays:
* ${f" {p['about']['ordinalNum']}{(' ' + p['about']['periodTime']) if p['about']['periodType'] != 'SHOOTOUT' else ''}"} - \
${p['team']['triCode']} - \
${p['result']['penaltyMinutes']} Min ${p['result']['penaltySeverity']} - \
${p['result']['description']}
%   endfor

% endif