<%
    from datetime import datetime
    team_timezone = settings.get("Bot", {}).get("TEAM_TIMEZONE", "America/New_York")
    def subLink(t):
        return f"[{t.team_name}]({data['teamSubs'].get(t.team_tricode, '')})"
%>\
% if len(data["todayOtherDivisionGames"]):
${'##'} ${data["myTeam"].team_info.team_division} Division Scoreboard
% for game in data["todayOtherDivisionGames"]:
<%
    d = convert_timezone(  # Convert Zulu to my team TZ
        datetime.strptime(
            game.game_time_utc,
            "%Y-%m-%dT%H:%M:%SZ",
        ),
        team_timezone,
    )
    formattedGameTime = d.strftime("%I:%M %p %Z")
%>\
${subLink(game.away_team)} \
%   if game.game_status > 1:
(${game.away_team.score}) \
%   endif
@ \
%   if game.game_status > 1:
(${game.home_team.score}) \
%   endif
${subLink(game.home_team)} \
- ${game.game_status_text.strip()}

% endfor
% endif  # if len(divGames)