<%
    prefix = settings.get("Game Thread", {}).get("TITLE_PREFIX","Game Thread:")
    home_team_record = f" ({data['game']['summary'].box_score_summary.home_team.team_wins}-{data['game']['summary'].box_score_summary.home_team.team_losses})"
    away_team_record = f" ({data['game']['summary'].box_score_summary.away_team.team_wins}-{data['game']['summary'].box_score_summary.away_team.team_losses})"
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
## Visiting Team
${data["game"]["summary"].box_score_summary.away_team.team_city} ${data["game"]["summary"].box_score_summary.away_team.team_name}${away_team_record} \
@ \
## Home Team
${data["game"]["summary"].box_score_summary.home_team.team_city} ${data["game"]["summary"].box_score_summary.home_team.team_name}${home_team_record}\
## Date/Time
${(" - " + data["gameTime"]["myTeam"].strftime(settings.get("Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))) if settings.get("Game Thread", {}).get("TITLE_DATE_FORMAT") != "" else ""}