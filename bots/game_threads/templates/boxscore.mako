<%page args="boxStyle='wide'" />
<%
    import copy
    def playerLink(name, personId):
        return '[{}](http://mlb.mlb.com/team/player.jsp?player_id={})'.format(name,str(personId))
%>
% if boxStyle.lower() == 'wide':
    ## Wide Batting Boxes
    ## Displaying ops instead of avg and slg, to save a little space
    <%
        wideBattingBox = ''
        awayBatters = copy.deepcopy(data[gamePk]['boxscore']['awayBatters'])
        homeBatters = copy.deepcopy(data[gamePk]['boxscore']['homeBatters'])

        ##Make sure the home and away batter lists are the same length
        while len(awayBatters) > len(homeBatters):
            homeBatters.append({'namefield':'','ab':'','r':'','h':'','rbi':'','bb':'','k':'','lob':'','avg':'','ops':'','obp':'','slg':'','name':'','position':'','battingOrder':'-1','note':'','personId':0})

        while len(awayBatters) < len(homeBatters):
            awayBatters.append({'namefield':'','ab':'','r':'','h':'','rbi':'','bb':'','k':'','lob':'','avg':'','ops':'','obp':'','slg':'','name':'','position':'','battingOrder':'-1','note':'','personId':0})

        ##Get team totals
        awayBatters.append(data[gamePk]['boxscore']['awayBattingTotals'])
        homeBatters.append(data[gamePk]['boxscore']['homeBattingTotals'])

        ##Build the batting box!
        if len(awayBatters) > 2:
            for i in range(0,len(awayBatters)):
                if awayBatters[i]['namefield'].find('Batters') == -1 and awayBatters[i]['namefield'] != 'Totals':
                    awayBatters[i].update({'namefield' : awayBatters[i]['note'] + playerLink(awayBatters[i]['name'],awayBatters[i]['personId']) + ' - ' + awayBatters[i]['position']})

                wideBattingBox += '|'
                if awayBatters[i]['battingOrder'] != '' and awayBatters[i]['battingOrder'][-2:]=='00':
                    wideBattingBox += awayBatters[i]['battingOrder'][0]

                wideBattingBox += '|{namefield}|{ab}|{r}|{h}|{rbi}|{bb}|{k}|{lob}|{avg}|{ops}| |'.format(**awayBatters[i])

                if homeBatters[i]['namefield'].find('Batters') == -1 and homeBatters[i]['namefield'] != 'Totals':
                    homeBatters[i].update({'namefield' : homeBatters[i]['note'] + playerLink(homeBatters[i]['name'],homeBatters[i]['personId']) + ' - ' + homeBatters[i]['position']})

                if homeBatters[i]['battingOrder'] != '' and homeBatters[i]['battingOrder'][-2:]=='00':
                    wideBattingBox += homeBatters[i]['battingOrder'][0]

                wideBattingBox += '|{namefield}|{ab}|{r}|{h}|{rbi}|{bb}|{k}|{lob}|{avg}|{ops}|\n'.format(**homeBatters[i])
                if i==0:
                    wideBattingBox += '|:--'*(11*2+1) + '|\n' # Left-align cols for away, home, plus separator

        ##Get batting notes
        awayBattingNotes = copy.deepcopy(data[gamePk]['boxscore']['awayBattingNotes'])
        homeBattingNotes = copy.deepcopy(data[gamePk]['boxscore']['homeBattingNotes'])

        ##Make sure notes are the same size
        while len(awayBattingNotes) > len(homeBattingNotes):
            homeBattingNotes.update({len(homeBattingNotes):''})

        while len(homeBattingNotes) > len(awayBattingNotes):
            awayBattingNotes.update({len(awayBattingNotes):''})

        ##Get batting and fielding info
        awayBoxInfo = {'BATTING':'', 'FIELDING':''}
        homeBoxInfo = {'BATTING':'', 'FIELDING':''}
        for infoType in ['BATTING','FIELDING']:
            ## if (infoType=='BATTING' and battingInfo) or (infoType=='FIELDING' and fieldingInfo):
            for z in (x for x in data[gamePk]['gumbo']['liveData']['boxscore']['teams']['away']['info'] if x.get('title')==infoType):
                for x in z['fieldList']:
                    awayBoxInfo[infoType] += ('**' + x.get('label','') + '**: ' + x.get('value','') + ' ')

            for z in (x for x in data[gamePk]['gumbo']['liveData']['boxscore']['teams']['home']['info'] if x.get('title')==infoType):
                for x in z['fieldList']:
                    homeBoxInfo[infoType] += ('**' + x.get('label','') + '**: ' + x.get('value','') + ' ')

        if len(awayBattingNotes) or len(homeBattingNotes) or len(awayBoxInfo['BATTING']) or len(awayBoxInfo['FIELDING']):
            wideBattingBox += '\n\n|{}|{}|\n|:--|:--|\n'.format(data[gamePk]['schedule']['teams']['away']['team']['teamName'], data[gamePk]['schedule']['teams']['home']['team']['teamName'])

        if len(awayBattingNotes) or len(homeBattingNotes):
            for i in range(0,len(awayBattingNotes)):
                wideBattingBox += '|{}|{}|\n'.format(awayBattingNotes[i], homeBattingNotes[i])

        if awayBoxInfo['BATTING'] != homeBoxInfo['BATTING']:
            wideBattingBox += '|{}{}|{}{}|\n'.format('BATTING: ' if len(awayBoxInfo['BATTING']) else '', awayBoxInfo['BATTING'], 'BATTING: ' if len(homeBoxInfo['BATTING']) else '', homeBoxInfo['BATTING'])

        if awayBoxInfo['FIELDING'] != homeBoxInfo['FIELDING']:
            wideBattingBox += '|{}{}|{}{}|\n'.format('FIELDING: ' if len(awayBoxInfo['FIELDING']) else '', awayBoxInfo['FIELDING'], 'FIELDING: ' if len(homeBoxInfo['FIELDING']) else '', homeBoxInfo['FIELDING'])

    %>
