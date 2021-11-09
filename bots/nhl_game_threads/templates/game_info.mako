## Date/Time
* Game Time: ${data["gameTime"]["myTeam"].strftime(settings.get("Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}
## Venue
* Venue: ${data["game"]["gameData"].get("venue", {}).get("name")}
<%
    awayTv = [x for x in data['todayGames'][0].get('broadcasts', []) if x.get('type')=='away']
    awayRadio = [x for x in data['todayGames'][0].get('radioBroadcasts', []) if x.get('type')=='away']
    homeTv = [x for x in data['todayGames'][0].get('broadcasts', []) if x.get('type')=='home']
    homeRadio = [x for x in data['todayGames'][0].get('radioBroadcasts', []) if x.get('type')=='home']
    nationalTv = [x for x in data['todayGames'][0].get('broadcasts', []) if x.get('type')=='national']
    nationalRadio = [x for x in data['todayGames'][0].get('radioBroadcasts', []) if x.get('type')=='home']
%>\
* TV: \
<%
    tv = ''
    flag = False
    for info in [(nationalTv, "National"), (awayTv, data["game"]["gameData"]["teams"]["away"]["teamName"]), (homeTv, data["game"]["gameData"]["teams"]["home"]["teamName"])]:
        if len(info[0]):
            if flag: tv += ', '
            flag = True
            tv += '**{}**:'.format(info[1])
            used = []
            while len(info[0]):
                r = info[0].pop()
                if r['name'] not in used:
                    tv += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r.get('language', 'en')!='en' else '')
                    used.append(r['name'])
                    if len(info[0]) and info[0][0]['name'] not in used: tv += ','

    if tv == '': tv = 'None'
%>\
${tv}
* Radio: \
<%
    radio = ''
    flag = False
    if len(awayRadio):
        if flag: radio += ', '
        flag = True
        radio += '**{}**:'.format(data["game"]["gameData"]["teams"]["away"]["teamName"])
        used = []
        while len(awayRadio):
            r = awayRadio.pop()
            if r['name'] not in used:
                radio += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r.get('language', 'en')!='en' else '')
                used.append(r['name'])
                if len(awayRadio) and awayRadio[0]['name'] not in used: radio += ','

    if len(homeRadio):
        if flag: radio += ', '
        flag = None
        radio += '**{}**:'.format(data["game"]["gameData"]["teams"]["home"]["teamName"])
        used = []
        while len(homeRadio):
            r = homeRadio.pop()
            radio += ' {}{}'.format(r['name'],' (' + r['language'] + ')' if r.get('language', 'en')!='en' else '')
            if len(homeRadio) and homeRadio[0]['name'] not in used: radio += ','

    if radio == '': radio = 'None'
%>\
${radio}
* [NHL GameCenter](https://www.nhl.com/gamecenter/${data["game"]["gamePk"]})