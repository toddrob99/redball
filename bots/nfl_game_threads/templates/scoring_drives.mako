<%
    game = data["todayGames"][data["myGameIndex"]]
%>\
%if len(data["gameDetails"].get("scoringSummaries", [])) > 0:
${'##'} Scoring Summary
%for x in data["gameDetails"]["scoringSummaries"]:
<%
play = next((p for p in data["gameDetails"]["plays"] if p["playId"] == x["playId"] and p["scoringPlay"]), None)
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