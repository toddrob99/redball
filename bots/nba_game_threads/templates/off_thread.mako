<%
    from datetime import datetime
%>\
% if settings.get("Off Day Thread", {}).get("STANDINGS_TYPE","Conference") == "Division":
<%include file="division_standings.mako" args="num_to_show=settings.get('Off Day Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
% elif settings.get("Off Day Thread", {}).get("STANDINGS_TYPE","Conference") == "Conference":
<%include file="conference_standings.mako" args="num_to_show=settings.get('Off Day Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
% elif settings.get("Off Day Thread", {}).get("STANDINGS_TYPE","Conference") == "League":
<%include file="league_standings.mako" args="num_to_show=settings.get('Off Day Thread',{}).get('STANDINGS_NUM_TO_SHOW', 8)" />
% endif

% if settings.get("Off Day Thread", {}).get("SCOREBOARD_TYPE","Conference") == "Division":
<%include file="division_scoreboard.mako" />
% elif settings.get("Off Day Thread", {}).get("SCOREBOARD_TYPE","Conference") == "Conference":
<%include file="conference_scoreboard.mako" />
% elif settings.get("Off Day Thread", {}).get("SCOREBOARD_TYPE","Conference") == "League":
<%include file="league_scoreboard.mako" />
% endif

## Configurable footer text
${settings.get('Off Day Thread',{}).get('FOOTER','')}