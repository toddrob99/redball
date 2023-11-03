## Scratches
<%
    awayScratches = data["game"].get("matchup", {}).get("gameInfo", {}).get("awayTeam", {}).get("scratches", None)
    if not awayScratches:
        awayScratches = data["game"].get("summary", {}).get("gameInfo", {}).get("awayTeam", {}).get("scratches", None)
    if awayScratches is None:
        awayScratches = []
    homeScratches = data["game"].get("matchup", {}).get("gameInfo", {}).get("homeTeam", {}).get("scratches", None)
    if not homeScratches:
        homeScratches = data["game"].get("summary", {}).get("gameInfo", {}).get("homeTeam", {}).get("scratches", None)
    if homeScratches is None:
        homeScratches = []
    
    if not len(awayScratches) and not len(homeScratches):
        return
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    #awayPlayers = data["game_boxscore"][""]["boxscore"]["teams"]["away"]["players"]
    #homePlayers = data["game"]["liveData"]["boxscore"]["teams"]["home"]["players"]
    #awayScratches = [{"id": s["person"]["id"], "name":s["person"]["fullName"], "position_abbreviation": s["position"]["abbreviation"], "position_name": s["position"]["name"], "position_type": s["position"]["type"]} for k, s in awayPlayers.items() if int(k[2:]) in awayScratchIds]
    #homeScratches = [{"id": s["person"]["id"], "name":s["person"]["fullName"], "position_abbreviation": s["position"]["abbreviation"], "position_name": s["position"]["name"], "position_type": s["position"]["type"]} for k, s in homePlayers.items() if int(k[2:]) in homeScratchIds]
    def playerLink(p):
        return f"[{p['firstName']['default']} {p['lastName']['default']}](https://www.nhl.com/player/{p['id']})"
%>
% if len(awayScratches) or len(homeScratches):
${'##'} Scratches
|${awayTeam["commonName"]["default"]}|${homeTeam["commonName"]["default"]}|
|:--|:--|
%   for i in range(0, max(len(awayScratches), len(homeScratches))):
|${playerLink(awayScratches[i]) if len(awayScratches)>i else ""}|\
${playerLink(homeScratches[i]) if len(homeScratches)>i else ""}|
%   endfor
% endif
