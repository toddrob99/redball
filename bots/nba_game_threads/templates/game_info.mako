## Date/Time
* Game Time: ${data["gameTime"]["myTeam"].strftime(settings.get("Game Thread", {}).get("THREAD_DATE_FORMAT","%B %d, %Y @ %I:%M %p %Z"))}
## Venue
* Venue: ${data["game"]["summary"].box_score_summary.arena.arena_name} - ${data["game"]["summary"].box_score_summary.arena.arena_city}, ${data["game"]["summary"].box_score_summary.arena.arena_state}
% if data["gameStatus"] < 3:
<%
    nationalTv = data["game"]["summary"].box_score_summary.broadcasters.national_broadcasters
    awayTv = data["game"]["summary"].box_score_summary.broadcasters.away_tv_broadcasters
    awayRadio = data["game"]["summary"].box_score_summary.broadcasters.away_radio_broadcasters
    homeTv = data["game"]["summary"].box_score_summary.broadcasters.home_tv_broadcasters
    homeRadio = data["game"]["summary"].box_score_summary.broadcasters.home_radio_broadcasters
%>\
* TV: \
<%
    tv = ''
    flag = False
    for x in [(nationalTv, "National"), (awayTv, data["game"]["summary"].box_score_summary.away_team.team_city), (homeTv, data["game"]["summary"].box_score_summary.home_team.team_city)]:
        if len(x[0]):
            if flag:
                tv += ', '
            flag = True
            tv += f'**{x[1]}**: '
            tv += ", ".join(list(set([x.broadcast_display for x in x[0]])))

    if tv == '': tv = 'None'
%>\
${tv}
* Radio: \
<%
    radio = ''
    flag = False
    for x in [(awayRadio, data["game"]["summary"].box_score_summary.away_team.team_city), (homeRadio, data["game"]["summary"].box_score_summary.home_team.team_city)]:
        if len(x[0]):
            if flag:
                radio += ', '
            flag = True
            radio += f'**{x[1]}**: '
            radio += ", ".join(list(set([x.broadcast_display for x in x[0]])))

    if radio == '': radio = 'None'
%>\
${radio}
% endif
* NBA Game [Summary](https://www.nba.com/game/${data["game"]["summary"].box_score_summary.game_id}) / [Charts](https://www.nba.com/game/${data["game"]["summary"].box_score_summary.game_id}/game-charts)