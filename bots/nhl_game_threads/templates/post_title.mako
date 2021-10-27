<%
    prefix = settings.get("Post Game Thread", {}).get("TITLE_PREFIX","Post Game Thread:")
    result = (
        "tie" if data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"] == data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"]
        else "win" if (
            data["homeAway"] == "home" and data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"] > data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"]
            or data["homeAway"] == "away" and data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"] > data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"]
        )
        else "loss" if (
            data["homeAway"] == "home" and data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"] < data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"]
            or data["homeAway"] == "away" and data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"] < data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"]
        )
        else ""
    )
    maxScore = max(int(data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"]), int(data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"]))
    minScore = min(int(data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"]), int(data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"]))
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
## My Team
The ${data["myTeam"]["teamName"]} \
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
${data["oppTeam"]["teamName"]} \
## Score
%if result == "tie":
## TIE
with ${minScore} goals each \
%elif result in ["win", "loss"]:
%   if data["game"]["liveData"]["linescore"]["currentPeriodOrdinal"] == "OT":
in overtime \
%   elif data["game"]["liveData"]["linescore"]["currentPeriodOrdinal"] == "SO":
in a shootout \
%   endif
## WIN / LOSS
with a final score of ${maxScore} to ${minScore} \
%else:
## EXCEPTION
%endif
- \
## Date/Time
${data["gameTime"]["myTeam"].strftime(settings.get("Post Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}