## Skaters
<%
    if not len(data["game"]["liveData"]["boxscore"]["teams"]["away"]["scratches"]) and not len(data["game"]["liveData"]["boxscore"]["teams"]["home"]["scratches"]):
        return
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    awayScratchIds = data["game"]["liveData"]["boxscore"]["teams"]["away"]["scratches"]
    homeScratchIds = data["game"]["liveData"]["boxscore"]["teams"]["home"]["scratches"]
    awayPlayers = data["game"]["liveData"]["boxscore"]["teams"]["away"]["players"]
    homePlayers = data["game"]["liveData"]["boxscore"]["teams"]["home"]["players"]
    awayScratches = [{"id": s["person"]["id"], "name":s["person"]["fullName"], "position_abbreviation": s["position"]["abbreviation"], "position_name": s["position"]["name"], "position_type": s["position"]["type"]} for k, s in awayPlayers.items() if int(k[2:]) in awayScratchIds]
    homeScratches = [{"id": s["person"]["id"], "name":s["person"]["fullName"], "position_abbreviation": s["position"]["abbreviation"], "position_name": s["position"]["name"], "position_type": s["position"]["type"]} for k, s in homePlayers.items() if int(k[2:]) in homeScratchIds]
    def playerLink(p):
        return f"[{p['name']}](https://www.nhl.com/player/{p['id']})"
%>
% if len(awayScratches) or len(homeScratches):
${'##'} Scratches
|${awayTeam["teamName"]}|${homeTeam["teamName"]}|
|:--|:--|
%   for i in range(0, max(len(awayScratches), len(homeScratches))):
|${playerLink(awayScratches[i]) if len(awayScratches)>i else ""}|\
${playerLink(homeScratches[i]) if len(homeScratches)>i else ""}|
%   endfor
% endif
