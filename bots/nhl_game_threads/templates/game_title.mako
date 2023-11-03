<%
    prefix = settings.get("Game Thread", {}).get("TITLE_PREFIX","Game Thread:")
    oppHomeAway = "away" if data["homeAway"] == "home" else "home"
    if data["standings"]:
        myTeamStandingsData = next((x for x in data["standings"] if x["teamAbbrev"].get("default") == data["myTeam"]["abbrev"]), {})
        myTeamRecord = f" ({myTeamStandingsData.get('wins', 0)}-{myTeamStandingsData.get('losses', 0)}{'-'+str(myTeamStandingsData['otLosses']) if myTeamStandingsData.get('otLosses', 0) > 0 else ''})" if myTeamStandingsData else ""
        oppTeamStandingsData = next((x for x in data["standings"] if x["teamAbbrev"].get("default") == data["oppTeam"]["abbrev"]), {})
        oppTeamRecord = f" ({oppTeamStandingsData.get('wins', 0)}-{oppTeamStandingsData.get('losses', 0)}{'-'+str(oppTeamStandingsData['otLosses']) if oppTeamStandingsData.get('otLosses', 0) > 0 else ''})" if oppTeamStandingsData else ""
    else:
        myTeamRecord = ""
        oppTeamRecord = ""
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
## Visiting Team
${data["myTeam"]["name"]["default"] if data["homeAway"] == "away" else data["oppTeam"]["name"]["default"]}${myTeamRecord if data["homeAway"] == "away" else oppTeamRecord} \
@ \
## Home Team
${data["myTeam"]["name"]["default"] if data["homeAway"] == "home" else data["oppTeam"]["name"]["default"]}${myTeamRecord if data["homeAway"] == "home" else oppTeamRecord} \
- \
% if data["game"].get("gameScheduleState") == "PPD":
POSTPONED
% elif data["game"].get("gameScheduleState") == "SUSP":
SUSPENDED
% elif data["game"].get("gameScheduleState") == "CNCL":
CANCELED
% else:
## Date/Time
${data["gameTime"]["myTeam"].strftime(settings.get("Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}
% endif