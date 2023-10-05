<%
    from datetime import datetime
    import pytz
    def subLink(t):
        return f"[{t['name']}]({data['teamSubs'].get(t['abbrev'], '')})"
    ordDict = {1:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},2:{1:'1st',2:'2nd',3:'3rd',4:'OT',5:'SO'},3:{1:'1st',2:'2nd',3:'3rd',4:'OT1',5:'OT2',6:'OT3',7:'OT4',8:'OT5'}}
    def format_period(game):
        return ordDict[game["gameType"]].get(game.get("period"), "")
%>\
% if len(data["todayOtherDivisionGames"]):
${'##'} ${data["myTeam"]["divisionName"]} Division Scoreboard
% for game in data["todayOtherDivisionGames"]:
<%
    dt = datetime.strptime(game["startTimeUTC"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
    toTz = pytz.timezone(settings.get("Bot", {}).get("TEAM_TIMEZONE", "America/New_York"))
    formattedGameTime = dt.astimezone(toTz).strftime("%I:%M %p")
    #formattedPeriod = "" if game["gameState"] == "FUT" else game["period"] if game.get("period") and game["period"] <= 3 else (game.get("periodDescriptor", {}).get("otPeriods", "") + "OT") if game.get("periodDescriptor", {}).get("periodType") == "OT" else "SO" if game.get("periodDescriptor", {}).get("periodType") == "SO" else game["period"]
%>\
% if data["game"].get("gameScheduleState") in ["PPD", "SUSP", "CNCL"]:
${subLink(game["awayTeam"])} @ ${subLink(game["homeTeam"])} - ${data["game"].get("gameScheduleState")}
% elif game["gameState"] in ["FINAL", "OFF", "OVER"]:
${subLink(game["awayTeam"])} @ ${subLink(game["homeTeam"])} - Final
% elif game["gameState"] in ["LIVE", "CRIT"]:
${subLink(game["awayTeam"])} @ ${subLink(game["homeTeam"])} - ${format_period(game)} ${game.get("clock", {}).get("timeRemaining", "")}
% else:
${subLink(game["awayTeam"])} @ ${subLink(game["homeTeam"])} - ${formattedGameTime}
% endif

% endfor
% endif