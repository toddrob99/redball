<%
    from datetime import datetime
    game = data["todayGames"][data["myGameIndex"]]
    myTeamStandings = next((
        x.get("standings", {}).get("data", {})[0]
        for x in data["standings"] 
        if x["abbr"] == data["myTeam"]["abbr"]
    ), {})
    myTeamRecord = (
        f" ({myTeamStandings['overallWins']}-{myTeamStandings['overallLosses']}{'-'+str(myTeamStandings['overallTies']) if myTeamStandings['overallTies'] > 0 else ''})"
        if len(myTeamStandings)
        else ""
        ##if data["currentWeek"]["weekType"] == "REG"
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
        else ""
        ##if data["currentWeek"]["weekType"] == "REG"
        ##else ""
    )
%>\
## Week
%if data["currentWeek"]["weekType"] == "HOF":
# Hall of Fame Game

%elif data["currentWeek"]["weekType"] == "PRE":
# Preseason Week ${data["currentWeek"]["week"]}

%elif data["currentWeek"]["weekType"] == "REG":
# Week ${data["currentWeek"]["week"]}

%elif data["currentWeek"]["weekType"] == "WC":
# Wild Card Game

%elif data["currentWeek"]["weekType"] == "DIV":
# Divisional Playoff Game

%elif data["currentWeek"]["weekType"] == "CONF":
# ${data["myTeam"]["conference"]["abbr"]} Champsionship Game

%elif data["currentWeek"]["weekType"] == "PRO":
# Pro Bowl

%elif data["currentWeek"]["weekType"] == "SB":
# SUPER BOWL

%endif
## Visiting Team
${game["visitorTeam"]["fullName"]}${myTeamRecord if data["homeVisitor"] == "visitor" else oppTeamRecord} \
@ \
## Home Team
${game["homeTeam"]["fullName"]}${myTeamRecord if data["homeVisitor"] == "home" else oppTeamRecord}

## Date/Time
Game Time: ${data["gameTime"]["myTeam"].strftime(settings.get("Tailgate Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}

<%include file="venue_weather.mako" />

<%include file="standings.mako" />

<%include file="inactives.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Tailgate Thread',{}).get('FOOTER','')}