<%
    from datetime import datetime 
%>\
Weekly ${data[0]['myTeam']['teamName']} \
${'Discussion Thread' if data[0]['myTeam']['seasonState'] in ['regular','post:in'] else ''}\
${'Postseason Discussion Thread' if data[0]['myTeam']['seasonState'] == 'post:out' else ''}\
${'Offseason Discussion Thread' if data[0]['myTeam']['seasonState'].startswith('off') else ''}\
 - ${datetime.strptime(data[0]['today']['Ymd'],'%Y%m%d').strftime('%A, %B %d')}