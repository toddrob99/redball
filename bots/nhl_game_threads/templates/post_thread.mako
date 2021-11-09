<%
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

%if result != "":
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

%if len(data["game"]["liveData"].get("decisions", {})):
<%include file="decisions.mako" />
%endif

<%include file="linescore.mako" />

<%include file="game_stats.mako" />

<%include file="scoring_summary.mako" />

<%include file="penalties.mako" />

<%include file="standings.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Post Game Thread',{}).get('FOOTER','')}