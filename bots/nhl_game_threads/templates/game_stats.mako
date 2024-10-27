<%
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    #awayStats = data["game_boxscore"].get("awayTeam")
    #homeStats = data["game_boxscore"].get("homeTeam")
    stats = {
        x.get("category", "foo"): (x.get("awayValue", "-"), x.get("homeValue", "-")) for x in data["game_right_rail"].get("teamGameStats", [])
    }
    placeholder = ("-", "-")
%>\
${'##'} Game Stats
||SOG|FO%|PP|PIM|Hits|Blks|GA|TA|
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
## Team
|[${awayTeam["commonName"]["default"]}](${data["teamSubs"][awayTeam["abbrev"]]})|\
${stats.get("sog", placeholder)[0]}|\
${(str(round(stats.get("faceoffWinningPctg", placeholder)[0] * 100)) + "%") if stats.get("faceoffWinningPctg") else "-"}|\
${stats.get("powerPlay", placeholder)[0]}|\
${stats.get("pim", placeholder)[0]}|\
${stats.get("hits", placeholder)[0]}|\
${stats.get("blockedShots", placeholder)[0]}|\
${stats.get("giveaways", placeholder)[0]}|\
${stats.get("takeaways", placeholder)[0]}|
|[${homeTeam["commonName"]["default"]}](${data["teamSubs"][homeTeam["abbrev"]]})|\
${stats.get("sog", placeholder)[1]}|\
${(str(round(stats.get("faceoffWinningPctg", placeholder)[1] * 100)) + "%") if stats.get("faceoffWinningPctg") else "-"}|\
${stats.get("powerPlay", placeholder)[1]}|\
${stats.get("pim", placeholder)[1]}|\
${stats.get("hits", placeholder)[1]}|\
${stats.get("blockedShots", placeholder)[1]}|\
${stats.get("giveaways", placeholder)[1]}|\
${stats.get("takeaways", placeholder)[1]}|

<%
    awayF = data["game_boxscore"].get("playerByGameStats", {}).get("awayTeam", {}).get("forwards", [])
    awayL = [x for x in awayF if x["position"] == "L"]
    awayC = [x for x in awayF if x["position"] == "C"]
    awayR = [x for x in awayF if x["position"] == "R"]
    awayD = data["game_boxscore"].get("playerByGameStats", {}).get("awayTeam", {}).get("defense", [])
    awayG = data["game_boxscore"].get("playerByGameStats", {}).get("awayTeam", {}).get("goalies", [])
    awaySkaters = awayF + awayD
    awayOnIce_dict = data["game_pbp"].get("awayTeam", {}).get("onIce", [])
    awayOnIce = [x.get("playerId") for x in awayOnIce_dict]
    awaySkatersOnIce = [x for x in awaySkaters if x["playerId"] in awayOnIce]
    awaySkatersOnBench = [x for x in awaySkaters if x["playerId"] not in awayOnIce]
    homeF = data["game_boxscore"].get("playerByGameStats", {}).get("homeTeam", {}).get("forwards", [])
    homeL = [x for x in homeF if x["position"] == "L"]
    homeC = [x for x in homeF if x["position"] == "C"]
    homeR = [x for x in homeF if x["position"] == "R"]
    homeD = data["game_boxscore"].get("playerByGameStats", {}).get("homeTeam", {}).get("defense", [])
    homeG = data["game_boxscore"].get("playerByGameStats", {}).get("homeTeam", {}).get("goalies", [])
    homeSkaters = homeF + homeD
    homeOnIce_dict = data["game_pbp"].get("homeTeam", {}).get("onIce", [])
    homeOnIce = [x.get("playerId") for x in homeOnIce_dict]
    homeSkatersOnIce = [x for x in homeSkaters if x["playerId"] in homeOnIce]
    homeSkatersOnBench = [x for x in homeSkaters if x["playerId"] not in homeOnIce]
    def playerLink(p):
        return f"[{p['name']['default']}](https://www.nhl.com/player/{p['playerId']})"
    if not (awaySkaters or awayG or homeSkaters or homeG):
        return
%>\
\
% for info in [(awayTeam, awaySkatersOnIce, awaySkatersOnBench, awayG, awayOnIce), (homeTeam, homeSkatersOnIce, homeSkatersOnBench, homeG, homeOnIce)]:
%   if len(info[1]) or len(info[2]):
|[${info[0]["commonName"]["default"]}](${data["teamSubs"][info[0]["abbrev"]]}) Skaters|G|A|+/-|S|Blk|PIM|FO%|TOI|
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
%       for p in info[1] + info[2]:
|^${p['position']} ${'**' if p in info[1] else ''}${playerLink(p)}${'**' if p in info[1] else ''}|\
${p.get("goals", "-")}|\
${p.get("assists", "-")}|\
${p.get("plusMinus", "-")}|\
${p.get("sog", "-")}|\
${p.get("blockedShots", "-")}|\
${p.get("pim", "-")}|\
${(str(round(p.get("faceoffWinningPctg", 0.0) * 100)) + "%") if p.get("faceoffWinningPctg") else "-"}|\
${p.get("toi", "-")}|
%       endfor
%   endif

%   if len(info[3]):
|[${info[0]["commonName"]["default"]}](${data["teamSubs"][info[0]["abbrev"]]}) Goalies|Saves/Shots|Save %|TOI|
|:--|:-:|:-:|:-:|
%       for g in info[3]:
|${'**' if g["playerId"] in info[4] else ''}${playerLink(g)}${'**' if g["playerId"] in info[4] else ''}|\
${g.get("saveShotsAgainst", "-") if g.get("toi", "00:00") != "00:00" else "-"}|\
${f'{float(g["savePctg"])*100:.1f}%' if g.get("savePctg") is not None and g.get("toi", "00:00") != "00:00" else "-"}|\
${g.get("toi", "-")}|
%       endfor
%   endif

% endfor