${wideBattingBox}

    ## Wide Pitching Boxes
    <%
        widePitchingBox = ''
        awayPitchers = copy.deepcopy(data[gamePk]['boxscore']['awayPitchers'])
        homePitchers = copy.deepcopy(data[gamePk]['boxscore']['homePitchers'])

        ## Make sure the home and away pitcher lists are the same length
        while len(awayPitchers) > len(homePitchers):
            homePitchers.append({'namefield':'','ip':'','h':'','r':'','er':'','bb':'','k':'','hr':'','era':'','p':'','s':'','name':'','personId':0,'note':''})

        while len(awayPitchers) < len(homePitchers):
            awayPitchers.append({'namefield':'','ip':'','h':'','r':'','er':'','bb':'','k':'','hr':'','era':'','p':'','s':'','name':'','personId':0,'note':''})

        ## Get team totals
        awayPitchers.append(data[gamePk]['boxscore']['awayPitchingTotals'])
        homePitchers.append(data[gamePk]['boxscore']['homePitchingTotals'])

        #Build the pitching box!
        if len(awayPitchers) > 2:
            for i in range(0,len(awayPitchers)):
                if i==0:
                    awayPitchers[i].update({'ps':'P-S'})
                    homePitchers[i].update({'ps':'P-S'})
                else:
                    if awayPitchers[i]['p'] != '':
                        awayPitchers[i].update({'ps':'{}-{}'.format(awayPitchers[i]['p'], awayPitchers[i]['s'])})
                    else:#if awayPitchers[i]['name'] == '':
                        awayPitchers[i].update({'ps':''})

                    if homePitchers[i]['p'] != '':
                        homePitchers[i].update({'ps':'{}-{}'.format(homePitchers[i]['p'], homePitchers[i]['s'])})
                    else:#if homePitchers[i]['name'] == '':
                        homePitchers[i].update({'ps':''})

                widePitchingBox += '|'
                widePitchingBox += playerLink(awayPitchers[i]['name'],awayPitchers[i]['personId']) if awayPitchers[i]['personId']!=0 else awayPitchers[i]['name']
                widePitchingBox += (' ' + awayPitchers[i]['note']) if len(awayPitchers[i]['note'])>0 else ''
                widePitchingBox += '|{ip}|{h}|{r}|{er}|{bb}|{k}|{hr}|{ps}|{era}| '.format(**awayPitchers[i])
                widePitchingBox += '|'
                widePitchingBox += playerLink(homePitchers[i]['name'],homePitchers[i]['personId']) if homePitchers[i]['personId']!=0 else homePitchers[i]['name']
                widePitchingBox += (' ' + homePitchers[i]['note']) if len(homePitchers[i]['note'])>0 else ''
                widePitchingBox += '|{ip}|{h}|{r}|{er}|{bb}|{k}|{hr}|{ps}|{era}|\n'.format(**homePitchers[i])
                if i==0:
                    widePitchingBox += '|:--'*(10*2+1) + '|\n'

    %>
