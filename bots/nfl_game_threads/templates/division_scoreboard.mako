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
    divGames = [x for x in data["todayGames"] if data["myTeam"]["division"]["abbr"] in [x["visitorTeam"]["division"]["abbr"], x["homeTeam"]["division"]["abbr"]] and data["myTeam"]["id"] not in [x["visitorTeam"]["id"], x["homeTeam"]["id"]]]
%>\
% if len(divGames):
${'##'} Division Scoreboard
% for game in divGames:
<%
    dt = datetime.strptime(game["gameTime"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
    toTz = pytz.timezone(settings.get("Bot", {}).get("TEAM_TIMEZONE", "America/New_York"))
    formattedGameTime = dt.astimezone(toTz).strftime("%I:%M %p")
%>\
|${qtrDesc[game["gameStatus"]["period"]] if game["gameStatus"]["period"] else ""} ${game["gameStatus"]["gameClock"] if game["gameStatus"]["phase"] == "INGAME" else gameStatusDesc[game["gameStatus"]["phase"]] if game["gameStatus"]["phase"] != "PREGAME" else formattedGameTime}||
|:--|:--|
|${game["visitorTeam"]["abbr"]}${" &#127944;" if game["gameStatus"]["period"] and game["gameStatus"]["possessionTeam"] and game["gameStatus"]["possessionTeam"]["abbr"] == game["visitorTeam"]["abbr"] else ""}|${game['visitorTeamScore'].get('pointsTotal', 0) if game["gameStatus"]["phase"] != "PREGAME" else ""}|
|${game["homeTeam"]["abbr"]}${" &#127944;" if game["gameStatus"]["period"] and game["gameStatus"]["possessionTeam"] and game["gameStatus"]["possessionTeam"]["abbr"] == game["homeTeam"]["abbr"] else ""}|${game['homeTeamScore'].get('pointsTotal', 0) if game["gameStatus"]["phase"] != "PREGAME" else ""}|

% endfor
% endif  # if len(divGames)