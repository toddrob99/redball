<%
    awayTeam = data["myTeam"] if data["homeAway"] == "away" else data["oppTeam"]
    homeTeam = data["myTeam"] if data["homeAway"] == "home" else data["oppTeam"]
    def playerLink(p):
        return f"[{p['fullName']}](https://www.nhl.com/player/{p['id']})"
%>\
${'##'} Decisions
%if data["game"]["liveData"]["decisions"].get("winner", {}).get("fullName"):
* Winner: ${playerLink(data["game"]["liveData"]["decisions"]["winner"])}
%endif
%if data["game"]["liveData"]["decisions"].get("loser", {}).get("fullName"):
* Loser: ${playerLink(data["game"]["liveData"]["decisions"]["loser"])}
%endif
%if data["game"]["liveData"]["decisions"].get("firstStar", {}).get("fullName"):
* First Star: ${playerLink(data["game"]["liveData"]["decisions"]["firstStar"])}
%endif
%if data["game"]["liveData"]["decisions"].get("secondStar", {}).get("fullName"):
* Second Star: ${playerLink(data["game"]["liveData"]["decisions"]["secondStar"])}
%endif
%if data["game"]["liveData"]["decisions"].get("thirdStar", {}).get("fullName"):
* Third Star: ${playerLink(data["game"]["liveData"]["decisions"]["thirdStar"])}
%endif
