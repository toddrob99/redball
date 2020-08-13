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
        headerLine = "||1|2|3|4|"
        alignmentLine = "|:--|:--|:--|:--|:--|"
        visitorLine = f'|{visitorTeam["nickName"]}|{vs.get("pointsQ1", 0)}|{vs.get("pointsQ2", 0)}|{vs.get("pointsQ3", 0)}|{vs.get("pointsQ4", 0)}|'
        homeLine = f'|{homeTeam["nickName"]}|{hs.get("pointsQ1", 0)}|{hs.get("pointsQ2", 0)}|{hs.get("pointsQ3", 0)}|{hs.get("pointsQ4", 0)}|'
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
        headerLine += "TOTAL|"
        alignmentLine += ":--|"
        visitorLine += f"{vs['pointsTotal']}|"
        homeLine += f"{hs['pointsTotal']}|"
%>\
${headerLine}
${alignmentLine}
${visitorLine}
${homeLine}