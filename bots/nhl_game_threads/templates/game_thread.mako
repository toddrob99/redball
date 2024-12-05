<%
    from datetime import datetime, timedelta
    if data["game"]["gameState"] in ["FINAL", "OFF", "OVER"] or data["game"].get("gameScheduleState") in ["PPD", "SUSP", "CNCL"]:
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
    else:
        result = None
    oppHomeAway = "away" if data["homeAway"] == "home" else "home"
    if data["standings"]:
        myTeamStandingsData = next((x for x in data["standings"] if x["teamAbbrev"].get("default") == data["myTeam"]["abbrev"]), {})
        myTeamRecord = f" ({myTeamStandingsData.get('wins', 0)}-{myTeamStandingsData.get('losses', 0)}{'-'+str(myTeamStandingsData['otLosses']) if myTeamStandingsData.get('otLosses', 0) > 0 else ''})" if myTeamStandingsData else ""
        oppTeamStandingsData = next((x for x in data["standings"] if x["teamAbbrev"].get("default") == data["oppTeam"]["abbrev"]), {})
        oppTeamRecord = f" ({oppTeamStandingsData.get('wins', 0)}-{oppTeamStandingsData.get('losses', 0)}{'-'+str(oppTeamStandingsData['otLosses']) if oppTeamStandingsData.get('otLosses', 0) > 0 else ''})" if oppTeamStandingsData else ""
    else:
        myTeamRecord = ""
        oppTeamRecord = ""

    homeTeam = data["myTeam"] if data["homeAway"] == "home" else data["oppTeam"]
    awayTeam = data["myTeam"] if data["homeAway"] == "away" else data["oppTeam"]
    maxScore = max(int(data["game"].get("awayTeam", {}).get("score", 0)), int(data["game"].get("homeTeam", {}).get("score", 0)))
    minScore = min(int(data["game"].get("awayTeam", {}).get("score", 0)), int(data["game"].get("homeTeam", {}).get("score", 0)))
    ordDict = {1:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},2:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},3:{1:'1st',2:'2nd',3:'3rd',4:'OT1',5:'OT2',6:'OT3',7:'OT4',8:'OT5'}}
    periodOrd = ordDict[data["game"]["gameType"]]
%>\
## Visiting Team
${'##'} [${awayTeam["name"]["default"]}](${data["teamSubs"][awayTeam["abbrev"]]})${myTeamRecord if data["homeAway"] == "away" else oppTeamRecord} \
@ \
## Home Team
[${homeTeam["name"]["default"]}](${data["teamSubs"][homeTeam["abbrev"]]})${myTeamRecord if data["homeAway"] == "home" else oppTeamRecord}

<%include file="game_info.mako" />

%if data["game"]["gameState"] in ["LIVE", "CRIT"]:
${'##'} Game Status - \
%   if data["game_boxscore"].get("periodDescriptor", {}).get("periodType") == "SO":
<%
    shootout_data = data["game_boxscore"].get("boxscore", {}).get("linescore", {}).get("shootout", {})
%>
Shootout! ${data["game"]["awayTeam"].get("name", data["game"]["awayTeam"]["commonName"])["default"]}: ${shootout_data.get("awayConversions", 0)}/${shootout_data.get("awayAttempts", 0)}, ${data["game"]["homeTeam"].get("name", data["game"]["homeTeam"]["commonName"])["default"]}: ${shootout_data.get("homeConversions", 0)}/${shootout_data.get("homeAttempts", 0)}
%   elif data["game"].get("clock", {}).get("inIntermission"):
Intermission
%   else:
${periodOrd[data["game_boxscore"].get("period", data["game_boxscore"].get("periodDescriptor", {}).get("number"))]}${' Period' if data["game_boxscore"].get("period", data["game_boxscore"].get("periodDescriptor", {}).get("number")) <= 3 else ''} - ${data["game"]["clock"]["timeRemaining"]} \
##%       if data["game"]["liveData"]["linescore"]["teams"]["away"]["powerPlay"]:
##- ${data["game"]["gameData"]["teams"]["away"]["teamName"]} Power Play (${data["game"]["liveData"]["linescore"]["teams"]["away"]["numSkaters"]} on ${data["game"]["liveData"]["linescore"]["teams"]["home"]["numSkaters"]}) \
##%       elif data["game"]["liveData"]["linescore"]["teams"]["home"]["powerPlay"]:
##- ${data["game"]["gameData"]["teams"]["home"]["teamName"]} Power Play (${data["game"]["liveData"]["linescore"]["teams"]["home"]["numSkaters"]} on ${data["game"]["liveData"]["linescore"]["teams"]["away"]["numSkaters"]}) \
##%       endif
##%       if data["game"]["liveData"]["linescore"]["teams"]["away"]["goaliePulled"]:
##- ${data["game"]["gameData"]["teams"]["away"]["teamName"]} Goalie Pulled \
##%       endif
##%       if data["game"]["liveData"]["linescore"]["teams"]["home"]["goaliePulled"]:
##- ${data["game"]["gameData"]["teams"]["home"]["teamName"]} Goalie Pulled \
##%   endif
% endif

%elif result == "postponed":
${'##'} Game Status: Postponed
%elif result:
${'##'} Final${f'/{periodOrd[data["game_boxscore"].get("period", data["game_boxscore"].get("periodDescriptor", {}).get("number"))]}' if data["game_boxscore"].get("period", data["game_boxscore"].get("periodDescriptor", {}).get("number")) > 3 else ""}: \
${maxScore} - ${minScore} \
%   if result == "tie":
TIE
%   elif result == "win":
${data["myTeam"]["commonName"]["default"]}
%   elif result == "loss":
${data["oppTeam"]["commonName"]["default"]}
%   endif
%endif

%if data["game"]["gameState"] in ["FINAL", "OFF", "OVER"] and len(data["game"].get("summary", {}).get("threeStars", {})):
## Only include decisions if the game has ended
<%include file="decisions.mako" />

%endif
%if data["game"]["gameState"] in ["LIVE", "CRIT", "OFF", "OVER", "FINAL"]:
## Only include the line score if the game has already started
<%include file="linescore.mako" />

<%include file="scoring_summary.mako" />

<%include file="penalties.mako" />

%endif
%if data["game"]["gameState"] in ["FUT", "PRE"] and data["game"].get("gameScheduleState") not in ["PPD", "SUSP", "CNCL"]:
<%include file="skaters.mako" />

%endif
%if data["game"].get("gameScheduleState") not in ["PPD", "SUSP", "CNCL"]:
<%include file="scratches.mako" />

%endif

%if data["game"]["gameState"] in ["LIVE", "CRIT", "OFF", "OVER", "FINAL"]:
<%include file="game_stats.mako" />

%endif
<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Game Thread',{}).get('FOOTER','')}