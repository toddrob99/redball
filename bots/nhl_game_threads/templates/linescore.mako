<%
    awayTeam = (
        data["myTeam"] if data["homeAway"] == "away"
        else data["oppTeam"]
    )
    homeTeam = (
        data["myTeam"] if data["homeAway"] == "home"
        else data["oppTeam"]
    )
    if (
        data["game"]["liveData"]["linescore"]["teams"]["away"].get("goals") is not None
        and data["game"]["liveData"]["linescore"]["teams"]["home"].get("goals") is not None
    ):
        headerLine = "||"
        alignmentLine = "|:--|"
        awayLine = f'|[{awayTeam["teamName"]}]({data["teamSubs"][awayTeam["abbreviation"]]})|'
        homeLine = f'|[{homeTeam["teamName"]}]({data["teamSubs"][homeTeam["abbreviation"]]})|'
        for period in data["game"]["liveData"]["linescore"]["periods"]:
            headerLine += f'{period["ordinalNum"]}|'
            alignmentLine += ":--|"
            awayLine += f'{period["away"]["goals"]}|'
            homeLine += f'{period["home"]["goals"]}|'
        if data["game"]["liveData"]["linescore"]["hasShootout"]:
            headerLine += "SO|"
            alignmentLine += ":--|"
            awayLine += f"{data['game']['liveData']['linescore']['shootoutInfo']['away']['scores']}/{data['game']['liveData']['linescore']['shootoutInfo']['away']['attempts']}|"
            homeLine += f"{data['game']['liveData']['linescore']['shootoutInfo']['home']['scores']}/{data['game']['liveData']['linescore']['shootoutInfo']['home']['attempts']}|"
        headerLine += "|TOTAL|"
        alignmentLine += ":--|:--|"
        awayLine += f'|{data["game"]["liveData"]["linescore"]["teams"]["away"]["goals"]}|'
        homeLine += f'|{data["game"]["liveData"]["linescore"]["teams"]["home"]["goals"]}|'
%>\
${'##'} Linescore
${headerLine}
${alignmentLine}
${awayLine}
${homeLine}