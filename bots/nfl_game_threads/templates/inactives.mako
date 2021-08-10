<%
    excludeRosterStatus = ["Active"]
    myInactives = [x for x in data["myTeamRoster"] if x["status"] not in excludeRosterStatus]
    oppInactives = [x for x in data["oppTeamRoster"] if x["status"] not in excludeRosterStatus]
%>\
% if len(myInactives):
${'##'} ${data["myTeam"]["nickName"]} Inactives
% for x in set(x["status"] for x in myInactives):
* ${f"{x['status']}: {', '.join([p['position'] + ' ' + p['displayName'] for p in myInactives if p['status'] == x])}"}
% else:
not len myInactives: ${myInactives}
% endfor

% endif
% if len(oppInactives):
${'##'} ${data["oppTeam"]["nickName"]} Inactives
% for x in set(x["status"] for x in oppInactives):
* ${f"{x['status']}: {', '.join([p['position'] + ' ' + p['displayName'] for p in oppInactives if p['status'] == x])}"}
% else:
not len oppInactives: ${oppInactives}
% endfor

% endif