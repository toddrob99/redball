## Skaters
<%
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    awayF = data["game_boxscore"].get("playerByGameStats", {}).get("awayTeam", {}).get("forwards", [])
    awayL = [x for x in awayF if x["position"] == "L"]
    awayC = [x for x in awayF if x["position"] == "C"]
    awayR = [x for x in awayF if x["position"] == "R"]
    awayD = data["game_boxscore"].get("playerByGameStats", {}).get("awayTeam", {}).get("defense", [])
    awayG = data["game_boxscore"].get("playerByGameStats", {}).get("awayTeam", {}).get("goalies", [])
    awayOnIce = data["game_pbp"].get("awayTeam", {}).get("onIce", [])
    homeF = data["game_boxscore"].get("playerByGameStats", {}).get("homeTeam", {}).get("forwards", [])
    homeL = [x for x in homeF if x["position"] == "L"]
    homeC = [x for x in homeF if x["position"] == "C"]
    homeR = [x for x in homeF if x["position"] == "R"]
    homeD = data["game_boxscore"].get("playerByGameStats", {}).get("homeTeam", {}).get("defense", [])
    homeG = data["game_boxscore"].get("playerByGameStats", {}).get("homeTeam", {}).get("goalies", [])
    homeOnIce = data["game_pbp"].get("homeTeam", {}).get("onIce", [])
    def playerLink(p):
        return f"[{p['name']['default']}](https://www.nhl.com/player/{p['playerId']})"
%>
% if len(awayF) or len(awayD) or len(awayG):
${'##'} ${awayTeam["commonName"]["default"]} Players
|Left|Center|Right|Defensemen|Goalies|
|:--|:--|:--|:--|:--|
%   for i in range(0, min(12, max(len(awayL), len(awayC), len(awayR), len(awayD), len(awayG)))):
|${"**" if len(awayL)>i and awayL[i]["playerId"] in awayOnIce else ""}${playerLink(awayL[i]) if len(awayL)>i else ""}${"**" if len(awayL)>i and awayL[i]["playerId"] in awayOnIce else ""}|\
${"**" if len(awayC)>i and awayC[i]["playerId"] in awayOnIce else ""}${playerLink(awayC[i]) if len(awayC)>i else ""}${"**" if len(awayC)>i and awayC[i]["playerId"] in awayOnIce else ""}|\
${"**" if len(awayR)>i and awayR[i]["playerId"] in awayOnIce else ""}${playerLink(awayR[i]) if len(awayR)>i else ""}${"**" if len(awayR)>i and awayR[i]["playerId"] in awayOnIce else ""}|\
${"**" if len(awayD)>i and awayD[i]["playerId"] in awayOnIce else ""}${playerLink(awayD[i]) if len(awayD)>i else ""}${"**" if len(awayD)>i and awayD[i]["playerId"] in awayOnIce else ""}|\
${"**" if len(awayG)>i and awayG[i]["playerId"] in awayOnIce else ""}${playerLink(awayG[i]) if len(awayG)>i else ""}${"**" if len(awayG)>i and awayG[i]["playerId"] in awayOnIce else ""}|
%   endfor
% endif

% if len(homeF) or len(homeD) or len(homeG):
${'##'} ${homeTeam["commonName"]["default"]} Players
|Left|Center|Right|Defensemen|Goalies|
|:--|:--|:--|:--|:--|
%   for i in range(0, min(12, max(len(homeL), len(homeC), len(homeR), len(homeD), len(homeG)))):
|${"**" if len(homeL)>i and homeL[i]["playerId"] in homeOnIce else ""}${playerLink(homeL[i]) if len(homeL)>i else ""}${"**" if len(homeL)>i and homeL[i]["playerId"] in homeOnIce else ""}|\
${"**" if len(homeC)>i and homeC[i]["playerId"] in homeOnIce else ""}${playerLink(homeC[i]) if len(homeC)>i else ""}${"**" if len(homeC)>i and homeC[i]["playerId"] in homeOnIce else ""}|\
${"**" if len(homeR)>i and homeR[i]["playerId"] in homeOnIce else ""}${playerLink(homeR[i]) if len(homeR)>i else ""}${"**" if len(homeR)>i and homeR[i]["playerId"] in homeOnIce else ""}|\
${"**" if len(homeD)>i and homeD[i]["playerId"] in homeOnIce else ""}${playerLink(homeD[i]) if len(homeD)>i else ""}${"**" if len(homeD)>i and homeD[i]["playerId"] in homeOnIce else ""}|\
${"**" if len(homeG)>i and homeG[i]["playerId"] in homeOnIce else ""}${playerLink(homeG[i]) if len(homeG)>i else ""}${"**" if len(homeG)>i and homeG[i]["playerId"] in homeOnIce else ""}|
%   endfor
% endif
