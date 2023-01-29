<%
    from datetime import datetime
    game = data["todayGames"][data["myGameIndex"]]
    gameDetails = data["gameDetails"]
    qtrDesc = {
        1: "1st Quarter",
        2: "2nd Quarter",
        3: "3rd Quarter",
        4: "4th Quarter",
        5: "Overtime",
        6: "Second Overtime",
        7: "Third Overtime",
        8: "Fourth Overtime",
        9: "Fifth Overtime",
        10: "Sixth Overtime",
    }
    downDesc = {
        1: "1st",
        2: "2nd",
        3: "3rd",
        4: "4th",
    }
    ##oppHomeAway = "away" if data["homeAway"] == "home" else "home"
    if gameDetails.get("phase", "SCHEDULED") in ["FINAL", "FINAL_OVERTIME"]:
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
    else:
        result = None
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
# SUPER BOWL

%endif
## Visiting Team
${game["awayTeam"]["fullName"]} \
@ \
## Home Team
${game["homeTeam"]["fullName"]}

## Date/Time
Game Time: ${data["gameTime"]["myTeam"].strftime(settings.get("Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}

<%include file="venue_weather.mako" />

%if gameDetails.get("phase", "SCHEDULED") == "INGAME":
${'##'} Game Status\
${f" - {qtrDesc[gameDetails['period']]}" if gameDetails.get("period") else ""} - \
${gameDetails["gameClock"]}

% if gameDetails.get("possessionTeam") and gameDetails.get("down"):
${gameDetails.get("possessionTeam", {}).get("abbreviation")} &#127944; \
${downDesc[gameDetails["down"]]} and ${"Goal" if gameDetails.get("goalToGo") else gameDetails["yardsToGo"]} @ \
${gameDetails.get("yardLine", "")} yard line
% endif
%elif gameDetails.get("phase", "SCHEDULED") == "HALFTIME":
${'##'} Game Status: HALFTIME
%elif gameDetails.get("phase", "SCHEDULED") == "SUSPENDED":
${'##'} Game Status: SUSPENDED
%elif result:
${'##'} Final Score${f" (Overtime)" if gameDetails.get("phase", "SCHEDULED") == "FINAL_OVERTIME" else ""}: \
${max(int(gameDetails["homePointsTotal"]), int(gameDetails["visitorPointsTotal"]))}\
-\
${min(int(gameDetails["homePointsTotal"]), int(gameDetails["visitorPointsTotal"]))} \
%if result == "tie":
TIE
%elif result == "win":
${data["myTeam"]["nickName"]}
%elif result == "loss":
${data["oppTeam"]["nickName"]}
%endif
%endif

%if gameDetails.get("phase", "SCHEDULED") in ["INGAME", "HALFTIME", "FINAL", "FINAL_OVERTIME"]:
## Only include the line score if the game has already started
<%include file="linescore.mako" />
%endif

%if gameDetails.get("phase", "SCHEDULED") != "PREGAME":

<%include file="scoring_drives.mako" />
##
##<%include file="drive_summary.mako" />

<%include file="game_stats.mako" />
%else:

<%include file="inactives.mako" />

%endif

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Game Thread',{}).get('FOOTER','')}