<%
    from datetime import datetime
    team_timezone = settings.get("Bot", {}).get("TEAM_TIMEZONE", "America/New_York")
    prior_meetings = data["game"]["summary"].box_score_summary.last_five_meetings.meetings
    if not len(prior_meetings):
        return
%>\
${'##'} Matchup History
|Date|Location|Result|
|:--|:--|:--|:--|:--|
%for m in prior_meetings:
<%
    w = m.away_team if m.away_team.score > m.home_team.score else m.home_team
    l = m.away_team if w == m.home_team else m.home_team
    r = "Win" if w.team_id == data["myTeam"].team_info.team_id else "Loss"
    d = convert_timezone(  # Convert Zulu to my team TZ
        datetime.strptime(
            m.game_time_utc,
            "%Y-%m-%dT%H:%M:%SZ",
        ),
        team_timezone,
    )
%>\
|${d.strftime("%m/%d/%Y")}|${m.home_team.team_city}|${r} ${w.score}-${l.score}|
%endfor
