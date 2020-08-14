<%
    from datetime import datetime
    prefix = settings.get("Post Game Thread", {}).get("TITLE_PREFIX","Post Game Thread:")
    game = data["todayGames"][data["myGameIndex"]]
    oppHomeVisitor = "visitor" if data["homeVisitor"] == "home" else "home"
    result = (
        "tie" if game[data["homeVisitor"] + "TeamScore"]["pointsTotal"] == game[oppHomeVisitor + "TeamScore"]["pointsTotal"]
        else "win" if game[data["homeVisitor"] + "TeamScore"]["pointsTotal"] > game[oppHomeVisitor + "TeamScore"]["pointsTotal"]
        else "loss" if game[data["homeVisitor"] + "TeamScore"]["pointsTotal"] < game[oppHomeVisitor + "TeamScore"]["pointsTotal"]
        else ""
    )
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
${data["myTeam"]["conference"]["abbr"]} Champsionship Game - \
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
with ${game["homeTeamScore"]["pointsTotal"]} points each \
%elif result == "win":
## WIN
by a score of ${game[data["homeVisitor"] + "TeamScore"]["pointsTotal"]} to ${game[oppHomeVisitor + "TeamScore"]["pointsTotal"]} \
%elif result == "loss":
## LOSS
by a score of ${game[oppHomeVisitor + "TeamScore"]["pointsTotal"]} to ${game[data["homeVisitor"] + "TeamScore"]["pointsTotal"]} \
%else:
## EXCEPTION
%endif
- \
## Date/Time
${data["gameTime"]["myTeam"].strftime(settings.get("Post Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}