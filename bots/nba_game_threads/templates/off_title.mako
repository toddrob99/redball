<%
    from datetime import datetime
    prefix = settings.get("Off Day Thread", {}).get("TITLE_PREFIX","Off Day Thread:")
%>\
## Prefix
${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}\
${data["myTeam"].team_info.team_city} ${data["myTeam"].team_info.team_name} \
## TODO: Vary based on season status
Off Day \
Discussion Thread\
## Date/Time
${(" - " + datetime.now().strftime(settings.get("Off Day Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y"))) if settings.get("Off Day Thread", {}).get("TITLE_DATE_FORMAT") != "" else ""}