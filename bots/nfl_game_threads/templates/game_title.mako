<%
    from datetime import datetime
    prefix = settings.get("Game Thread", {}).get("TITLE_PREFIX","Game Thread:")
    game = data["todayGames"][data["myGameIndex"]]
    myTeamStandings = next((
        x.get("standings", {}).get("data", {})[0]
        for x in data["standings"] 
        if x["abbr"] == data["myTeam"]["abbr"]
    ), {})
    myTeamRecord = (
        f" ({myTeamStandings['overallWins']}-{myTeamStandings['overallLosses']}{'-'+str(myTeamStandings['overallTies']) if myTeamStandings['overallTies'] > 0 else ''})"
        if len(myTeamStandings)
        else " (0-0)"
        ##if data["currentWeek"]["weekType"] != "REG"
        ##else ""
    )
    oppTeamStandings = next((
        x.get("standings", {}).get("data", {})[0]
        for x in data["standings"] 
        if x["abbr"] == data["oppTeam"]["abbr"]
    ), {})
    oppTeamRecord = (
        f" ({oppTeamStandings['overallWins']}-{oppTeamStandings['overallLosses']}{'-'+str(oppTeamStandings['overallTies']) if oppTeamStandings['overallTies'] > 0 else ''})"
        if len(oppTeamStandings)
        else " (0-0)"
        ##if data["currentWeek"]["weekType"] == "REG"
        ##else ""
    )
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
## Week
%if data["currentWeek"]["weekType"] == "HOF":
Hall of Fame Game - 
%elif data["currentWeek"]["weekType"] == "PRE":
Preseason Week ${data["currentWeek"]["week"]} - 
%elif data["currentWeek"]["weekType"] == "REG":
Week ${data["currentWeek"]["week"]} - 
%elif data["currentWeek"]["weekType"] == "WC":
Wild Card Game - 
%elif data["currentWeek"]["weekType"] == "DIV":
Divisional Playoff Game - 
%elif data["currentWeek"]["weekType"] == "CONF":
${data["myTeam"]["conference"]["abbr"]} Champsionship Game - 
%elif data["currentWeek"]["weekType"] == "PRO":
Pro Bowl - 
%elif data["currentWeek"]["weekType"] == "SB":
SUPER BOWL - 
%endif
## Visiting Team
${game["visitorTeam"]["fullName"]}${myTeamRecord if data["homeVisitor"] == "visitor" else oppTeamRecord} \
@ \
## Home Team
${game["homeTeam"]["fullName"]}${myTeamRecord if data["homeVisitor"] == "home" else oppTeamRecord} \
- \
## Date/Time
${data["gameTime"]["myTeam"].strftime(settings.get("Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}