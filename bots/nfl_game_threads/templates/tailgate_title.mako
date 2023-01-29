<%
    from datetime import datetime
    prefix = settings.get("Tailgate Thread", {}).get("TITLE_PREFIX","Tailgate Thread:")
    game = data["todayGames"][data["myGameIndex"]]
    myTeamStandings = next((
        x
        for x in data["standings"]
        if x["team"]["id"] == data["myTeam"]["id"]
    ), None)
    myTeamRecord = (
        f" ({myTeamStandings['overall']['wins']}-{myTeamStandings['overall']['losses']}{'-'+str(myTeamStandings['overall']['ties']) if myTeamStandings['overall']['ties'] > 0 else ''})"
        ##if data["currentWeek"]["weekType"] == "REG"
        ##else ""
    ) if myTeamStandings else ""
    oppTeamStandings = next((
        x
        for x in data["standings"] 
        if x["team"]["id"] == data["oppTeam"]["id"]
    ), None)
    oppTeamRecord = (
        f" ({oppTeamStandings['overall']['wins']}-{oppTeamStandings['overall']['losses']}{'-'+str(oppTeamStandings['overall']['ties']) if oppTeamStandings['overall']['ties'] > 0 else ''})"
        ##if data["currentWeek"]["weekType"] == "REG"
        ##else ""
    ) if oppTeamStandings else ""
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
## Week
%if data["currentWeek"]["weekType"] == "HOF":
Hall of Fame Game - 
%elif data["currentWeek"]["weekType"] == "PRE":
Preseason Week ${data["currentWeek"]["week"]} - 
%elif data["currentWeek"]["weekType"] == "REG":
Week ${data["currentWeek"]["week"]} - 
%elif data["currentWeek"]["weekType"] == "WC":
Wild Card Game - 
%elif data["currentWeek"]["weekType"] == "DIV":
Divisional Playoff Game - 
%elif data["currentWeek"]["weekType"] == "CONF":
${data["myTeam"]["conferenceAbbr"]} Championship Game - 
%elif data["currentWeek"]["weekType"] == "PRO":
Pro Bowl - 
%elif data["currentWeek"]["weekType"] == "SB":
SUPER BOWL - 
%endif
## Visiting Team
${game["awayTeam"]["fullName"]}${myTeamRecord if data["homeAway"] == "away" else oppTeamRecord} \
@ \
## Home Team
${game["homeTeam"]["fullName"]}${myTeamRecord if data["homeAway"] == "home" else oppTeamRecord} \
- \
## Date/Time
${data["gameTime"]["myTeam"].strftime(settings.get("Tailgate Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}