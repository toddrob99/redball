<%page args="gamePk" />
${'###'}Links & Info
## Venue & weather
% if data[gamePk]['schedule'].get('weather') and len(data[gamePk]['schedule']['weather']) and (data[gamePk]['schedule']['weather'].get('temp') or data[gamePk]['schedule']['weather'].get('condition') or data[gamePk]['schedule']['weather'].get('wind') != 'null mph, null'):
* Current conditions at ${data[gamePk]['schedule']['venue']['name']}: ${data[gamePk]['schedule']['weather']['temp']+'&#176;F' if data[gamePk]['schedule']['weather'].get('temp') else ''} ${'- ' + data[gamePk]['schedule']['weather']['condition'] if data[gamePk]['schedule']['weather'].get('condition') else ''} ${'- Wind ' + data[gamePk]['schedule']['weather']['wind'] if data[gamePk]['schedule']['weather'].get('wind')  != 'null mph, null' else ''}
% else:
* Venue: ${data[gamePk]['schedule']['venue']['name']}
% endif
<%
    awayTv = [x for x in data[gamePk]['schedule'].get('broadcasts', []) if x.get('type')=='TV' and x.get('homeAway')=='away' and not x.get('isNational',False)]
    awayRadio = [x for x in data[gamePk]['schedule'].get('broadcasts', []) if x.get('type') in ['FM','AM'] and x.get('homeAway')=='away' and not x.get('isNational',False)]
    homeTv = [x for x in data[gamePk]['schedule'].get('broadcasts', []) if x.get('type')=='TV' and x.get('homeAway')=='home' and not x.get('isNational',False)]
    homeRadio = [x for x in data[gamePk]['schedule'].get('broadcasts', []) if x.get('type') in ['FM','AM'] and x.get('homeAway')=='home' and not x.get('isNational',False)]
    nationalTv = [x for x in data[gamePk]['schedule'].get('broadcasts', []) if x.get('type')=='TV' and x.get('isNational')]
    nationalRadio = [x for x in data[gamePk]['schedule'].get('broadcasts', []) if x.get('type')=='Radio' and x.get('isNational')]
%>\
* TV: \
<%
    tv = ''
    flag = False
    if len(nationalTv):
        flag = True
        tv += '**National**:'
        used = []
        while len(nationalTv):
            r = nationalTv.pop()
            if r['name'] not in used:
                tv += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r['language']!='en' else '')
                used.append(r['name'])
                if len(nationalTv) and nationalTv[0]['name'] not in used: tv += ','

    if len(awayTv):
        if flag: tv += ', '
        flag = True
        tv += '**{}**:'.format(data[gamePk]['schedule']['teams']['away']['team']['teamName'])
        used = []
        while len(awayTv):
            r = awayTv.pop()
            if r['name'] not in used:
                tv += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r['language']!='en' else '')
                used.append(r['name'])
                if len(awayTv) and awayTv[0]['name'] not in used: tv += ','

    if len(homeTv):
        if flag: tv += ', '
        flag = None
        tv += '**{}**:'.format(data[gamePk]['schedule']['teams']['home']['team']['teamName'])
        used = []
        while len(homeTv):
            r = homeTv.pop()
            if r['name'] not in used:
                tv += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r['language']!='en' else '')
                used.append(r['name'])
                if len(homeTv) and homeTv[0]['name'] not in used: tv += ','

    if tv == '': tv = 'None'
%>\
${tv}
* Radio: \
<%
    radio = ''
    flag = False
    if len(nationalRadio):
        flag = True
        radio += '**National**:'
        used = []
        while len(nationalRadio):
            r = nationalRadio.pop()
            if r['name'] not in used:
                radio += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r['language']!='en' else '')
                used.append(r['name'])
                if len(nationalRadio) and nationalRadio[0]['name'] not in used: radio += ','

    if len(awayRadio):
        if flag: radio += ', '
        flag = True
        radio += '**{}**:'.format(data[gamePk]['schedule']['teams']['away']['team']['teamName'])
        used = []
        while len(awayRadio):
            r = awayRadio.pop()
            if r['name'] not in used:
                radio += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r['language']!='en' else '')
                used.append(r['name'])
                if len(awayRadio) and awayRadio[0]['name'] not in used: radio += ','

    if len(homeRadio):
        if flag: radio += ', '
        flag = None
        radio += '**{}**:'.format(data[gamePk]['schedule']['teams']['home']['team']['teamName'])
        used = []
        while len(homeRadio):
            r = homeRadio.pop()
            radio += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r['language']!='en' else '')
            if len(homeRadio) and homeRadio[0]['name'] not in used: radio += ','

    if radio == '': radio = 'None'
%>\
${radio}
* [MLB Gameday](https://www.mlb.com/gameday/${gamePk}/)
##* Game Notes: [${data[gamePk]['schedule']['teams']['away']['team']['teamName']}](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=${data[gamePk]['schedule']['teams']['away']['team']['fileCode']}), [${data[gamePk]['schedule']['teams']['home']['team']['teamName']}](http://mlb.mlb.com/mlb/presspass/gamenotes.jsp?c_id=${data[gamePk]['schedule']['teams']['home']['team']['fileCode']})

% if 1==1 or (data[gamePk]['schedule']['status']['abstractGameCode'] == 'L' and data[gamePk]['schedule']['status']['statusCode'] != 'PW') or data[gamePk]['schedule']['status']['abstractGameCode'] == 'F':
##* ${'[Strikezone Map](http://www.brooksbaseball.net/pfxVB/zoneTrack.php?month={}&day={}&year={}&game=gid_{})'.format(data[gamePk]['gameTime']['homeTeam'].strftime('%m'), data[gamePk]['gameTime']['homeTeam'].strftime('%d'), data[gamePk]['gameTime']['homeTeam'].strftime('%Y'), data[gamePk]['gumbo']['gameData']['game']['id'].replace('/','_').replace('-','_'))}
* ${'[Game Graphs](http://www.fangraphs.com/livewins.aspx?date={}&team={}&dh={}&season={})'.format( data[gamePk]['gameTime']['homeTeam'].strftime("%Y-%m-%d"), data[gamePk]['schedule']['teams']['home']['team']['teamName'].replace(' ','%20'), data[gamePk]['schedule']['gameNumber'] if data[gamePk]['schedule']['doubleHeader']!='N' else 0, data[gamePk]['gameTime']['homeTeam'].strftime('%Y'))}
% endif