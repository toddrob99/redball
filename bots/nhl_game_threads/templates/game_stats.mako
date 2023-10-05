<%
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    awayStats = data["game_boxscore"].get("awayTeam")
    homeStats = data["game_boxscore"].get("homeTeam")
%>\
${'##'} Game Stats
||SOG|FO%|PP|PIM|Hits|Blks|
|:--|:--|:--|:--|:--|:--|:--|
## Team
|[${awayTeam["commonName"]}](${data["teamSubs"][awayTeam["abbrev"]]})|${awayStats.get("sog", "-")}|${round(float(awayStats.get("faceoffWinningPctg", 0)))}%|\
${awayStats.get("powerPlayConversion", "-")}|\
${awayStats.get("pim", "-")}|${awayStats.get("hits", "-")}|${awayStats.get("blocks", "-")}|
|[${homeTeam["commonName"]}](${data["teamSubs"][homeTeam["abbrev"]]})|${homeStats.get("sog", "-")}|${round(float(homeStats.get("faceoffWinningPctg", 0)))}%|\
${homeStats.get("powerPlayConversion", "-")}|\
${homeStats.get("pim", "-")}|${homeStats.get("hits", "-")}|${homeStats.get("blocks", "-")}|

<%
    awayF = data["game_boxscore"].get("boxscore", {}).get("playerByGameStats", {}).get("awayTeam", {}).get("forwards", [])
    awayL = [x for x in awayF if x["position"] == "L"]
    awayC = [x for x in awayF if x["position"] == "C"]
    awayR = [x for x in awayF if x["position"] == "R"]
    awayD = data["game_boxscore"].get("boxscore", {}).get("playerByGameStats", {}).get("awayTeam", {}).get("defense", [])
    awayG = data["game_boxscore"].get("boxscore", {}).get("playerByGameStats", {}).get("awayTeam", {}).get("goalies", [])
    awaySkaters = awayF + awayD
    awayOnIce = data["game_pbp"].get("awayTeam", {}).get("onIce", [])
    awaySkatersOnIce = [x for x in awaySkaters if x["playerId"] in awayOnIce]
    awaySkatersOnBench = [x for x in awaySkaters if x["playerId"] not in awayOnIce]
    homeF = data["game_boxscore"].get("boxscore", {}).get("playerByGameStats", {}).get("homeTeam", {}).get("forwards", [])
    homeL = [x for x in homeF if x["position"] == "L"]
    homeC = [x for x in homeF if x["position"] == "C"]
    homeR = [x for x in homeF if x["position"] == "R"]
    homeD = data["game_boxscore"].get("boxscore", {}).get("playerByGameStats", {}).get("homeTeam", {}).get("defense", [])
    homeG = data["game_boxscore"].get("boxscore", {}).get("playerByGameStats", {}).get("homeTeam", {}).get("goalies", [])
    homeSkaters = homeF + homeD
    homeOnIce = data["game_pbp"].get("homeTeam", {}).get("onIce", [])
    homeSkatersOnIce = [x for x in homeSkaters if x["playerId"] in homeOnIce]
    homeSkatersOnBench = [x for x in homeSkaters if x["playerId"] not in homeOnIce]
    def playerLink(p):
        return f"[{p['name']}](https://www.nhl.com/player/{p['playerId']})"
    if not (awaySkaters or awayG or homeSkaters or homeG):
        return
%>\
\
% for info in [(awayTeam, awaySkatersOnIce, awaySkatersOnBench, awayG, awayOnIce), (homeTeam, homeSkatersOnIce, homeSkatersOnBench, homeG, homeOnIce)]:
%   if len(info[1]) or len(info[2]):
|[${info[0]["commonName"]}](${data["teamSubs"][info[0]["abbrev"]]}) Skaters|G|A|+/-|S|Blk|PIM|FO|TOI|
|:--|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
%       for p in info[1] + info[2]:
|^${p['position']} ${'**' if p in info[1] else ''}${playerLink(p)}${'**' if p in info[1] else ''}|\
${p["goals"]}|\
${p["assists"]}|\
${p["plusMinus"]}|\
${p["shots"]}|\
${p["blockedShots"]}|\
${p["pim"]}|\
${p["faceoffs"]}|\
${p["toi"]}|
%       endfor
%   endif

%   if len(info[3]):
|[${info[0]["commonName"]}](${data["teamSubs"][info[0]["abbrev"]]}) Goalies|Saves/Shots|Save %|TOI|
|:--|:-:|:-:|:-:|
%       for g in info[3]:
|${'**' if g["playerId"] in info[4] else ''}${playerLink(g)}${'**' if g["playerId"] in info[4] else ''}|\
${g.get("saveShotsAgainst", "-")}|\
${f'{float(g["savePctg"])*100:.1f}%' if g.get("savePctg") is not None else "-"}|\
${g["toi"]}|
%       endfor
%   endif

% endfor
