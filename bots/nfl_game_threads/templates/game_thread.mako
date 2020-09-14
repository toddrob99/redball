<%
    from datetime import datetime
    game = data["todayGames"][data["myGameIndex"]]
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
${game["visitorTeam"]["fullName"]} \
@ \
## Home Team
${game["homeTeam"]["fullName"]}

## Date/Time
Game Time: ${data["gameTime"]["myTeam"].strftime(settings.get("Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}

Venue: ${game["venue"]["name"]}

%if game["gameStatus"]["phase"] == "INGAME":
${'##'} Game Status\
${f" - {qtrDesc[data['gameDetails']['period']]}" if data["gameDetails"].get("period") else ""} - \
${game["gameStatus"]["gameClock"]}

% if game["gameStatus"].get("possessionTeam"):
${game["gameStatus"].get("possessionTeam", {}).get("abbr")} &#127944; \
${downDesc[game["gameStatus"]["down"]]} and ${"Goal" if game["gameStatus"].get("goalToGo") else game["gameStatus"]["yardsToGo"]} @ \
${game["gameStatus"].get("yardLineSide", "")} ${game["gameStatus"].get("yardLineNumber", "")} yard line
% endif
%elif game["gameStatus"]["phase"] == "HALFTIME":
${'##'} Game Status: HALFTIME
%endif

%if game["gameStatus"]["phase"] in ["INGAME", "HALFTIME", "FINAL", "FINAL_OVERTIME"]:
## Only include the line score if the game has already started
<%include file="linescore.mako" />
%endif

%if game["gameStatus"]["phase"] != "PREGAME":

<%include file="scoring_drives.mako" />

<%include file="game_stats.mako" />
%endif

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Game Thread',{}).get('FOOTER','')}