<%
    game = data["todayGames"][data["myGameIndex"]]
    gameDetails = data["gameDetails"]
    result = (
        "tie" if gameDetails["homePointsTotal"] == gameDetails["visitorPointsTotal"]
        else "win" if (
            data["homeAway"] == "home" and gameDetails["homePointsTotal"] > gameDetails["visitorPointsTotal"]
            or data["homeAway"] == "away" and gameDetails["visitorPointsTotal"] > gameDetails["homePointsTotal"]
        )
        else "loss" if (
            data["homeAway"] == "home" and gameDetails["homePointsTotal"] < gameDetails["visitorPointsTotal"]
            or data["homeAway"] == "away" and gameDetails["visitorPointsTotal"] < gameDetails["homePointsTotal"]
        )
        else ""
    )
    maxScore = max(int(gameDetails["homePointsTotal"]), int(gameDetails["visitorPointsTotal"]))
    minScore = min(int(gameDetails["homePointsTotal"]), int(gameDetails["visitorPointsTotal"]))
    myTeamStandings = next((
        x
        for x in data["standings"]
        if x["team"]["id"] == data["myTeam"]["id"]
    ), None)
    myTeamRecord = (
        f" ({myTeamStandings['overall']['wins']}-{myTeamStandings['overall']['losses']}{'-'+str(myTeamStandings['overall']['ties']) if myTeamStandings['overall']['ties'] > 0 else ''})"
        ##if data["currentWeek"]["weekType"] == "REG"
        ##else ""
    ) if myTeamStandings else ""
    oppTeamStandings = next((
        x
        for x in data["standings"] 
        if x["team"]["id"] == data["oppTeam"]["id"]
    ), None)
    oppTeamRecord = (
        f" ({oppTeamStandings['overall']['wins']}-{oppTeamStandings['overall']['losses']}{'-'+str(oppTeamStandings['overall']['ties']) if oppTeamStandings['overall']['ties'] > 0 else ''})"
        ##if data["currentWeek"]["weekType"] == "REG"
        ##else ""
    ) if oppTeamStandings else ""
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
# ${data["myTeam"]["conferenceAbbr"]} Championship Game

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
${game["awayTeam"]["fullName"]}${myTeamRecord if data["homeAway"] == "away" else oppTeamRecord} \
@ \
## Home Team
${game["homeTeam"]["fullName"]}${myTeamRecord if data["homeAway"] == "home" else oppTeamRecord}

%if result != "":
${'##'} Final Score${f" (Overtime)" if gameDetails["phase"] == "FINAL_OVERTIME" else ""}: \
${maxScore}-${minScore} \
%if result == "tie":
TIE
%elif result == "win":
${data["myTeam"]["nickName"]}
%elif result == "loss":
${data["oppTeam"]["nickName"]}
%endif
%endif

## Date/Time
Game Time: ${data["gameTime"]["myTeam"].strftime(settings.get("Post Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}

Venue: ${game["venue"]["name"]}

<%include file="linescore.mako" />

<%include file="scoring_drives.mako" />
##
##<%include file="drive_summary.mako" />

<%include file="game_stats.mako" />

<%include file="standings.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Post Game Thread',{}).get('FOOTER','')}