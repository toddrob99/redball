<%
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    linescore = data["game_right_rail"].get("linescore", {}).get("byPeriod", [])
    ordDict = {1:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},2:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},3:{1:'1st',2:'2nd',3:'3rd',4:'OT1',5:'OT2',6:'OT3',7:'OT4',8:'OT5'}}
    periodOrd = ordDict[data["game"]["gameType"]]
    if linescore:
        headerLine = "||"
        alignmentLine = "|:--|"
        awayLine = f'|[{awayTeam["commonName"]["default"]}]({data["teamSubs"][awayTeam["abbrev"]]})|'
        homeLine = f'|[{homeTeam["commonName"]["default"]}]({data["teamSubs"][homeTeam["abbrev"]]})|'
        for period in linescore:
            headerLine += f'{periodOrd[period.get("period", period.get("periodDescriptor", {}).get("number"))]}|'
            alignmentLine += ":--|"
            awayLine += f'{period["away"]}|'
            homeLine += f'{period["home"]}|'
        headerLine += "|TOTAL|"
        alignmentLine += ":--|:--|"
        awayLine += f'|{data["game_right_rail"].get("linescore", {}).get("totals", {}).get("away")}|'
        homeLine += f'|{data["game_right_rail"].get("linescore", {}).get("totals", {}).get("home")}|'
%>\
% if linescore:
${'##'} Linescore
${headerLine}
${alignmentLine}
${awayLine}
${homeLine}
% endif