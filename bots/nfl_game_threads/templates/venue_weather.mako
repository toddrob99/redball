<%
    game = data["todayGames"][data["myGameIndex"]]
%>\
%if data["gameDetails"] and data["gameDetails"].get("weather") and data["gameDetails"].get("weather", {}).get("shortDescription"):
Weather at ${game["venue"]["name"]}: ${data["gameDetails"]["weather"]["shortDescription"]}
%else:
Venue: ${game["venue"]["name"]}
%endif