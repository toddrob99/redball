<%
    away_inactives = data["game"]["summary"].box_score_summary.away_team.inactives
    home_inactives = data["game"]["summary"].box_score_summary.home_team.inactives
    def playerLink(p):
        return f"[{p.first_name} {p.family_name}](https://www.nba.com/player/{p.person_id})"
%>
% if len(away_inactives) or len(home_inactives):
${'##'} Inactives
|${data["game"]["summary"].box_score_summary.away_team.team_name}|${data["game"]["summary"].box_score_summary.home_team.team_name}|
|:--|:--|
%   for i in range(0, max(len(away_inactives), len(home_inactives))):
|${playerLink(away_inactives[i]) if len(away_inactives)>i else ""}|\
${playerLink(home_inactives[i]) if len(home_inactives)>i else ""}|
%   endfor
% endif
