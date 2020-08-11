<%
    from datetime import datetime 
    prefix = settings.get("Game Day Thread", {}).get("TITLE_PREFIX","Game Day Thread")
    dateFormat = settings.get("Game Day Thread", {}).get("DATE_FORMAT","%A, %B %d")
%>\
${data[0]['myTeam']['teamName']} ${prefix + (" " if len(prefix) and not prefix.endswith(" ") else "")}- ${datetime.strptime(data[0]['today']['Ymd'],'%Y%m%d').strftime(dateFormat)}