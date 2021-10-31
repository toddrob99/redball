<%
    prefix = settings.get("Tailgate Thread", {}).get("TITLE_PREFIX","Tailgate Thread:")
    home_team_record = f" ({data['game']['summary'].box_score_summary.home_team.team_wins}-{data['game']['summary'].box_score_summary.home_team.team_losses})"
    away_team_record = f" ({data['game']['summary'].box_score_summary.away_team.team_wins}-{data['game']['summary'].box_score_summary.away_team.team_losses})"
%>\
## Visiting Team
${'##'} [${data["game"]["summary"].box_score_summary.away_team.team_city} ${data["game"]["summary"].box_score_summary.away_team.team_name}](${data["teamSubs"].get(data["game"]["summary"].box_score_summary.away_team.team_tricode, "")})${away_team_record} \
@ \
## Home Team
[${data["game"]["summary"].box_score_summary.home_team.team_city} ${data["game"]["summary"].box_score_summary.home_team.team_name}](${data["teamSubs"].get(data["game"]["summary"].box_score_summary.home_team.team_tricode, "")})${home_team_record}

<%include file="game_info.mako" />

<%include file="matchup_history.mako" />

<%include file="inactives.mako" />

<%include file="pregame_charts.mako" />

<%include file="standings.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Tailgate Thread',{}).get('FOOTER','')}