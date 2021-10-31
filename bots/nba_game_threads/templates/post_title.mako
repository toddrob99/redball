<%
    prefix = settings.get("Post Game Thread", {}).get("TITLE_PREFIX","Post Game Thread:")
    away_score = data["game"]["summary"].box_score_summary.away_team.score
    home_score = data["game"]["summary"].box_score_summary.home_team.score
    min_score = min(away_score, home_score)
    max_score = max(away_score, home_score)
    away_team = data["game"]["summary"].box_score_summary.away_team
    home_team = data["game"]["summary"].box_score_summary.home_team
    if data["gameStatus"] >= 3:
        result = (
            "tie" if away_score == home_score
            else "win" if (
                data["homeAway"] == "home" and home_score > away_score
                or data["homeAway"] == "away" and away_score > home_score
            )
            else "loss" if (
                data["homeAway"] == "home" and home_score < away_score
                or data["homeAway"] == "away" and away_score < home_score
            )
            else ""
        )
    else:
        result = None
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
## My Team
The ${data["myTeam"].team_info.team_name} \
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
${data["oppTeam"].team_info.team_name} \
## Score
%if result == "tie":
## TIE
with ${min_score} points each \
%elif result in ["win", "loss"]:
%   if data["game"]["live"].game.period > 4:
in overtime \
%   endif
## WIN / LOSS
with a final score of ${max_score} to ${min_score}\
%else:
## EXCEPTION
%endif
## Date/Time
${(" - " + data["gameTime"]["myTeam"].strftime(settings.get("Post Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))) if settings.get("Post Game Thread", {}).get("TITLE_DATE_FORMAT") != "" else ""}