${widePitchingBox}
% elif boxStyle.lower() == 'stacked':
    ## Stacked Batting Boxes
    ## Away Batting
    <%
        if 1==1:
            awayBattingBox = ''
            awayBatters = copy.deepcopy(data[gamePk]['boxscore']['awayBatters'])

            ## Get team totals
            awayBatters.append(data[gamePk]['boxscore']['awayBattingTotals'])

            ##Build the batting box!
            if len(awayBatters) > 2:
                for i in range(0,len(awayBatters)):
                    if awayBatters[i]['namefield'].find('Batters') == -1 and awayBatters[i]['namefield'] != 'Totals':
                        awayBatters[i].update({'namefield' : awayBatters[i]['note'] + playerLink(awayBatters[i]['name'],awayBatters[i]['personId']) + ' - ' + awayBatters[i]['position']})

                    awayBattingBox += '|' + (awayBatters[i]['battingOrder'][0] if awayBatters[i]['battingOrder'] != '' and awayBatters[i]['battingOrder'][-2:]=='00' else '') + '|{namefield}|{ab}|{r}|{h}|{rbi}|{bb}|{k}|{lob}|{avg}|{obp}|{slg}|\n'.format(**awayBatters[i])
                    if i==0:
                        awayBattingBox += '|:--'*12 + '|\n' # Left-align cols for away, plus separator

            ##Get batting notes
            awayBattingNotes = data[gamePk]['boxscore']['awayBattingNotes']

            ##Get batting and fielding info
            awayBoxInfo = {'BATTING':'', 'FIELDING':''}
            for infoType in ['BATTING','FIELDING']:
                ## if (infoType=='BATTING' and battingInfo) or (infoType=='FIELDING' and fieldingInfo):
                for z in (x for x in data[gamePk]['gumbo']['liveData']['boxscore']['teams']['away']['info'] if x.get('title')==infoType):
                    for x in z['fieldList']:
                        awayBoxInfo[infoType] += ('**' + x.get('label','') + '**: ' + x.get('value','') + ' ')

            if len(awayBattingNotes) or len(awayBoxInfo['BATTING']) or len(awayBoxInfo['FIELDING']):
                awayBattingBox += '\n\n|{}|\n|:--|\n'.format(data[gamePk]['schedule']['teams']['away']['team']['teamName'])

            if len(awayBattingNotes):
                awayBattingBox += '|{}|\n'.format(' '.join(awayBattingNotes.values()))

            if len(awayBoxInfo['BATTING']):
                awayBattingBox += '|{}{}|\n'.format('BATTING: ' if len(awayBoxInfo['BATTING']) else '', awayBoxInfo['BATTING'])

            if len(awayBoxInfo['FIELDING']):
                awayBattingBox += '|{}{}|\n'.format('FIELDING: ' if len(awayBoxInfo['FIELDING']) else '', awayBoxInfo['FIELDING'])

    %>
${awayBattingBox}

    ## Home Batting
    <%
        homeBattingBox = ''
        homeBatters = copy.deepcopy(data[gamePk]['boxscore']['homeBatters'])

        ## Get team totals
        homeBatters.append(data[gamePk]['boxscore']['homeBattingTotals'])

        ##Build the batting box!
        if len(homeBatters) > 2:
            for i in range(0,len(homeBatters)):
                if homeBatters[i]['namefield'].find('Batters') == -1 and homeBatters[i]['namefield'] != 'Totals':
                    homeBatters[i].update({'namefield' : homeBatters[i]['note'] + playerLink(homeBatters[i]['name'],homeBatters[i]['personId']) + ' - ' + homeBatters[i]['position']})

                homeBattingBox += '|' + (homeBatters[i]['battingOrder'][0] if homeBatters[i]['battingOrder'] != '' and homeBatters[i]['battingOrder'][-2:]=='00' else '') + '|{namefield}|{ab}|{r}|{h}|{rbi}|{bb}|{k}|{lob}|{avg}|{obp}|{slg}|\n'.format(**homeBatters[i])
                if i==0:
                    homeBattingBox += '|:--'*12 + '|\n' # Left-align cols for home, plus separator

        ##Get batting notes
        homeBattingNotes = data[gamePk]['boxscore']['homeBattingNotes']

        ##Get batting and fielding info
        homeBoxInfo = {'BATTING':'', 'FIELDING':''}
        for infoType in ['BATTING','FIELDING']:
            ## if (infoType=='BATTING' and battingInfo) or (infoType=='FIELDING' and fieldingInfo):
            for z in (x for x in data[gamePk]['gumbo']['liveData']['boxscore']['teams']['home']['info'] if x.get('title')==infoType):
                for x in z['fieldList']:
                    homeBoxInfo[infoType] += ('**' + x.get('label','') + '**: ' + x.get('value','') + ' ')

        if len(homeBattingNotes) or len(homeBoxInfo['BATTING']) or len(homeBoxInfo['FIELDING']):
            homeBattingBox += '\n\n|{}|\n|:--|\n'.format(data[gamePk]['schedule']['teams']['home']['team']['teamName'])

        if len(homeBattingNotes):
            homeBattingBox += '|{}|\n'.format(' '.join(homeBattingNotes.values()))

        if len(homeBoxInfo['BATTING']):
            homeBattingBox += '|{}{}|\n'.format('BATTING: ' if len(homeBoxInfo['BATTING']) else '', homeBoxInfo['BATTING'])

        if len(homeBoxInfo['FIELDING']):
            homeBattingBox += '|{}{}|\n'.format('FIELDING: ' if len(homeBoxInfo['FIELDING']) else '', homeBoxInfo['FIELDING'])

    %>
