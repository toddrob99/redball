<%
    prefix = settings.get("Post Game Thread", {}).get("TITLE_PREFIX","Post Game Thread:")
    result = (
        "postponed" if data["game"].get("gameScheduleState") == "PPD"
        else "suspended" if data["game"].get("gameScheduleState") == "SUSP"
        else "canceled" if data["game"].get("gameScheduleState") == "CNCL"
        else "tie" if data["game"].get("awayTeam", {}).get("score") == data["game"].get("homeTeam", {}).get("score")
        else "win" if (
            data["homeAway"] == "home" and data["game"].get("homeTeam", {}).get("score") > data["game"].get("awayTeam", {}).get("score")
            or data["homeAway"] == "away" and data["game"].get("awayTeam", {}).get("score") > data["game"].get("homeTeam", {}).get("score")
        )
        else "loss" if (
            data["homeAway"] == "home" and data["game"].get("homeTeam", {}).get("score") < data["game"].get("awayTeam", {}).get("score")
            or data["homeAway"] == "away" and data["game"].get("awayTeam", {}).get("score") < data["game"].get("homeTeam", {}).get("score")
        )
        else ""
    )
    maxScore = max(int(data["game"].get("awayTeam", {}).get("score")), int(data["game"].get("homeTeam", {}).get("score")))
    minScore = min(int(data["game"].get("awayTeam", {}).get("score")), int(data["game"].get("homeTeam", {}).get("score")))
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
## My Team
The ${data["myTeam"]["commonName"]["default"]} \
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
%elif result == "postponed":
will have to wait to play the \
%elif result == "suspended":
will have to wait to finish playing the \
%else:
## EXCEPTION
were supposed to play the \
%endif
## Opposing Team
${data["oppTeam"]["commonName"]["default"]} \
## Score
%if result == "tie":
## TIE
with ${minScore} goals each \
%elif result in ["win", "loss"]:
%   if data["game_pbp"].get("periodDescriptor", {}).get("periodType") == "OT":
in${' double' if data["game_pbp"].get("periodDescriptor", {}).get("otPeriods") == 2 else ' triple' if data["game_pbp"].get("periodDescriptor", {}).get("otPeriods") == 3 else ' quadruple' if data["game_pbp"].get("periodDescriptor", {}).get("otPeriods") == 4 else ' quintuple' if data["game_pbp"].get("periodDescriptor", {}).get("otPeriods") == 5 else ' sextuple' if data["game_pbp"].get("periodDescriptor", {}).get("otPeriods") == 6 else ''} overtime \
%   elif data["game_pbp"].get("periodDescriptor", {}).get("periodType") == "SO":
in a shootout \
%   endif
## WIN / LOSS
with a final score of ${maxScore} to ${minScore} \
%else:
## EXCEPTION
%endif
- \
% if data["game"].get("gameScheduleState") == "PPD":
## Postponed
POSTPONED
% elif data["game"].get("gameScheduleState") == "SUSP":
SUSPENDED
% elif data["game"].get("gameScheduleState") == "CNCL":
CANCELED
% else:
## Date/Time
${data["gameTime"]["myTeam"].strftime(settings.get("Post Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}
% endif