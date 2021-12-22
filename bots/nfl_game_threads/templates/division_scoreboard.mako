<%
    from datetime import datetime
    import pytz
    gameStatusDesc = {
        "PREGAME": "Pre",
        "INGAME": "Live",
        "HALFTIME": "Half",
        "SUSPENDED": "Susp",
        "FINAL": "Final",
        "FINAL_OVERTIME": "F/OT",
    }
    qtrDesc = {
        1: "Q1",
        2: "Q2",
        3: "Q3",
        4: "Q4",
        5: "OT",
        6: "OT2",
        7: "OT3",
        8: "OT4",
        9: "OT5",
        10: "OT6",
    }
    otherDivisionTeamIds = [divTeam["id"] for divTeam in data["otherDivisionTeams"]]
    divGames = [x for x in data["todayGames"] if (x["awayTeam"]["id"] in otherDivisionTeamIds or x["homeTeam"]["id"] in otherDivisionTeamIds) and data["myTeam"]["id"] not in [x["awayTeam"]["id"], x["homeTeam"]["id"]] and data["otherTodayGamesDetails"].get(x["id"])]
%>\
% if len(divGames):
${'##'} Division Scoreboard
% for game in divGames:
<%
    dt = datetime.strptime(game["time"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
    toTz = pytz.timezone(settings.get("Bot", {}).get("TEAM_TIMEZONE", "America/New_York"))
    formattedGameTime = dt.astimezone(toTz).strftime("%I:%M %p")
    gd = data["otherTodayGamesDetails"].get(game["id"], {})
%>\
|${qtrDesc[gd["period"]] if gd.get("period") else ""} ${gd["gameClock"] if gd.get("phase") == "INGAME" else gameStatusDesc[gd["phase"]] if gd.get("phase") != "PREGAME" else formattedGameTime}||
|:--|:--|
|${gd["visitorTeam"]["abbreviation"]}${" &#127944;" if gd.get("period") and gd.get("possessionTeam") and gd["possessionTeam"]["abbreviation"] == gd["visitorTeam"]["abbreviation"] else ""}|${gd.get('visitorPointsTotal', 0) if gd["phase"] != "PREGAME" else ""}|
|${gd["homeTeam"]["abbreviation"]}${" &#127944;" if gd.get("period") and gd.get("possessionTeam") and gd["possessionTeam"]["abbreviation"] == gd["homeTeam"]["abbreviation"] else ""}|${gd.get('homePointsTotal', 0) if gd["phase"] != "PREGAME" else ""}|

% endfor
% endif  # if len(divGames)