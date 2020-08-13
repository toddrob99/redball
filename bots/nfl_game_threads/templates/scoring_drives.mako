<%
    game = data["todayGames"][data["myGameIndex"]]
%>\
%if len(data["gameDetails"]["scoringSummaries"]) > 0:
${'##'} Scoring Drives
%for x in data["gameDetails"]["scoringSummaries"]:
<%
play = next((p for p in data["gameDetails"]["plays"] if p["playId"] == x["playId"]), None)
%>\
%if play:
* Q${play["quarter"]} ${play["scoringTeam"]["abbreviation"]} ${play["shortDescription"]} - Score: ${max(x["visitorScore"], x["homeScore"])}-${min(x["visitorScore"], x["homeScore"])} \
%if x["visitorScore"] > x["homeScore"]:
${game["visitorTeam"]["abbr"]}
%elif x["homeScore"] > x["visitorScore"]:
${game["homeTeam"]["abbr"]}
%else:
## don't list a team abbr if game is tied

%endif
%endif
%endfor
%endif