${homeBattingBox}

    ## Stacked Pitching Boxes
    ## Away Pitching
    <%
        awayPitchingBox = ''
        awayPitchers = copy.deepcopy(data[gamePk]['boxscore']['awayPitchers'])

        ## Get team totals
        awayPitchers.append(data[gamePk]['boxscore']['awayPitchingTotals'])

        #Build the pitching box!
        if len(awayPitchers) > 2:
            if len(awayPitchers):
                for i in range(0,len(awayPitchers)):
                    if i==0:
                        awayPitchers[i].update({'ps':'P-S'})
                    elif awayPitchers[i]['p'] != '':
                        awayPitchers[i].update({'ps':'{}-{}'.format(awayPitchers[i]['p'], awayPitchers[i]['s'])})
                    else:#if awayPitchers[i]['name'] == '':
                        awayPitchers[i].update({'ps':''})

                    awayPitchingBox += '|'
                    awayPitchingBox += playerLink(awayPitchers[i]['name'],awayPitchers[i]['personId']) if awayPitchers[i]['personId']!=0 else awayPitchers[i]['name']
                    awayPitchingBox += (' ' + awayPitchers[i]['note']) if len(awayPitchers[i]['note'])>0 else ''
                    awayPitchingBox += '|{ip}|{h}|{r}|{er}|{bb}|{k}|{hr}|{ps}|{era}|\n'.format(**awayPitchers[i])
                    if i==0:
                        awayPitchingBox += '|:--'*10 + '|\n'

    %>
${awayPitchingBox}

    ## Home Pitching
    <%
        homePitchingBox = ''
        homePitchers = copy.deepcopy(data[gamePk]['boxscore']['homePitchers'])

        ## Get team totals
        homePitchers.append(data[gamePk]['boxscore']['homePitchingTotals'])

        #Build the pitching box!
        if len(homePitchers) > 2:
            if len(homePitchers):
                for i in range(0,len(homePitchers)):
                    if i==0:
                        homePitchers[i].update({'ps':'P-S'})
                    elif homePitchers[i]['p'] != '':
                        homePitchers[i].update({'ps':'{}-{}'.format(homePitchers[i]['p'], homePitchers[i]['s'])})
                    else:#if homePitchers[i]['name'] == '':
                        homePitchers[i].update({'ps':''})

                    homePitchingBox += '|'
                    homePitchingBox += playerLink(homePitchers[i]['name'],homePitchers[i]['personId']) if homePitchers[i]['personId']!=0 else homePitchers[i]['name']
                    homePitchingBox += (' ' + homePitchers[i]['note']) if len(homePitchers[i]['note'])>0 else ''
                    homePitchingBox += '|{ip}|{h}|{r}|{er}|{bb}|{k}|{hr}|{ps}|{era}|\n'.format(**homePitchers[i])
                    if i==0:
                        homePitchingBox += '|:--'*10 + '|\n'

    %>
${homePitchingBox}

% endif

## Include game info if game is final
% if data[gamePk]['schedule']['status']['abstractGameCode'] == 'F':
    % if len(data[gamePk]['boxscore']['gameBoxInfo']):
|Game Info|
|:--|
    % endif
    % for x in data[gamePk]['boxscore']['gameBoxInfo']:
|${x['label'] + (': ' if x.get('value') else '') + x.get('value','')}|
    % endfor
% endif
