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
%>\
${'##'} Team Stats
||SOG|FO%|PP|PIM|Hits|Blks|GVA|
|:--|:--|:--|:--|:--|:--|:--|:--|
## Team
|[${awayTeam["teamName"]}](${data["teamSubs"][awayTeam["abbreviation"]]})|${awayStats["shots"]}|${round(float(awayStats["faceOffWinPercentage"]))}%|\
${int(awayStats["powerPlayGoals"])}/${int(awayStats["powerPlayOpportunities"])} (${int(float(awayStats["powerPlayPercentage"]))}%)|\
${awayStats["pim"]}|${awayStats["hits"]}|${awayStats["blocked"]}|${awayStats["giveaways"]}|
|[${homeTeam["teamName"]}](${data["teamSubs"][homeTeam["abbreviation"]]})|${homeStats["shots"]}|${round(float(homeStats["faceOffWinPercentage"]))}%|\
${int(homeStats["powerPlayGoals"])}/${int(homeStats["powerPlayOpportunities"])} (${int(float(homeStats["powerPlayPercentage"]))}%)|\
${homeStats["pim"]}|${homeStats["hits"]}|${homeStats["blocked"]}|${homeStats["giveaways"]}|