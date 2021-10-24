<%
    from datetime import datetime, timedelta
    if data["game"]["gameData"]["status"]["abstractGameState"] == "Final":
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
    else:
        result = None
    oppHomeAway = "away" if data["homeAway"] == "home" else "home"
    myLeagueRecord = data["todayGames"][0]["teams"][data["homeAway"]]['leagueRecord']
    oppLeagueRecord = data["todayGames"][0]["teams"][oppHomeAway]['leagueRecord']
    myTeamRecord = (
        f" ({myLeagueRecord['wins']}-{myLeagueRecord['losses']}{'-'+str(myLeagueRecord['ot']) if myLeagueRecord.get('ot', 0) > 0 else ''})"
    ) if data["todayGames"][0]["teams"][data["homeAway"]].get("leagueRecord") else ""
    oppTeamRecord = (
        f" ({oppLeagueRecord['wins']}-{oppLeagueRecord['losses']}{'-'+str(oppLeagueRecord['ot']) if oppLeagueRecord.get('ot', 0) > 0 else ''})"
    ) if data["todayGames"][0]["teams"][oppHomeAway].get("leagueRecord") else ""
%>\
## Visiting Team
${'##'} [${data["game"]["gameData"]["teams"]["away"]["name"]}](${data["teamSubs"][data["game"]["gameData"]["teams"]["away"]["abbreviation"]]})${myTeamRecord if data["homeAway"] == "away" else oppTeamRecord} \
@ \
## Home Team
[${data["game"]["gameData"]["teams"]["home"]["name"]}](${data["teamSubs"][data["game"]["gameData"]["teams"]["home"]["abbreviation"]]})${myTeamRecord if data["homeAway"] == "home" else oppTeamRecord}

<%include file="game_info.mako" />

%if data["game"]["gameData"]["status"]["abstractGameState"] == "Live":
${'##'} Game Status - \
%   if data["game"]["liveData"]["linescore"]["hasShootout"]:
Shootout! ${data["game"]["gameData"]["teams"]["away"]["teamName"]}: ${data["game"]["liveData"]["linescore"]["shootoutInfo"]["away"]["scores"]}/${data["game"]["liveData"]["linescore"]["shootoutInfo"]["away"]["attempts"]}, ${data["game"]["gameData"]["teams"]["home"]["teamName"]}: ${data["game"]["liveData"]["linescore"]["shootoutInfo"]["home"]["scores"]}/${data["game"]["liveData"]["linescore"]["shootoutInfo"]["home"]["attempts"]}}
%   elif data["game"]["liveData"]["linescore"]["intermissionInfo"].get("inIntermission"):
Intermission, ${str(timedelta(seconds=int(data["game"]["liveData"]["linescore"]["intermissionInfo"]["intermissionTimeRemaining"])))[-5:]} Remaining
%   else:
${data["game"]["liveData"]["linescore"]["currentPeriodOrdinal"]}${' Period' if data["game"]["liveData"]["linescore"]["currentPeriod"] <= 3 else ''} - ${data["game"]["liveData"]["linescore"]["currentPeriodTimeRemaining"]} \
%       if data["game"]["liveData"]["linescore"]["teams"]["away"]["powerPlay"]:
- ${data["game"]["gameData"]["teams"]["away"]["teamName"]} Power Play (${data["game"]["liveData"]["linescore"]["teams"]["away"]["numSkaters"]} on ${data["game"]["liveData"]["linescore"]["teams"]["home"]["numSkaters"]}) \
%       elif data["game"]["liveData"]["linescore"]["teams"]["home"]["powerPlay"]:
- ${data["game"]["gameData"]["teams"]["home"]["teamName"]} Power Play (${data["game"]["liveData"]["linescore"]["teams"]["home"]["numSkaters"]} on ${data["game"]["liveData"]["linescore"]["teams"]["away"]["numSkaters"]}) \
%       endif
%       if data["game"]["liveData"]["linescore"]["teams"]["away"]["goaliePulled"]:
- ${data["game"]["gameData"]["teams"]["away"]["teamName"]} Goalie Pulled \
%       endif
%       if data["game"]["liveData"]["linescore"]["teams"]["home"]["goaliePulled"]:
- ${data["game"]["gameData"]["teams"]["home"]["teamName"]} Goalie Pulled \
%   endif
% endif

%elif result:
${'##'} Final${f'/{data["game"]["liveData"]["linescore"]["currentPeriodOrdinal"]}' if data["game"]["liveData"]["linescore"]["currentPeriod"] > 3 else ""}: \
${max(int(data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"]), int(data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"]))}\
-\
${min(int(data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"]), int(data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"]))} \
%   if result == "tie":
TIE
%   elif result == "win":
${data["myTeam"]["teamName"]}
%   elif result == "loss":
${data["oppTeam"]["teamName"]}
%   endif
%endif

%if data["game"]["gameData"]["status"]["abstractGameState"] == "Final" and len(data["game"]["liveData"].get("decisions", {})):
## Only include decisions if the game has ended
<%include file="decisions.mako" />

%endif
%if data["game"]["gameData"]["status"]["abstractGameState"] in ["Live", "Final"]:
## Only include the line score if the game has already started
<%include file="linescore.mako" />

%endif
%if data["game"]["gameData"]["status"]["abstractGameState"] == "Preview":
<%include file="skaters.mako" />


<%include file="scratches.mako" />

%endif
%if data["game"]["gameData"]["status"]["abstractGameState"] in ["Live", "Final"]:
<%include file="game_stats.mako" />

%endif
%if data["game"]["gameData"]["status"]["abstractGameState"] != "Preview":
<%include file="scoring_summary.mako" />

<%include file="penalties.mako" />

%endif
<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Game Thread',{}).get('FOOTER','')}