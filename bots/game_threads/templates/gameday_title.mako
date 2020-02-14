<%
    from datetime import datetime 
    prefix = settings.get("Game Day Thread", {}).get("TITLE_PREFIX","Game Day Thread")
%>\
${data[0]['myTeam']['teamName']} ${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}- ${datetime.strptime(data[0]['today']['Ymd'],'%Y%m%d').strftime('%A, %B %d')}