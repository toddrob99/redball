<%page args="gamePk" />
<%
    def playerLink(name, personId):
        return '[{}](https://www.mlb.com/player/{})'.format(name,str(personId))

    if data[gamePk]["gumbo"]["liveData"].get("decisions"):
        decisions = data[gamePk]["gumbo"]["liveData"]["decisions"]
        decisions_prepared = []
        for k, v in decisions.items():
            seasonStats = data[gamePk]["gumbo"]["liveData"]["boxscore"]["teams"]["away"]["players"].get(f"ID{v['id']}", data[gamePk]["gumbo"]["liveData"]["boxscore"]["teams"]["home"]["players"].get(f"ID{v['id']}", {})).get("seasonStats", {}).get("pitching", {})
            detail = (
                f"({seasonStats.get('holds', '-')}, {seasonStats.get('era', '-.--')})" if k == "hold"
                else f"({seasonStats.get('saves', '-')}, {seasonStats.get('era', '-.--')})" if k == "save"
                else f"({seasonStats.get('wins', '-')}-{seasonStats.get('losses', '-')}, {seasonStats.get('era', '-.--')})"
            )
            decisions_prepared.append(f"{k.title()}: {playerLink(v.get('fullName', 'Unknown'), v.get('id', 0))} {detail}")
    else:
        return
    if not len(decisions_prepared):
        return
%>
${'###'}Decisions
% for d in decisions_prepared:
* ${d}
% endfor