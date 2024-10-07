<%
    import re

    if not data["game"]["live"]:
        return
    a = data["game"]["summary"].box_score_summary.away_team
    h = data["game"]["summary"].box_score_summary.home_team
    abt = data["game"]["live"].game.away_team
    hbt = data["game"]["live"].game.home_team
    abts = abt.statistics
    hbts = hbt.statistics
    def round_and_truncate(num):
        return str(round(num * 100, 1)).replace(".0", "")
    def playerLink(p):
        return f"[{p.first_name} {p.family_name}](https://www.nba.com/player/{p.person_id})"
%>\
% if abts or hbts or len(abt.players) or len(hbt.players):
${'##'} Game Stats
% endif
% if abts or hbts:
|Team|PTS|FG|3P|FT|REB (O+D)|AST|PF|STL|TO|BLK|
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
%   if abts:
|[${a.team_name}](${data["teamSubs"].get(a.team_tricode, "")})${" ^BONUS" if a.in_bonus == '1' else ""}|\
${abts.points}|${abts.field_goals_made}/${abts.field_goals_attempted} (${round(abts.field_goals_percentage * 100, 1)}%)|\
${abts.three_pointers_made}/${abts.three_pointers_attempted} (${round(abts.three_pointers_percentage * 100, 1)}%)|\
${abts.free_throws_made}/${abts.free_throws_attempted} (${round(abts.free_throws_percentage * 100, 1)}%)|\
${abts.rebounds_offensive}+${abts.rebounds_defensive}|\
${abts.assists}|${abts.fouls_personal}|${abts.steals}|${abts.turnovers}|${abts.blocks}|
%   endif
%   if hbts is not None:
|[${h.team_name}](${data["teamSubs"].get(h.team_tricode, "")})${" ^BONUS" if a.in_bonus == '1' else ""}|\
${hbts.points}|${hbts.field_goals_made}/${hbts.field_goals_attempted} (${round_and_truncate(hbts.field_goals_percentage)}%)|\
${hbts.three_pointers_made}/${hbts.three_pointers_attempted} (${round_and_truncate(hbts.three_pointers_percentage)}%)|\
${hbts.free_throws_made}/${hbts.free_throws_attempted} (${round_and_truncate(hbts.free_throws_percentage)}%)|\
${hbts.rebounds_offensive}+${hbts.rebounds_defensive}|\
${hbts.assists}|${hbts.fouls_personal}|${hbts.steals}|${hbts.turnovers}|${hbts.blocks}|
%   endif
% endif

<%
    abtp = [p for p in abt.players if p.played == '1']
    hbtp = [p for p in hbt.players if p.played == '1']
%>\
% for info in ({"t": a, "btp": abtp, "sl": f"[{a.team_name}]({data['teamSubs'].get(a.team_tricode, '')})"}, {"t": h, "btp": hbtp, "sl": f"[{h.team_name}]({data['teamSubs'].get(h.team_tricode, '')})"}):
%   if len(info["btp"]):
|${info["sl"]}|MIN|PTS|FG|3P|FT|REB (O+D)|AST|STL|BLK|TO|PF|+/-|
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
%      for p in info["btp"]:
<%
    pattern = r"PT(\d+)M(\d+).\d+S"
    reformatted = ":".join(re.match(pattern, p.statistics.minutes).groups())
    p_minutes = reformatted if bool(re.match(r"\d+:\d+", reformatted)) else p.minutes
%>\
|${f"^{p.position} " if hasattr(p, "position") else ""}${playerLink(p)}|${p_minutes}|${p.statistics.points}|\
${p.statistics.field_goals_made}/${p.statistics.field_goals_attempted} (${round_and_truncate(p.statistics.field_goals_percentage)}%)|\
${p.statistics.three_pointers_made}/${p.statistics.three_pointers_attempted} (${round_and_truncate(p.statistics.three_pointers_percentage)}%)|\
${p.statistics.free_throws_made}/${p.statistics.free_throws_attempted} (${round_and_truncate(p.statistics.free_throws_percentage)}%)|\
${p.statistics.rebounds_offensive}+${p.statistics.rebounds_defensive}|\
${p.statistics.assists}|${p.statistics.steals}|${p.statistics.blocks}|${p.statistics.turnovers}|\
${p.statistics.fouls_personal}|${p.statistics.plus_minus_points}|
%       endfor
%   endif

% endfor