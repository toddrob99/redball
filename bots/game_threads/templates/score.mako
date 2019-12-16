Score: ${sorted([data[gamePk]['schedule']['teams']['away']['score'],data[gamePk]['schedule']['teams']['home']['score']],reverse=True)[0]}-\
${sorted([data[gamePk]['schedule']['teams']['away']['score'],data[gamePk]['schedule']['teams']['home']['score']],reverse=True)[1]} \
% if data[gamePk]['schedule']['teams']['away']['score'] > data[gamePk]['schedule']['teams']['home']['score']:
${data[gamePk]['schedule']['teams']['away']['team']['teamName']}\
% elif data[gamePk]['schedule']['teams']['away']['score'] < data[gamePk]['schedule']['teams']['home']['score']:
${data[gamePk]['schedule']['teams']['home']['team']['teamName']}\
% endif