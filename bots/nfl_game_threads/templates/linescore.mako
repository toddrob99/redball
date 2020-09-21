<%
    game = data["todayGames"][data["myGameIndex"]]
    visitorTeam = (
        data["myTeam"] if data["homeVisitor"] == "visitor"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeVisitor"] == "home"
        else data["oppTeam"]
    )
    if (
        game.get("homeTeamScore", {}).get("pointsTotal") is not None
        and game.get("visitorTeamScore", {}).get("pointsTotal") is not None
    ):
        vs = game["visitorTeamScore"]
        hs = game["homeTeamScore"]
        #headerLine = "||1|2|3|4|"
        headerLine = "||"
        #alignmentLine = "|:--|:--|:--|:--|:--|"
        alignmentLine = "|:--|"
        #visitorLine = f'|{visitorTeam["nickName"]}|{vs.get("pointsQ1", "")}|{vs.get("pointsQ2", "")}|{vs.get("pointsQ3", "")}|{vs.get("pointsQ4", "")}|'
        visitorLine = f'|{visitorTeam["nickName"]}|'
        #homeLine = f'|{homeTeam["nickName"]}|{hs.get("pointsQ1", "")}|{hs.get("pointsQ2", "")}|{hs.get("pointsQ3", "")}|{hs.get("pointsQ4", "")}|'
        homeLine = f'|{homeTeam["nickName"]}|'
        for qtr in [str(q) for q in range(1, (game["gameStatus"]["period"] if game["gameStatus"]["period"] and game["gameStatus"]["phase"] == "INGAME" else 2 if game["gameStatus"]["period"] and game["gameStatus"]["phase"] == "HALFTIME" else 1 if not game["gameStatus"]["period"] else 4) + 1)]:
            headerLine += f"Q{qtr}|"
            alignmentLine += ":--|"
            visitorLine += f"{vs.get('pointsQ'+qtr, '')}|"
            homeLine += f"{hs.get('pointsQ'+qtr, '')}|"
        if game["gameStatus"]["phase"] == "FINAL_OVERTIME" or vs.get("pointsOvertime", {}).get("pointsOvertimeTotal", 0) > 0 or hs.get("pointsOvertime", {}).get("pointsOvertimeTotal", 0) > 0:
            for i, x in [(i, x) for i, x in enumerate(vs.get("pointsOvertime", {}).get("data", []))]:
                if len(vs.get("pointsOvertime", {}).get("data", [])) > 1:
                    headerLine += f"OT{i+1}|"
                    alignmentLine += ":--|"
                    visitorLine += f"{x}|"
                    homeLine += f'{hs.get("pointsOvertime", {}).get("data", [])[i]}|'
                else:
                    headerLine += f"OT|"
                    alignmentLine += ":--|"
                    visitorLine += f"{x}|"
                    homeLine += f'{hs.get("pointsOvertime", {}).get("data", [])[i]}|'
        headerLine += "|TOTAL|"
        alignmentLine += ":--|:--|"
        visitorLine += f"|{vs['pointsTotal']}|"
        homeLine += f"|{hs['pointsTotal']}|"
%>\
${headerLine}
${alignmentLine}
${visitorLine}
${homeLine}