<%
    excludeRosterStatus = []
    includeRosterStatus = ["NOT_ACTIVE"]
    myTeamHomeVisitor = "homeLiveGameRoster" if data["homeAway"] == "home" else "visitorLiveGameRoster"
    oppTeamHomeVisitor = "homeLiveGameRoster" if data["homeAway"] == "away" else "visitorLiveGameRoster"
    myInactives = [x for x in data["gameDetails"].get(myTeamHomeVisitor, []) if x["status"] not in excludeRosterStatus and x["status"] in includeRosterStatus]
    oppInactives = [x for x in data["gameDetails"].get(oppTeamHomeVisitor, []) if x["status"] not in excludeRosterStatus and x["status"] in includeRosterStatus]
    nl = "\n"
%>\
% if len(myInactives):
${'##'} ${data["myTeam"]["nickName"]} Inactives
* ${f"{(nl+'* ').join([p['position'] + ' ' + p['firstName'] + ' ' + p['lastName'] for p in myInactives])}"}

% endif
% if len(oppInactives):
${'##'} ${data["oppTeam"]["nickName"]} Inactives
* ${f"{(nl + '* ').join([p['position'] + ' ' + p['firstName'] + ' ' + p['lastName'] for p in oppInactives])}"}

% endif