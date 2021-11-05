<%
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    awayStats = data["game"]["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]
    homeStats = data["game"]["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]

    awaySkaterIds = data["game"]["liveData"]["boxscore"]["teams"]["away"]["skaters"]
    homeSkaterIds = data["game"]["liveData"]["boxscore"]["teams"]["home"]["skaters"]
    awayGoalieIds = data["game"]["liveData"]["boxscore"]["teams"]["away"]["goalies"]
    homeGoalieIds = data["game"]["liveData"]["boxscore"]["teams"]["home"]["goalies"]
    awayPlayers = data["game"]["liveData"]["boxscore"]["teams"]["away"]["players"]
    homePlayers = data["game"]["liveData"]["boxscore"]["teams"]["home"]["players"]
    awaySkaters = sorted([s for k, s in awayPlayers.items() if int(k[2:]) in awaySkaterIds and s.get("stats", {}).get("skaterStats")], key=lambda p: p["position"]["abbreviation"])
    homeSkaters = sorted([s for k, s in homePlayers.items() if int(k[2:]) in homeSkaterIds and s.get("stats", {}).get("skaterStats")], key=lambda p: p["position"]["abbreviation"])
    awayGoalies = sorted([s for k, s in awayPlayers.items() if int(k[2:]) in awayGoalieIds and s.get("stats", {}).get("goalieStats")], key=lambda g: g["stats"]["goalieStats"]["timeOnIce"], reverse=1)
    homeGoalies = sorted([s for k, s in homePlayers.items() if int(k[2:]) in homeGoalieIds and s.get("stats", {}).get("goalieStats")], key=lambda g: g["stats"]["goalieStats"]["timeOnIce"], reverse=1)
    awayOnIce = data["game"]["liveData"]["boxscore"]["teams"]["away"]["onIce"]
    homeOnIce = data["game"]["liveData"]["boxscore"]["teams"]["home"]["onIce"]
    def playerLink(p):
        return f"[{p['person']['fullName']}](https://www.nhl.com/player/{p['person']['id']})"
%>\
${'##'} Game Stats
||SOG|FO%|PP|PIM|Hits|Blks|GVA|
|:--|:--|:--|:--|:--|:--|:--|:--|
## Team
|[${awayTeam["teamName"]}](${data["teamSubs"][awayTeam["abbreviation"]]})|${awayStats["shots"]}|${round(float(awayStats["faceOffWinPercentage"]))}%|\
${int(awayStats["powerPlayGoals"])}/${int(awayStats["powerPlayOpportunities"])} (${int(float(awayStats["powerPlayPercentage"]))}%)|\
${awayStats["pim"]}|${awayStats["hits"]}|${awayStats["blocked"]}|${awayStats["giveaways"]}|
|[${homeTeam["teamName"]}](${data["teamSubs"][homeTeam["abbreviation"]]})|${homeStats["shots"]}|${round(float(homeStats["faceOffWinPercentage"]))}%|\
${int(homeStats["powerPlayGoals"])}/${int(homeStats["powerPlayOpportunities"])} (${int(float(homeStats["powerPlayPercentage"]))}%)|\
${homeStats["pim"]}|${homeStats["hits"]}|${homeStats["blocked"]}|${homeStats["giveaways"]}|
<%
    if not len(data["game"]["liveData"]["boxscore"]["teams"]["away"]["skaters"]) and not len(data["game"]["liveData"]["boxscore"]["teams"]["home"]["skaters"]):
        return
%>
% for info in [(awayTeam, awaySkaters, awayOnIce, awayGoalies), (homeTeam, homeSkaters, homeOnIce, homeGoalies)]:
%   if len(info[1]):
|[${info[0]["teamName"]}](${data["teamSubs"][info[0]["abbreviation"]]}) Skaters|G|A|+/-|S|Blk|Tkwy|Gvwy|PIM|TOI|
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
%       for p in info[1]:
|^${p['position']['abbreviation']} ${'**' if p["person"]["id"] in info[2] else ''}${playerLink(p)}${'**' if p["person"]["id"] in info[2] else ''}|\
${p["stats"]["skaterStats"]["goals"]}|\
${p["stats"]["skaterStats"]["assists"]}|\
${p["stats"]["skaterStats"]["plusMinus"]}|\
${p["stats"]["skaterStats"]["shots"]}|\
${p["stats"]["skaterStats"]["blocked"]}|\
${p["stats"]["skaterStats"]["takeaways"]}|\
${p["stats"]["skaterStats"]["giveaways"]}|\
${p["stats"]["skaterStats"]["penaltyMinutes"]}|\
${p["stats"]["skaterStats"]["timeOnIce"]}|
%       endfor
%   endif

%   if len(info[3]):
|[${info[0]["teamName"]}](${data["teamSubs"][info[0]["abbreviation"]]}) Goalies|Saves|Shots|Save %|TOI|
|:--|:-:|:-:|:-:|:-:|
%       for g in info[3]:
|${'**' if g["person"]["id"] in info[2] else ''}${playerLink(g)}${'**' if g["person"]["id"] in info[2] else ''}|\
${g["stats"]["goalieStats"]["saves"]}|\
${g["stats"]["goalieStats"]["shots"]}|\
${f'{g["stats"]["goalieStats"]["savePercentage"]:.1f}%' if g["stats"]["goalieStats"].get("savePercentage") else "-"}|\
${g["stats"]["goalieStats"]["timeOnIce"]}|
%       endfor
%   endif

% endfor
