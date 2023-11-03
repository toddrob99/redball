<%
    awayTeam = data["myTeam"] if data["homeAway"] == "away" else data["oppTeam"]
    homeTeam = data["myTeam"] if data["homeAway"] == "home" else data["oppTeam"]
    def playerLink(p):
        return f"[{p['name']['default']}](https://www.nhl.com/player/{p['playerId']})"
    threeStars = data["game"].get("summary", {}).get("threeStars")
    labels = ["First", "Second", "Third"]
%>\
% if threeStars:
${'##'} Stars of the Game
##%   if data["game"]["liveData"]["decisions"].get("winner", {}).get("fullName"):
##* Winner: ${playerLink(data["game"]["liveData"]["decisions"]["winner"])}
##%   endif
##%   if data["game"]["liveData"]["decisions"].get("loser", {}).get("fullName"):
##* Loser: ${playerLink(data["game"]["liveData"]["decisions"]["loser"])}
##%   endif
% for p in threeStars:
* ${labels[p["star"] - 1]} Star: ${playerLink(p)} (${p["teamAbbrev"]})\
%   if p.get("goals") is not None and p.get("assists") is not None:
 Goals: ${p["goals"]}, Assists: ${p["assists"]}
%   else:

%   endif
% endfor
% endif