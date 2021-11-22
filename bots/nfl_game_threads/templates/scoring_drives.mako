<%
    game = data["todayGames"][data["myGameIndex"]]
    gameDetails = data["gameDetails"]
    awayTeam = data["myTeam"] if data["homeAway"] == "away" else data["oppTeam"]
    homeTeam = data["myTeam"] if data["homeAway"] == "home" else data["oppTeam"]
%>\
%if len(gameDetails.get("scoringSummaries", [])) > 0 and not (len(gameDetails["scoringSummaries"]) == 1 and gameDetails["scoringSummaries"][0]["playId"] == 0):
${'##'} Scoring Summary
|Qtr|Team|Type|Description|Score|
|:--|:--|:--|:--|:--|
%   for x in gameDetails["scoringSummaries"]:
<%
        play = next((p for p in gameDetails["plays"] if p["playId"] == x["playId"] and p["scoringPlay"]), None)
%>\
%       if play:
|${play["quarter"]}|${play["scoringTeam"]["abbreviation"]}|${play["scoringPlayType"]}|${x["playDescription"]}|${max(x["visitorScore"], x["homeScore"])}-${min(x["visitorScore"], x["homeScore"])} \
%           if x["visitorScore"] > x["homeScore"]:
${awayTeam["abbreviation"]}|
%           elif x["homeScore"] > x["visitorScore"]:
${homeTeam["abbreviation"]}|
%           else:
|
%           endif
%       endif
%   endfor
%endif