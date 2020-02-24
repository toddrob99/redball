% if settings.get("Comments", {}).get("MYTEAM_BATTING_HEADER" if myTeamBatting else "MYTEAM_PITCHING_HEADER"):
## Header is defined for all events
${settings['Comments']["MYTEAM_BATTING_HEADER" if myTeamBatting else "MYTEAM_PITCHING_HEADER"]}

% endif
% if actionOrResult == 'action':
## Event occurred during an at-bat
    % if settings.get("Comments", {}).get(("MYTEAM_BATTING_HEADER_" if myTeamBatting else "MYTEAM_PITCHING_HEADER_") + eventType.upper()):
    ## Header is defined for this event
${settings['Comments'][("MYTEAM_BATTING_HEADER_" if myTeamBatting else "MYTEAM_PITCHING_HEADER_") + eventType.upper()]}

    % else:
    ## Use event for header
${'###'} ${atBat["playEvents"][actionIndex]["details"].get("event", "")}

    ## End if custom event header
    % endif
## The event description:
${atBat["playEvents"][actionIndex]["details"].get('description', "")}
    % if settings.get("Comments", {}).get(("MYTEAM_BATTING_FOOTER_" if myTeamBatting else "MYTEAM_PITCHING_FOOTER_") +eventType.upper()):
    ## Footer is defined for this event

${settings['Comments'][("MYTEAM_BATTING_FOOTER_" if myTeamBatting else "MYTEAM_PITCHING_FOOTER_") + eventType.upper()]}
    ## End if custom event footer
    % endif
## End if actionOrResult == 'action'
% elif actionOrResult == 'result':
## Event is the result of an at-bat
    % if settings.get("Comments", {}).get(("MYTEAM_BATTING_HEADER_" if myTeamBatting else "MYTEAM_PITCHING_HEADER_") + eventType.upper()):
    ## Header is defined for this event
${settings['Comments'][("MYTEAM_BATTING_HEADER_" if myTeamBatting else "MYTEAM_PITCHING_HEADER_") + eventType.upper()]}

    ## End if custom event header
    %elif eventType == 'home_run':
    ## Use standard home run headers
        % if atBat['result']['rbi'] == 4:
# GRAND SLAM!
        % else:
# HOME RUN!
        % endif
    ## End if eventType == 'home_run'
    % elif eventType == 'strikeout':
        % if atBat['playEvents'][atBat['pitchIndex'][-1]]['details']['code'] == 'C':
${'#'} &#xA4D8; (${data[gamePk]["gumbo"]["liveData"]["boxscore"]["teams"]["home" if atBat['about']['halfInning'] == 'top' else "away"]["players"]["ID" + str(atBat['matchup']['pitcher']['id'])]["stats"]["pitching"]["strikeOuts"]})
        % else:
${'###'} K (${data[gamePk]["gumbo"]["liveData"]["boxscore"]["teams"]["home" if atBat['about']['halfInning'] == 'top' else "away"]["players"]["ID" + str(atBat['matchup']['pitcher']['id'])]["stats"]["pitching"]["strikeOuts"]})
        % endif
    ## End if custom event header
    % else:
${'###'} ${atBat['result']['event']}
    ## End else (if eventType == * or custom event header)
    % endif
## The event description:
${atBat['result']['description']}
    % if atBat['playEvents'][atBat['pitchIndex'][-1]].get('pitchData'):
    ## Event has pitch data

Pitch from ${atBat['matchup']['pitcher']['fullName']}: ${atBat['playEvents'][atBat['pitchIndex'][-2]].get('count',{}).get('balls','0')}-${atBat['playEvents'][atBat['pitchIndex'][-2]].get('count',{}).get('strikes','0')} ${atBat['playEvents'][atBat['pitchIndex'][-1]].get('details',{}).get('type',{}).get('description','Unknown pitch type')} @ ${atBat['playEvents'][atBat['pitchIndex'][-1]].get('pitchData',{}).get('startSpeed','-')} mph
    % endif
    % if atBat['playEvents'][atBat['pitchIndex'][-1]].get('hitData'):
    ## Event has hit data

Hit by ${atBat['matchup']['batter']['fullName']}: Launched ${atBat['playEvents'][atBat['pitchIndex'][-1]].get('hitData',{}).get('launchSpeed','-')} mph at ${atBat['playEvents'][atBat['pitchIndex'][-1]].get('hitData',{}).get('launchAngle','-')}&#176; for a total distance of ${atBat['playEvents'][atBat['pitchIndex'][-1]].get('hitData',{}).get('totalDistance','-')} ft
    % endif
    % if atBat['about']['isScoringPlay']:
    ## Event is a scoring play, so include the updated score (and inning)

${atBat['about']['halfInning'].capitalize()} ${atBat['about']['inning']} - \
${max(atBat['result']['homeScore'], atBat['result']['awayScore'])}-${min(atBat['result']['homeScore'], atBat['result']['awayScore'])} 
${'TIE' if atBat['result']['homeScore'] == atBat['result']['awayScore'] else data[0]['myTeam']['teamName'] if atBat['result']['homeScore'] > atBat['result']['awayScore'] and data[gamePk]['homeAway']=='home' else data[gamePk]['oppTeam']['teamName']}
    % endif
    % if settings.get("Comments", {}).get(("MYTEAM_BATTING_FOOTER_" if myTeamBatting else "MYTEAM_PITCHING_FOOTER_") + eventType.upper()):
    ## Footer is defined for this event

${settings['Comments'][("MYTEAM_BATTING_FOOTER_" if myTeamBatting else "MYTEAM_PITCHING_FOOTER_") + eventType.upper()]}
    ## End if custom event footer
    % endif
## End elif actionOrResult == 'result'
% endif
% if settings.get("Comments", {}).get("MYTEAM_BATTING_FOOTER" if myTeamBatting else "MYTEAM_PITCHING_FOOTER"):
## Footer is defined for all events

${settings['Comments']["MYTEAM_BATTING_FOOTER" if myTeamBatting else "MYTEAM_PITCHING_FOOTER"]}
% endif