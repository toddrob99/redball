<%
    from datetime import datetime
    game = data["todayGames"][data["myGameIndex"]]
    oppHomeVisitor = "visitor" if data["homeVisitor"] == "home" else "home"
    result = (
        "tie" if game[data["homeVisitor"] + "TeamScore"]["pointsTotal"] == game[oppHomeVisitor + "TeamScore"]["pointsTotal"]
        else "win" if game[data["homeVisitor"] + "TeamScore"]["pointsTotal"] > game[oppHomeVisitor + "TeamScore"]["pointsTotal"]
        else "loss" if game[data["homeVisitor"] + "TeamScore"]["pointsTotal"] < game[oppHomeVisitor + "TeamScore"]["pointsTotal"]
        else ""
    )
    myTeamStandings = next((
        x.get("standings", {}).get("data", {})[0]
        for x in data["standings"] 
        if x["abbr"] == data["myTeam"]["abbr"]
    ), {})
    myTeamRecord = (
        f" ({myTeamStandings['overallWins']}-{myTeamStandings['overallLosses']}{'-'+str(myTeamStandings['overallTies']) if myTeamStandings['overallTies'] > 0 else ''})"
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
%if result == "win":
## Boom
# THE ${data["myTeam"]["fullName"].upper()} HAVE WON THE SUPER BOWL!
%else:
# Super Bowl
%endif

%endif
## Make the matchup h2
${'##'} \
## Visiting Team
${game["visitorTeam"]["fullName"]}${myTeamRecord if data["homeVisitor"] == "visitor" else oppTeamRecord} \
@ \
## Home Team
${game["homeTeam"]["fullName"]}${myTeamRecord if data["homeVisitor"] == "home" else oppTeamRecord}

%if result != "":
${'##'} Final Score: \
${max(int(game[data["homeVisitor"] + "TeamScore"]["pointsTotal"]), int(game[oppHomeVisitor + "TeamScore"]["pointsTotal"]))}\
-\
${min(int(game[data["homeVisitor"] + "TeamScore"]["pointsTotal"]), int(game[oppHomeVisitor + "TeamScore"]["pointsTotal"]))} \
%if result == "tie":
TIE
%elif result == "win":
${data["myTeam"]["nickName"]}
%elif result == "loss":
${data["oppTeam"]["nickName"]}
%endif
%endif

## Date/Time
Game Time: ${data["gameTime"]["myTeam"].strftime(settings.get("Tailgate Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}

Venue: ${game["venue"]["name"]}

<%include file="linescore.mako" />

<%include file="scoring_drives.mako" />

<%include file="game_stats.mako" />

<%include file="standings.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Post Game Thread',{}).get('FOOTER','')}