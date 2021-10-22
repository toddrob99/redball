<%
    prefix = settings.get("Tailgate Thread", {}).get("TITLE_PREFIX","Tailgate Thread:")
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

<%include file="skaters.mako" />

<%include file="scratches.mako" />

<%include file="standings.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Tailgate Thread',{}).get('FOOTER','')}