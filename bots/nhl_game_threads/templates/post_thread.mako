<%
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
    maxScore = max(int(data["game"].get("awayTeam", {}).get("score")), int(data["game"].get("homeTeam", {}).get("score")))
    minScore = min(int(data["game"].get("awayTeam", {}).get("score")), int(data["game"].get("homeTeam", {}).get("score")))
    ordDict = {1:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},2:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},3:{1:'1st',2:'2nd',3:'3rd',4:'OT1',5:'OT2',6:'OT3',7:'OT4',8:'OT5'}}
    periodOrd = ordDict[data["game"]["gameType"]]
    def highlight_url(clip_id):
        return f"https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId={clip_id}"
%>\
## Visiting Team
${'##'} [${awayTeam["name"]["default"]}](${data["teamSubs"][awayTeam["abbrev"]]})${myTeamRecord if data["homeAway"] == "away" else oppTeamRecord} \
@ \
## Home Team
[${homeTeam["name"]["default"]}](${data["teamSubs"][homeTeam["abbrev"]]})${myTeamRecord if data["homeAway"] == "home" else oppTeamRecord}

%if result == "postponed":
${'##'} Game Status: Postponed
%elif result != "":
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

% if data["game_boxscore"].get("gameVideo", {}).get("threeMinRecap") or data["game_boxscore"].get("gameVideo", {}).get("condensedGame") or data["game_boxscore"].get("boxscore", {}).get("gameReports"):
${'##'} Game Videos/Summaries
%   if data["game_boxscore"].get("gameVideo", {}).get("threeMinRecap"):
* [Three Minute Recap Video](${highlight_url(data["game_boxscore"]["gameVideo"]["threeMinRecap"])})
%   endif
%   if data["game_boxscore"].get("gameVideo", {}).get("condensedGame"):
* [Condensed Game Video](${highlight_url(data["game_boxscore"]["gameVideo"]["condensedGame"])})
%   endif
%   if data["game_boxscore"].get("boxscore", {}).get("gameReports"):
%       if data["game_boxscore"]["boxscore"]["gameReports"].get("gameSummary"):
* [Game Summary](${data["game_boxscore"]["boxscore"]["gameReports"]["gameSummary"]})
%       endif
%       if data["game_boxscore"]["boxscore"]["gameReports"].get("eventSummary"):
* [Event Summary](${data["game_boxscore"]["boxscore"]["gameReports"]["eventSummary"]})
%       endif
%       if data["game_boxscore"]["boxscore"]["gameReports"].get("playByPlay"):
* [Play by Play](${data["game_boxscore"]["boxscore"]["gameReports"]["playByPlay"]})
%       endif
%       if data["game_boxscore"]["boxscore"]["gameReports"].get("faceoffSummary") or data["game_boxscore"]["boxscore"]["gameReports"].get("faceoffComparison"):
* Face Off \
%           if data["game_boxscore"]["boxscore"]["gameReports"].get("faceoffSummary"):
[Summary](${data["game_boxscore"]["boxscore"]["gameReports"]["faceoffSummary"]}) \
%           endif
%           if data["game_boxscore"]["boxscore"]["gameReports"].get("faceoffComparison"):
[Comparison](${data["game_boxscore"]["boxscore"]["gameReports"]["faceoffComparison"]})
%           endif
%       endif
##%       if data["game_boxscore"]["boxscore"]["gameReports"].get("rosters"):
##* [Rosters](${data["game_boxscore"]["boxscore"]["gameReports"]["rosters"]})
##%       endif
%       if data["game_boxscore"]["boxscore"]["gameReports"].get("shotSummary"):
* [Shot Summary](${data["game_boxscore"]["boxscore"]["gameReports"]["shotSummary"]})
%       endif
%       if data["game_boxscore"]["boxscore"]["gameReports"].get("shootoutSummary"):
* [Shootout Summary](${data["game_boxscore"]["boxscore"]["gameReports"]["shootoutSummary"]})
%       endif
%       if data["game_boxscore"]["boxscore"]["gameReports"].get("shiftChart"):
* [Shift Chart](${data["game_boxscore"]["boxscore"]["gameReports"]["shiftChart"]})
%       endif
%       if data["game_boxscore"]["boxscore"]["gameReports"].get("toiAway") or data["game_boxscore"]["boxscore"]["gameReports"].get("toiHome"):
* TOI Report: \
%           if data["game_boxscore"]["boxscore"]["gameReports"].get("toiAway"):
[${awayTeam["commonName"]["default"]}](${data["game_boxscore"]["boxscore"]["gameReports"]["toiAway"]}) \
%           endif
%           if data["game_boxscore"]["boxscore"]["gameReports"].get("toiHome"):
[${homeTeam["commonName"]["default"]}](${data["game_boxscore"]["boxscore"]["gameReports"]["toiHome"]})
%           endif
%       endif
%   endif
% endif

%if len(data["game"].get("summary", {}).get("threeStars", {})):
<%include file="decisions.mako" />

%endif
%if result != "postponed":
<%include file="linescore.mako" />

<%include file="scoring_summary.mako" />

<%include file="penalties.mako" />

<%include file="game_stats.mako" />

%endif
<%include file="standings.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Post Game Thread',{}).get('FOOTER','')}