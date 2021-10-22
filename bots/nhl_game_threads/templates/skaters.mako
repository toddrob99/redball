## Skaters
<%
    if not len(data["game"]["liveData"]["boxscore"]["teams"]["away"]["skaters"]) or not len(data["game"]["liveData"]["boxscore"]["teams"]["home"]["skaters"]):
        return
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    awaySkaterIds = data["game"]["liveData"]["boxscore"]["teams"]["away"]["skaters"]
    homeSkaterIds = data["game"]["liveData"]["boxscore"]["teams"]["home"]["skaters"]
    awayGoalieIds = data["game"]["liveData"]["boxscore"]["teams"]["away"]["goalies"]
    homeGoalieIds = data["game"]["liveData"]["boxscore"]["teams"]["home"]["goalies"]
    awayPlayers = data["game"]["liveData"]["boxscore"]["teams"]["away"]["players"]
    homePlayers = data["game"]["liveData"]["boxscore"]["teams"]["home"]["players"]
    awaySkaters = [{"id": s["person"]["id"], "name":s["person"]["fullName"], "position_abbreviation": s["position"]["abbreviation"], "position_name": s["position"]["name"], "position_type": s["position"]["type"]} for k, s in awayPlayers.items() if int(k[2:]) in awaySkaterIds]
    homeSkaters = [{"id": s["person"]["id"], "name":s["person"]["fullName"], "position_abbreviation": s["position"]["abbreviation"], "position_name": s["position"]["name"], "position_type": s["position"]["type"]} for k, s in homePlayers.items() if int(k[2:]) in homeSkaterIds]
    awayGoalies = [{"id": s["person"]["id"], "name":s["person"]["fullName"], "position_abbreviation": s["position"]["abbreviation"], "position_name": s["position"]["name"], "position_type": s["position"]["type"]} for k, s in awayPlayers.items() if int(k[2:]) in awayGoalieIds]
    homeGoalies = [{"id": s["person"]["id"], "name":s["person"]["fullName"], "position_abbreviation": s["position"]["abbreviation"], "position_name": s["position"]["name"], "position_type": s["position"]["type"]} for k, s in homePlayers.items() if int(k[2:]) in homeGoalieIds]
    awayF = [x for x in awaySkaters if x["position_type"] == "Forward"]
    awayD = [x for x in awaySkaters if x["position_type"] == "Defenseman"]
    homeF = [x for x in homeSkaters if x["position_type"] == "Forward"]
    homeD = [x for x in homeSkaters if x["position_type"] == "Defenseman"]
    awayOnIce = data["game"]["liveData"]["boxscore"]["teams"]["away"]["onIce"]
    homeOnIce = data["game"]["liveData"]["boxscore"]["teams"]["home"]["onIce"]
    def playerLink(p):
        return f"[{p['name']}](https://www.nhl.com/player/{p['id']})"
%>
% if len(awaySkaters):
${'##'} ${awayTeam["teamName"]} Players
|Forwards|Forwards|Defensemen|Goalies|
|:--|:--|:--|:--|
%   for i in range(0, min(6, max(len(awayF), len(awayD), len(awayGoalies)))):
|${"**" if len(awayF)>i and awayF[i]["id"] in awayOnIce else ""}${playerLink(awayF[i]) if len(awayF)>i else ""}${"**" if len(awayF)>i and awayF[i]["id"] in awayOnIce else ""}|\
${"**" if len(awayF)>i+6 and awayF[i+6]["id"] in awayOnIce else ""}${playerLink(awayF[i+6]) if len(awayF)>i+6 else ""}${"**" if len(awayF)>i+6 and awayF[i+6]["id"] in awayOnIce else ""}|\
${"**" if len(awayD)>i and awayD[i]["id"] in awayOnIce else ""}${playerLink(awayD[i]) if len(awayD)>i else ""}${"**" if len(awayD)>i and awayD[i]["id"] in awayOnIce else ""}|\
${"**" if len(awayGoalies)>i and awayGoalies[i]["id"] in awayOnIce else ""}${playerLink(awayGoalies[i]) if len(awayGoalies)>i else ""}${"**" if len(awayGoalies)>i and awayGoalies[i]["id"] in awayOnIce else ""}|
%   endfor
% endif

% if len(homeSkaters):
${'##'} ${homeTeam["teamName"]} Players
|Forwards|Forwards|Defensemen|Goalies|
|:--|:--|:--|:--|
%   for i in range(0, min(6, max(len(homeF), len(homeD), len(homeGoalies)))):
|${"**" if len(homeF)>i and homeF[i]["id"] in homeOnIce else ""}${playerLink(homeF[i]) if len(homeF)>i else ""}${"**" if len(homeF)>i and homeF[i]["id"] in homeOnIce else ""}|\
${"**" if len(homeF)>i+6 and homeF[i+6]["id"] in homeOnIce else ""}${playerLink(homeF[i+6]) if len(homeF)>i+6 else ""}${"**" if len(homeF)>i+6 and homeF[i+6]["id"] in homeOnIce else ""}|\
${"**" if len(homeD)>i and homeD[i]["id"] in homeOnIce else ""}${playerLink(homeD[i]) if len(homeD)>i else ""}${"**" if len(homeD)>i and homeD[i]["id"] in homeOnIce else ""}|\
${"**" if len(homeGoalies)>i and homeGoalies[i]["id"] in homeOnIce else ""}${playerLink(homeGoalies[i]) if len(homeGoalies)>i else ""}${"**" if len(homeGoalies)>i and homeGoalies[i]["id"] in homeOnIce else ""}|
%   endfor
% endif
