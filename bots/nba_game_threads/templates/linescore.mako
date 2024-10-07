<%
    a = data["game"]["summary"].box_score_summary.away_team
    h = data["game"]["summary"].box_score_summary.home_team
    headerLine = "||"
    alignmentLine = "|:--|"
    awayLine = f'|[{a.team_name}]({data["teamSubs"].get(a.team_tricode, "")})|'
    homeLine = f'|[{h.team_name}]({data["teamSubs"].get(h.team_tricode, "")})|'
    for i in range(0, len(a.periods)):
        a_p = a.periods[i]
        h_p = h.periods[i]
        headerLine += f'{a_p.period}|'
        alignmentLine += ":--|"
        awayLine += f'{a_p.score}|'
        homeLine += f'{h_p.score}|'
    headerLine += "|TOTAL|"
    alignmentLine += ":--|:--|"
    awayLine += f'|{a.score}|'
    homeLine += f'|{h.score}|'
%>\
${'##'} Linescore
${headerLine}
${alignmentLine}
${awayLine}
${homeLine}