% if None in [data[gamePk]['schedule']['teams']['away'].get('score'), data[gamePk]['schedule']['teams']['home'].get('score')]:
${''}\
% else:
Score: ${sorted([data[gamePk]['schedule']['teams']['away'].get('score', 0),data[gamePk]['schedule']['teams']['home'].get('score', 0)],reverse=True)[0]}-\
${sorted([data[gamePk]['schedule']['teams']['away'].get('score', 0),data[gamePk]['schedule']['teams']['home'].get('score', 0)],reverse=True)[1]} \
% if data[gamePk]['schedule']['teams']['away'].get('score', 0) > data[gamePk]['schedule']['teams']['home'].get('score', 0):
${data[gamePk]['schedule']['teams']['away']['team']['teamName']}\
% elif data[gamePk]['schedule']['teams']['away'].get('score', 0) < data[gamePk]['schedule']['teams']['home'].get('score', 0):
${data[gamePk]['schedule']['teams']['home']['team']['teamName']}\
% elif data[gamePk]['schedule']['teams']['away'].get('score', 0) == data[gamePk]['schedule']['teams']['home'].get('score', 0):
${''}\
% endif
% endif