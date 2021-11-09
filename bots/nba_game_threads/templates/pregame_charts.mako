<%
    away_sub_url = data["teamSubs"][data["game"]["summary"].box_score_summary.away_team.team_tricode]
    home_sub_url = data["teamSubs"][data["game"]["summary"].box_score_summary.home_team.team_tricode]
    a = data["game"]["summary"].box_score_summary.pregame_charts.away_team.statistics
    h = data["game"]["summary"].box_score_summary.pregame_charts.home_team.statistics
    def playerLink(f, l, i):
        return f"[{f} {l}](https://www.nba.com/player/{i})"
%>
${'##'} Season Stats
|Team|PTS|REB|AST|STL|BLK|TO|FG%|3P%|FT%|
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
|[${data["game"]["summary"].box_score_summary.away_team.team_name}](${away_sub_url})\
|${a.points}|${a.rebounds_total}|${a.assists}|${a.steals}|${a.blocks}|${a.turnovers}|${a.field_goals_percentage}|${a.three_pointers_percentage}|${a.free_throws_percentage}|
|[${data["game"]["summary"].box_score_summary.home_team.team_name}](${home_sub_url})\
|${h.points}|${h.rebounds_total}|${h.assists}|${h.steals}|${h.blocks}|${h.turnovers}|${h.field_goals_percentage}|${h.three_pointers_percentage}|${h.free_throws_percentage}|

${'##'} Team Leaders
||[${data["game"]["summary"].box_score_summary.away_team.team_name}](${away_sub_url})|[${data["game"]["summary"].box_score_summary.home_team.team_name}](${home_sub_url})|
|:--|--:|:--|
|PTS|${playerLink(a.player_pts_leader_first_name, a.player_pts_leader_family_name, a.player_pts_leader_id)} (${a.player_pts_leader_pts})|(${h.player_pts_leader_pts}) ${playerLink(h.player_pts_leader_first_name, h.player_pts_leader_family_name, h.player_pts_leader_id)}|
|REB|${playerLink(a.player_reb_leader_first_name, a.player_reb_leader_family_name, a.player_reb_leader_id)} (${a.player_reb_leader_reb})|(${h.player_reb_leader_reb}) ${playerLink(h.player_reb_leader_first_name, h.player_reb_leader_family_name, h.player_reb_leader_id)}|
|AST|${playerLink(a.player_ast_leader_first_name, a.player_ast_leader_family_name, a.player_ast_leader_id)} (${a.player_ast_leader_ast})|(${h.player_ast_leader_ast}) ${playerLink(h.player_ast_leader_first_name, h.player_ast_leader_family_name, h.player_ast_leader_id)}|
|BLK|${playerLink(a.player_blk_leader_first_name, a.player_blk_leader_family_name, a.player_blk_leader_id)} (${a.player_blk_leader_blk})|(${h.player_blk_leader_blk}) ${playerLink(h.player_blk_leader_first_name, h.player_blk_leader_family_name, h.player_blk_leader_id)}|
