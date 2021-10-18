<%
    awayTeam = data["myTeam"] if data["homeAway"] == "away" else data["oppTeam"]
    homeTeam = data["myTeam"] if data["homeAway"] == "home" else data["oppTeam"]
%>\
${'##'} Decisions
%if data["game"]["liveData"]["decisions"].get("winner"):
* Winner: ${data["game"]["liveData"]["decisions"]["winner"]["fullName"]}
%endif
%if data["game"]["liveData"]["decisions"].get("loser"):
* Loser: ${data["game"]["liveData"]["decisions"]["loser"]["fullName"]}
%endif
%if data["game"]["liveData"]["decisions"].get("firstStar"):
* First Star: ${data["game"]["liveData"]["decisions"]["firstStar"]["fullName"]}
%endif
%if data["game"]["liveData"]["decisions"].get("secondStar"):
* Second Star: ${data["game"]["liveData"]["decisions"]["secondStar"]["fullName"]}
%endif
%if data["game"]["liveData"]["decisions"].get("thirdStar"):
* Third Star: ${data["game"]["liveData"]["decisions"]["thirdStar"]["fullName"]}
%endif
