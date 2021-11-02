<%
    if data["game"]["live"] and hasattr(data["game"]["live"], "game"):
        away_score = data["game"]["live"].game.away_team.score
        home_score = data["game"]["live"].game.home_team.score
    else:
        away_score = data["game"]["summary"].box_score_summary.away_team.score
        home_score = data["game"]["summary"].box_score_summary.home_team.score
    away_team = data["game"]["summary"].box_score_summary.away_team
    home_team = data["game"]["summary"].box_score_summary.home_team
    result = (
        "tie" if away_score == home_score
        else "win" if (
            data["homeAway"] == "home" and home_score > away_score
            or data["homeAway"] == "away" and away_score > home_score
        )
        else "loss" if (
            data["homeAway"] == "home" and home_score < away_score
            or data["homeAway"] == "away" and away_score < home_score
        )
        else ""
    )
    home_team_record = f" ({data['game']['summary'].box_score_summary.home_team.team_wins}-{data['game']['summary'].box_score_summary.home_team.team_losses})"
    away_team_record = f" ({data['game']['summary'].box_score_summary.away_team.team_wins}-{data['game']['summary'].box_score_summary.away_team.team_losses})"
%>\
## Visiting Team
${'##'} [${away_team.team_city} ${away_team.team_name}](${data["teamSubs"].get(away_team.team_tricode, "")})${away_team_record} \
@ \
## Home Team
[${data["game"]["summary"].box_score_summary.home_team.team_city} ${data["game"]["summary"].box_score_summary.home_team.team_name}](${data["teamSubs"].get(data["game"]["summary"].box_score_summary.home_team.team_tricode, "")})${home_team_record}

<%include file="game_info.mako" />

${'##'} Game Status - ${data["gameStatusText"]}: \
%   if result == "tie":
TIE @ \
%   elif result == "win":
${data["myTeam"].team_info.team_name} Win \
%   elif result == "loss":
${data["oppTeam"].team_info.team_name} Win \
%   endif
${max(int(away_score), int(home_score))}-${min(int(away_score), int(home_score))}

<%include file="linescore.mako" />

<%include file="inactives.mako" />

<%include file="boxscore.mako" />

<%include file="standings.mako" />

<%include file="division_scoreboard.mako" />

## Configurable footer text
${settings.get('Post Game Thread',{}).get('FOOTER','')}