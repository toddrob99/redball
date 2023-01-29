<%
    from datetime import datetime
    prefix = settings.get("Post Game Thread", {}).get("TITLE_PREFIX","Post Game Thread:")
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
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
## Week
%if data["currentWeek"]["weekType"] == "HOF":
Hall of Fame Game - \
%elif data["currentWeek"]["weekType"] == "PRE":
Preseason Week ${data["currentWeek"]["week"]} - \
%elif data["currentWeek"]["weekType"] == "REG":
Week ${data["currentWeek"]["week"]} - \
%elif data["currentWeek"]["weekType"] == "WC":
Wild Card Game - \
%elif data["currentWeek"]["weekType"] == "DIV":
Divisional Playoff Game - \
%elif data["currentWeek"]["weekType"] == "CONF":
${data["myTeam"]["conferenceAbbr"]} Championship Game - \
%elif data["currentWeek"]["weekType"] == "PRO":
Pro Bowl - \
%elif data["currentWeek"]["weekType"] == "SB":
SUPER BOWL${" CHAMPIONS!" if result=="win" else " -"} \
%endif
## My Team
The ${data["myTeam"]["nickName"]} \
## Result
%if result == "tie":
## TIE
tied the \
%elif result == "win":
## WIN
defeated the \
%elif result == "loss":
## LOSS
fell to the \
%else:
## EXCEPTION
were supposed to play the \
%endif
## Opposing Team
${data["oppTeam"]["nickName"]} \
## Score
%if result == "tie":
## TIE
with ${gameDetails["visitorPointsTotal"]} points each \
%elif result in ["win", "loss"]:
## WIN / LOSS
by a score of ${maxScore} to ${minScore} \
%else:
## EXCEPTION
%endif
- \
## Date/Time
${data["gameTime"]["myTeam"].strftime(settings.get("Post Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}