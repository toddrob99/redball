<%
    game = data["todayGames"][data["myGameIndex"]]
    gameDetails = data["gameDetails"]
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    if (
        gameDetails.get("homePointsTotal") is not None
        and gameDetails.get("visitorPointsTotal") is not None
    ):
        headerLine = "||"
        alignmentLine = "|:--|"
        awayLine = f'|{awayTeam["nickName"]}|'
        homeLine = f'|{homeTeam["nickName"]}|'
        for qtr in [str(q) for q in range(1, (
                gameDetails["period"] if isinstance(gameDetails["period"], int) and gameDetails["period"] <= 4
                else 2 if gameDetails["phase"] == "HALFTIME"
                else 4
            ) + 1)]:
            headerLine += f"Q{qtr}|"
            alignmentLine += ":--|"
            awayLine += f"{gameDetails.get('visitorPointsQ'+qtr, '')}|"
            homeLine += f"{gameDetails.get('homePointsQ'+qtr, '')}|"
        if "OVERTIME" in gameDetails["phase"] or (isinstance(gameDetails["period"], int) and gameDetails["period"] > 4):
            headerLine += "OT|"
            alignmentLine += ":--|"
            awayLine += f"{gameDetails.get('visitorPointsOvertime', '')}|"
            homeLine += f"{gameDetails.get('homePointsOvertime', '')}|"
        headerLine += "|TOTAL|"
        alignmentLine += ":--|:--|"
        awayLine += f"|{gameDetails['visitorPointsTotal']}|"
        homeLine += f"|{gameDetails['homePointsTotal']}|"
%>\
${headerLine}
${alignmentLine}
${awayLine}
${homeLine}