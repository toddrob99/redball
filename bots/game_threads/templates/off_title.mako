<%
    from datetime import datetime
    prefix = settings.get("Off Day Thread", {}).get("TITLE_PREFIX","Off Day Thread") 
%>\
${data[0]['myTeam']['teamName']} \
${prefix if data[0]['myTeam']['seasonState'] in ['pre','regular','post:in'] else ''}\
${'Postseason Discussion Thread' if data[0]['myTeam']['seasonState'] == 'post:out' else ''}\
${'Offseason Discussion Thread' if data[0]['myTeam']['seasonState'].startswith('off') else ''}\
 - ${datetime.strptime(data[0]['today']['Ymd'],'%Y%m%d').strftime('%A, %B %d')}