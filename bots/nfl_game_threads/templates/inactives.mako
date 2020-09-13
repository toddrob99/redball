<%
    rosterStatusKey = {
        "ACT": "Active",
        "DEV": "Development Squad",
        "CUT": "Cut",
        "RES": "Reserved",
        "SUS": "Suspended",
        "RSN": "Reserved/Non-Football Injury",
        "TRD": "Traded to another division",
        "TRT": "Traded from Team",
        "TRC": "Traded to Another Conference",
        "EXE": "Exempt",
        "NWT": "Not With Team",
        "PUP": "Physically Unable to Perform",
        "UDF": "Unsigned Draft Pick",
        "RFA": "Restricted Free Agent",
        "UFA": "Unrestricted Free Agent",
        "NON": "Non Football Related Injured Reserve",
        "RET": "Retired",
    }
    excludeRosterStatus = ["ACT", "DEV", "CUT", "TRD", "TRT", "TRC", "UDF", "RFA", "UFA", "RET"]
    myInactives = [x for x in data["myTeam"]["roster"]["data"] if x["activeRole"] == "PLAYER" and x["player"]["rosterStatus"] not in excludeRosterStatus]
    oppInactives = [x for x in data["oppTeam"]["roster"]["data"] if x["activeRole"] == "PLAYER" and x["player"]["rosterStatus"] not in excludeRosterStatus]
    injuryStatusKey = {
        "--": "In",
    }
%>\
% if len(myInactives) or len(data["myTeam"]["injuries"]["data"]):
% if len(myInactives) and len(data["myTeam"]["injuries"]["data"]):
${'##'} ${data["myTeam"]["nickName"]} Inactives & Injury Status
% elif len(myInactives):
${'##'} ${data["myTeam"]["nickName"]} Inactives
% elif len(data["myTeam"]["injuries"]["data"]):
${'##'} ${data["myTeam"]["nickName"]} Injury Status
% endif
% if len(myInactives):
% for x in set(x["player"]["rosterStatus"] for x in myInactives):
* ${f"{rosterStatusKey[x]}: {', '.join([p['player']['position']['abbr'] + ' ' + p['displayName'] for p in myInactives if p['player']['rosterStatus'] == x])}"}
% endfor
% endif
% if len(data["myTeam"]["injuries"]["data"]):
% for x in set(x["injuryStatus"] for x in data["myTeam"]["injuries"]["data"]):
* ${f"{injuryStatusKey.get(x, x)}: {', '.join([p['person']['player']['position']['abbr'] + ' ' + p['person']['displayName'] for p in data['myTeam']['injuries']['data'] if p['injuryStatus'] == x])}"}
% endfor
% endif
% endif

% if len(oppInactives) or len(data["oppTeam"]["injuries"]["data"]):
% if len(oppInactives) and len(data["oppTeam"]["injuries"]["data"]):
${'##'} ${data["oppTeam"]["nickName"]} Inactives & Injury Status
% elif len(oppInactives):
${'##'} ${data["oppTeam"]["nickName"]} Inactives
% elif len(data["oppTeam"]["injuries"]["data"]):
${'##'} ${data["oppTeam"]["nickName"]} Injury Status
% endif
% if len(oppInactives):
% for x in set(x["player"]["rosterStatus"] for x in oppInactives):
* ${f"{rosterStatusKey[x]}: {', '.join([p['player']['position']['abbr'] + ' ' + p['displayName'] for p in oppInactives if p['player']['rosterStatus'] == x])}"}
% endfor
% endif
% if len(data["oppTeam"]["injuries"]["data"]):
% for x in set(x["injuryStatus"] for x in data["oppTeam"]["injuries"]["data"]):
* ${f"{injuryStatusKey.get(x, x)}: {', '.join([p['person']['player']['position']['abbr'] + ' ' + p['person']['displayName'] for p in data['oppTeam']['injuries']['data']  if p['injuryStatus'] == x])}"}
% endfor
% endif
% endif