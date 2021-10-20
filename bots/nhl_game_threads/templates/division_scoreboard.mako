<%
    from datetime import datetime
    import pytz
    divGames = [
        x
        for x in data["todayOtherGames"]
        if (
            x["teams"]["away"]["team"]["id"] in data["otherDivisionTeamIds"]
            or x["teams"]["home"]["team"]["id"] in data["otherDivisionTeamIds"]
        ) and data["myTeam"]["id"] not in [
            x["teams"]["away"]["team"]["id"],
            x["teams"]["home"]["team"]["id"],
        ]
    ]
%>\
% if len(divGames):
${'##'} ${data["myTeam"]["division"]["nameShort"]} Division Scoreboard
% for game in divGames:
<%
    dt = datetime.strptime(game["gameDate"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
    toTz = pytz.timezone(settings.get("Bot", {}).get("TEAM_TIMEZONE", "America/New_York"))
    formattedGameTime = dt.astimezone(toTz).strftime("%I:%M %p")
%>\
% if game["status"]["abstractGameState"] == "Final":
${next((t["teamName"] for t in data["allTeams"] if t["id"] == game["teams"]["away"]["team"]["id"]), "Unknown Team")} (${game["teams"]["away"]["score"]}) @ \
(${game["teams"]["home"]["score"]}) ${next((t["teamName"] for t in data["allTeams"] if t["id"] == game["teams"]["home"]["team"]["id"]), "Unknown Team")} - Final
% elif game["status"]["abstractGameState"] == "Live":
${next((t["teamName"] for t in data["allTeams"] if t["id"] == game["teams"]["away"]["team"]["id"]), "Unknown Team")} (${game["teams"]["away"]["score"]}) @ \
(${game["teams"]["home"]["score"]}) ${next((t["teamName"] for t in data["allTeams"] if t["id"] == game["teams"]["home"]["team"]["id"]), "Unknown Team")} \
- ${game["linescore"]["currentPeriodOrdinal"]} ${game["linescore"]["currentPeriodTimeRemaining"]}
% else:
${next((t["teamName"] for t in data["allTeams"] if t["id"] == game["teams"]["away"]["team"]["id"]), "Unknown Team")} @ \
${next((t["teamName"] for t in data["allTeams"] if t["id"] == game["teams"]["home"]["team"]["id"]), "Unknown Team")} \
- ${formattedGameTime}
% endif

% endfor
% endif  # if len(divGames)