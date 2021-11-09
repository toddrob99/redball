<%
    from datetime import datetime
    team_timezone = settings.get("Bot", {}).get("TEAM_TIMEZONE", "America/New_York")
    def subLink(t):
        return f"[{t.team_city} {t.team_name}]({data['teamSubs'].get(t.team_tricode, '')})"
%>\
% if len(data["todayOtherDivisionGames"]):
${'##'} ${data["myTeam"].team_info.team_division} Division Scoreboard
|Away|Score|Home|Status|
|--:|:-:|:--|:--|
% for game in data["todayOtherDivisionGames"]:
<%
    if game.game_status > 1:
        s = f"{game.away_team.score}-{game.home_team.score}"
    else:
        s = "-"
%>\
|${subLink(game.away_team)}|${s}|${subLink(game.home_team)}|${game.game_status_text.strip()}|
% endfor
% endif  # if len(divGames)