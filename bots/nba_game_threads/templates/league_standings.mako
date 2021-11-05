<%page args="num_to_show=8" />
<%
    if not len(data["standings"].standings):
        return
    confs = sorted(list(set([x.conference for x in data["standings"].standings])))
    conf_labels = {
        "East": "Eastern",
        "West": "Western",
    }
%>\
% for conf in confs:
${'##'} ${conf_labels.get(conf, conf)} Conference Standings
|Rank|Team|W|L|Pct|GB|Conf|Home|Away|L10|Strk|
|:-:|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
${"\n".join([f"|{i+1}|\
[{x.teamcity} {x.teamname}]({data['teamSubsById'][x.teamid]})|\
{x.wins}|{x.losses}|{x.winpct}|{'-' if str(x.conferencegamesback) == '0.0' else x.conferencegamesback}|{x.conferencerecord.strip()}|{x.home.strip()}|{x.road.strip()}|{x.l10.strip()}|{x.strcurrentstreak.strip()}|" for i, x in enumerate([y for y in data["standings"].standings if y.conference == conf])][:num_to_show])}

% endfor
