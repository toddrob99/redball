## Linescore
<%
    if not data[gamePk]['schedule'].get('linescore',{}).get('innings'):
        return

    header_row = []
    home = []
    away = []
    for i in data[gamePk]['schedule']['linescore']['innings']:
        header_row.append(str(i['num']))
        away.append(str(i['away'].get('runs','')))
        home.append(str(i['home'].get('runs','')))

    if len(data[gamePk]['schedule']['linescore']['innings']) < 9:
        for i in range(len(data[gamePk]['schedule']['linescore']['innings'])+1, 10):
            header_row.append(str(i))
            away.append(' ')
            home.append(' ')

    header_row.extend(['','R','H','E','LOB'])
    away.extend([
        '',
        str(data[gamePk]['schedule']['linescore']['teams']['away'].get('runs',0)),
        str(data[gamePk]['schedule']['linescore']['teams']['away'].get('hits',0)),
        str(data[gamePk]['schedule']['linescore']['teams']['away'].get('errors',0)),
        str(data[gamePk]['schedule']['linescore']['teams']['away'].get('leftOnBase',0))
    ])
    home.extend([
        '',
        str(data[gamePk]['schedule']['linescore']['teams']['home'].get('runs',0)),
        str(data[gamePk]['schedule']['linescore']['teams']['home'].get('hits',0)),
        str(data[gamePk]['schedule']['linescore']['teams']['home'].get('errors',0)),
        str(data[gamePk]['schedule']['linescore']['teams']['home'].get('leftOnBase',0))
    ])
%>
% for r in [['',header_row],[data[gamePk]['schedule']['teams']['away']['team']['teamName'],away],[data[gamePk]['schedule']['teams']['home']['team']['teamName'],home]]:
|${r[0]}|\
% for ri in r[1]:
${ri}|\
% endfor

% if r[0]=='':
|:--|\
${':--|'*len(r[1])}
% endif
% endfor
