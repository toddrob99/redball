<%
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

% if settings.get("Tailgate Thread", {}).get("STANDINGS_TYPE","Conference") == "Division":
<%include file="division_standings.mako" args="num_to_show=settings.get('Tailgate Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
% elif settings.get("Tailgate Thread", {}).get("STANDINGS_TYPE","Conference") == "Conference":
<%include file="conference_standings.mako" args="num_to_show=settings.get('Tailgate Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
% elif settings.get("Tailgate Thread", {}).get("STANDINGS_TYPE","Conference") == "League":
<%include file="league_standings.mako" args="num_to_show=settings.get('Tailgate Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
% endif

% if settings.get("Tailgate Thread", {}).get("SCOREBOARD_TYPE","Conference") == "Division":
<%include file="division_scoreboard.mako" />
% elif settings.get("Tailgate Thread", {}).get("SCOREBOARD_TYPE","Conference") == "Conference":
<%include file="conference_scoreboard.mako" />
% elif settings.get("Tailgate Thread", {}).get("SCOREBOARD_TYPE","Conference") == "League":
<%include file="league_scoreboard.mako" />
% endif

## Configurable footer text
${settings.get('Tailgate Thread',{}).get('FOOTER','')}