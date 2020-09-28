<%
    game = data["todayGames"][data["myGameIndex"]]
    if not data["gameDetails"]:
        return
    drives = data["gameDetails"]["drives"]
    if not len(drives):
        return
%>\
${"##"} Drive Summary
|Team|Time/Poss|Plays/Yards|Result|
|:--|:--|:--|:--|
% for d in drives:
|${d["possessionTeam"]["abbreviation"]}|${d["timeOfPossession"]}|${d["playCount"]}/${d["yards"]}|${d["howEndedDescription"]}|
% endfor