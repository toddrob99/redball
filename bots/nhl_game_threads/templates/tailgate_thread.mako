<%
    prefix = settings.get("Tailgate Thread", {}).get("TITLE_PREFIX","Tailgate Thread:")
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
%>\
## Visiting Team
${'##'} [${awayTeam["name"]["default"]}](${data["teamSubs"][awayTeam["abbrev"]]})${myTeamRecord if data["homeAway"] == "away" else oppTeamRecord} \
@ \
## Home Team
[${homeTeam["name"]["default"]}](${data["teamSubs"][homeTeam["abbrev"]]})${myTeamRecord if data["homeAway"] == "home" else oppTeamRecord}

<%include file="game_info.mako" />

<%include file="skaters.mako" />

<%include file="scratches.mako" />

<%include file="standings.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Tailgate Thread',{}).get('FOOTER','')}