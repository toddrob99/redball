<%
    from datetime import datetime
    import tzlocal
    if not data.get("next_game"):
        return
    if not data["next_game"].away_team.team_id or not data["next_game"].home_team.team_id:
        return
    team_timezone = settings.get("Bot", {}).get("TEAM_TIMEZONE", "America/New_York")
    game_datetime = convert_timezone(  # Convert Zulu to my team TZ
        datetime.strptime(
            data["next_game"].game_date_time_utc,
            "%Y-%m-%dT%H:%M:%SZ",
        ),
        team_timezone,
    )
    game_local_datetime = convert_timezone(  # Convert Zulu to local
        datetime.strptime(
            data["next_game"].game_date_time_utc,
            "%Y-%m-%dT%H:%M:%SZ",
        ),
        "local",
    )
    formatted_date_time = game_datetime.strftime(settings.get("Off Day Thread", {}).get("NEXT_GAME_DATE_FORMAT","%A, %B %d, %I:%M %p %Z"))
    days_til_next_game = (game_local_datetime - tzlocal.get_localzone().localize(data["today"]["obj"])).days
%>
${'##'} Next ${data["myTeam"].team_info.team_name} Game
${formatted_date_time} \
${f"@ [{data['next_game'].home_team.team_city} {data['next_game'].home_team.team_name}]({data['teamSubsById'][data['next_game'].home_team.team_id]})" if data['next_game'].away_team.team_id == data["myTeam"].team_info.team_id else f"vs. [{data['next_game'].away_team.team_city} {data['next_game'].away_team.team_name}]({data['teamSubsById'][data['next_game'].away_team.team_id]})"} \
% if days_til_next_game > 0:
(${days_til_next_game} day${'s' if days_til_next_game > 1 else ''})
% endif
