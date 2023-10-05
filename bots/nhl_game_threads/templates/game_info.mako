<%
    def highlight_url(clip_id):
        return f"https://players.brightcove.net/6415718365001/EXtG1xJ7H_default/index.html?videoId={clip_id}"
%>\
% if data["game"].get("gameScheduleState") == "PPD":
* Game Time: POSTPONED
% elif data["game"].get("gameScheduleState") == "SUSP":
* Game Time: SUSPENDED
% elif data["game"].get("gameScheduleState") == "CNCL":
* Game Time: CANCELED
% else:
## Date/Time
* Game Time: ${data["gameTime"]["myTeam"].strftime(settings.get("Game Thread", {}).get("TITLE_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}
% endif
## Venue
* Venue: ${data["game"].get("venue", "Unknown")}
<%
    awayTv = [x for x in data['game'].get('tvBroadcasts', []) if x.get('market')=='A']
    homeTv = [x for x in data['game'].get('tvBroadcasts', []) if x.get('market')=='H']
    nationalTv = [x for x in data['game'].get('tvBroadcasts', []) if x.get('market')=='N']
%>\
* TV: \
<%
    tv = ''
    flag = False
    for info in [(nationalTv, "National"), (awayTv, data["game"]["awayTeam"]["name"]), (homeTv, data["game"]["homeTeam"]["name"])]:
        if len(info[0]):
            if flag: tv += ', '
            flag = True
            tv += '**{}**:'.format(info[1])
            used = []
            while len(info[0]):
                r = info[0].pop()
                if r['network'] not in used:
                    tv += ' {}{}'.format(r['network'],' (' + r['countryCode'] + ')' if r.get('countryCode', 'US')!='US' else '')
                    used.append(r['network'])
                    if len(info[0]) and info[0][0]['network'] not in used: tv += ','

    if tv == '': tv = 'None'
%>\
${tv}
* [NHL GameCenter](https://www.nhl.com/gamecenter/${data["game"]["id"]})
% if data["game_boxscore"].get("gameVideo", {}).get("threeMinRecap"):
* [Three Minute Recap](${highlight_url(data["game_boxscore"]["gameVideo"]["threeMinRecap"])})
% endif
% if data["game_boxscore"].get("gameVideo", {}).get("condensedGame"):
* [Condensed Game](${highlight_url(data["game_boxscore"]["gameVideo"]["condensedGame"])})
% endif
