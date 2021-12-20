<%
    if data["game"]["live"] and hasattr(data["game"]["live"], "game"):
        away_score = data["game"]["live"].game.away_team.score
        home_score = data["game"]["live"].game.home_team.score
    else:
        away_score = data["game"]["summary"].box_score_summary.away_team.score
        home_score = data["game"]["summary"].box_score_summary.home_team.score
    away_team = data["game"]["summary"].box_score_summary.away_team
    home_team = data["game"]["summary"].box_score_summary.home_team
    if data["gameStatus"] >= 3:
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
    else:
        result = None
    home_team_record = f" ({data['game']['summary'].box_score_summary.home_team.team_wins}-{data['game']['summary'].box_score_summary.home_team.team_losses})"
    away_team_record = f" ({data['game']['summary'].box_score_summary.away_team.team_wins}-{data['game']['summary'].box_score_summary.away_team.team_losses})"
    per_desc = {
        1: "1st Qtr",
        2: "2nd Qtr",
        3: "3rd Qtr",
        4: "4th Qtr",
        5: "OT",
        6: "2nd OT",
        7: "3rd OT",
        8: "4th OT",
        9: "5th OT",
        10: "6th OT",
        11: "7th OT",
        12: "8th OT",
        13: "9th OT",
        14: "10th OT",
    }
%>\
## Visiting Team
${'##'} [${away_team.team_city} ${away_team.team_name}](${data["teamSubs"].get(away_team.team_tricode, "")})${away_team_record} \
@ \
## Home Team
[${data["game"]["summary"].box_score_summary.home_team.team_city} ${data["game"]["summary"].box_score_summary.home_team.team_name}](${data["teamSubs"].get(data["game"]["summary"].box_score_summary.home_team.team_tricode, "")})${home_team_record}

<%include file="game_info.mako" />

%if data["gameStatus"] == 2:
${'##'} Game Status: \
%   if data["game"]["live"]:
${data["gameStatusText"]}
%   else:
${per_desc[data["game"]["summary"].box_score_summary.period]}
%   endif

%elif result:
${'##'} Game Status: ${data["gameStatusText"]}: \
%   if result == "tie":
TIE @ \
%   elif result == "win":
${data["myTeam"].team_info.team_name} Win \
%   elif result == "loss":
${data["oppTeam"].team_info.team_name} Win \
%   endif
${max(int(away_score), int(home_score))}-${min(int(away_score), int(home_score))}
%elif "PPD" in data["gameStatusText"]:
${'##'} Game Status: ${data["gameStatusText"]}
%endif

%if data["gameStatus"] == 1:
<%include file="matchup_history.mako" />

<%include file="inactives.mako" />

<%include file="boxscore.mako" />

<%include file="pregame_charts.mako" />

%   if settings.get("Game Thread", {}).get("STANDINGS_TYPE","Conference") == "Division":
<%include file="division_standings.mako" args="num_to_show=settings.get('Game Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
%   elif settings.get("Game Thread", {}).get("STANDINGS_TYPE","Conference") == "Conference":
<%include file="conference_standings.mako" args="num_to_show=settings.get('Game Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
%   elif settings.get("Game Thread", {}).get("STANDINGS_TYPE","Conference") == "League":
<%include file="league_standings.mako" args="num_to_show=settings.get('Game Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
%   endif

%else:
<%include file="linescore.mako" />

<%include file="inactives.mako" />

<%include file="boxscore.mako" />

%endif

% if settings.get("Game Thread", {}).get("SCOREBOARD_TYPE","Conference") == "Division":
<%include file="division_scoreboard.mako" />
% elif settings.get("Game Thread", {}).get("SCOREBOARD_TYPE","Conference") == "Conference":
<%include file="conference_scoreboard.mako" />
% elif settings.get("Game Thread", {}).get("SCOREBOARD_TYPE","Conference") == "League":
<%include file="league_scoreboard.mako" />
% endif

## Configurable footer text
${settings.get('Game Thread',{}).get('FOOTER','')}