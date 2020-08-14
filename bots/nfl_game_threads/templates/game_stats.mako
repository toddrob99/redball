<%
    from datetime import timedelta
    if not len(data["gameStats"]):
        return

    game = data["todayGames"][data["myGameIndex"]]
    v = "teamGameStats" if data["homeVisitor"] == "visitor" else "opponentGameStats"
    h = "opponentGameStats" if v == "teamGameStats" else "opponentGameStats"
    headerRowTemplate = "|"
    alignmentRowTemplate = "|:--|"
    visitorRowTemplate = f'|{game["visitorTeam"]["abbr"]}|'
    homeRowTemplate = f'|{game["homeTeam"]["abbr"]}|'

    # General table
    gen_headerRow = headerRowTemplate + "|"
    gen_alignmentRow = alignmentRowTemplate
    gen_visitorRow = visitorRowTemplate
    gen_homeRow = homeRowTemplate

    # Time of possession
    gen_headerRow += "Time/Poss|"
    gen_alignmentRow += ":--|"
    gen_visitorRow += f'{str(timedelta(seconds=data["gameStats"][v]["timeOfPossSeconds"]))[-5:]}|'
    gen_homeRow += f'{str(timedelta(seconds=data["gameStats"][h]["timeOfPossSeconds"]))[-5:]}|'

    # Total plays
    gen_headerRow += "Plays (Yds)|"
    gen_alignmentRow += ":--|"
    gen_visitorRow += f'{data["gameStats"][v]["scrimmagePlays"]} ({data["gameStats"][v]["scrimmageYds"]})|'
    gen_homeRow += f'{data["gameStats"][h]["scrimmagePlays"]} ({data["gameStats"][h]["scrimmageYds"]})|'

    # Third downs
    gen_headerRow += "3rd downs (Conv)|"
    gen_alignmentRow += ":--|"
    gen_visitorRow += f'{data["gameStats"][v]["down3rdAttempted"]} ({data["gameStats"][v]["down3rdFdMade"]})|'
    gen_homeRow += f'{data["gameStats"][h]["down3rdAttempted"]} ({data["gameStats"][h]["down3rdFdMade"]})|'

    # Penalties
    gen_headerRow += "Penalties (Yds)|"
    gen_alignmentRow += ":--|"
    gen_visitorRow += f'{data["gameStats"][v]["penaltiesTotal"]} ({data["gameStats"][v]["penaltiesYardsPenalized"]})|'
    gen_homeRow += f'{data["gameStats"][h]["penaltiesTotal"]} ({data["gameStats"][h]["penaltiesYardsPenalized"]})|'

    # Turnovers
    gen_headerRow += "Turnovers|"
    gen_alignmentRow += ":--|"
    gen_visitorRow += f'{data["gameStats"][v]["fumblesLost"] + data["gameStats"][v]["passingInterceptions"]}|'
    gen_homeRow += f'{data["gameStats"][h]["fumblesLost"] + data["gameStats"][h]["passingInterceptions"]}|'

    # Passing table
    pass_headerRow = headerRowTemplate + "Passing|"
    pass_alignmentRow = alignmentRowTemplate
    pass_visitorRow = visitorRowTemplate
    pass_homeRow = homeRowTemplate

    # Pass completions/attempts
    pass_headerRow += "Comp/Att|"
    pass_alignmentRow += ":--|"
    pass_visitorRow += f'{data["gameStats"][v]["passingCompletions"]}/{data["gameStats"][v]["passingAttempts"]}|'
    pass_homeRow += f'{data["gameStats"][h]["passingCompletions"]}/{data["gameStats"][h]["passingAttempts"]}|'

    # Pass yds
    pass_headerRow += "Yds Tot/Avg/Lng|"
    pass_alignmentRow += ":--|"
    pass_visitorRow += f'{data["gameStats"][v]["passingNetYards"]}/{data["gameStats"][v]["passingAverageYards"]}/{data["gameStats"][v]["passingLong"]}|'
    pass_homeRow += f'{data["gameStats"][h]["passingNetYards"]}/{data["gameStats"][h]["passingAverageYards"]}/{data["gameStats"][h]["passingLong"]}|'

    # Pass 1st downs
    pass_headerRow += "1st Dn|"
    pass_alignmentRow += ":--|"
    pass_visitorRow += f'{data["gameStats"][v]["passingFirstDowns"]}|'
    pass_homeRow += f'{data["gameStats"][h]["passingFirstDowns"]}|'

    # Pass TD
    pass_headerRow += "TD|"
    pass_alignmentRow += ":--|"
    pass_visitorRow += f'{data["gameStats"][v]["passingTouchdowns"]}|'
    pass_homeRow += f'{data["gameStats"][h]["passingTouchdowns"]}|'

    # Sacked
    pass_headerRow += "Sacked (Yds)|"
    pass_alignmentRow += ":--|"
    pass_visitorRow += f'{data["gameStats"][v]["passingSacked"]} ({data["gameStats"][v]["passingSackedYardsLost"]})|'
    pass_homeRow += f'{data["gameStats"][h]["passingSacked"]} ({data["gameStats"][h]["passingSackedYardsLost"]})|'

    # Interceptions
    pass_headerRow += "Int|"
    pass_alignmentRow += ":--|"
    pass_visitorRow += f'{data["gameStats"][v]["passingInterceptions"]}|'
    pass_homeRow += f'{data["gameStats"][h]["passingInterceptions"]}|'

    # Rushing table
    rush_headerRow = headerRowTemplate + "Rushing|"
    rush_alignmentRow = alignmentRowTemplate
    rush_visitorRow = visitorRowTemplate
    rush_homeRow = homeRowTemplate

    # Rushing attempts
    rush_headerRow += "Att|"
    rush_alignmentRow += ":--|"
    rush_visitorRow += f'{data["gameStats"][v]["rushingAttempts"]}|'
    rush_homeRow += f'{data["gameStats"][h]["rushingAttempts"]}|'

    # Rushing yds
    rush_headerRow += "Yds Tot/Avg/Lng|"
    rush_alignmentRow += ":--|"
    rush_visitorRow += f'{data["gameStats"][v]["rushingYards"]}/{data["gameStats"][v]["rushingAverageYards"]}/{data["gameStats"][v]["rushingLong"]}|'
    rush_homeRow += f'{data["gameStats"][h]["rushingYards"]}/{data["gameStats"][h]["rushingAverageYards"]}/{data["gameStats"][h]["rushingLong"]}|'

    # Rushing 1st downs
    rush_headerRow += "1st Dn|"
    rush_alignmentRow += ":--|"
    rush_visitorRow += f'{data["gameStats"][v]["rushingFirstDowns"]}|'
    rush_homeRow += f'{data["gameStats"][h]["rushingFirstDowns"]}|'

    # Rushing TD
    rush_headerRow += "TD|"
    rush_alignmentRow += ":--|"
    rush_visitorRow += f'{data["gameStats"][v]["rushingTouchdowns"]}|'
    rush_homeRow += f'{data["gameStats"][h]["rushingTouchdowns"]}|'

    # Rushing Fumbles
    rush_headerRow += "Fumbles|"
    rush_alignmentRow += ":--|"
    rush_visitorRow += f'{data["gameStats"][v]["rushingFumbles"]}|'
    rush_homeRow += f'{data["gameStats"][h]["rushingFumbles"]}|'

    # Kick/punt return table
    kr_headerRow = headerRowTemplate + "Kick/Punt Ret|"
    kr_alignmentRow = alignmentRowTemplate
    kr_visitorRow = visitorRowTemplate
    kr_homeRow = homeRowTemplate

    # Kick returns
    kr_headerRow += "Kick Returns|"
    kr_alignmentRow += ":--|"
    kr_visitorRow += f'{data["gameStats"][v]["kickReturns"]}|'
    kr_homeRow += f'{data["gameStats"][h]["kickReturns"]}|'

    # Kick return fair catches
    kr_headerRow += "KR FC|"
    kr_alignmentRow += ":--|"
    kr_visitorRow += f'{data["gameStats"][v]["kickReturnsFairCatches"]}|'
    kr_homeRow += f'{data["gameStats"][h]["kickReturnsFairCatches"]}|'

    # Kick returns
    kr_headerRow += "KR Yds Tot/Avg/Lng|"
    kr_alignmentRow += ":--|"
    kr_visitorRow += f'{data["gameStats"][v]["kickReturnsYards"]}/{data["gameStats"][v]["kickReturnsAverageYards"]}/{data["gameStats"][v]["kickReturnsLong"]}|'
    kr_homeRow += f'{data["gameStats"][h]["kickReturnsYards"]}/{data["gameStats"][h]["kickReturnsAverageYards"]}/{data["gameStats"][h]["kickReturnsLong"]}|'

    # Kick return TD
    kr_headerRow += "KR TD|"
    kr_alignmentRow += ":--|"
    kr_visitorRow += f'{data["gameStats"][v]["kickReturnsTouchdowns"]}|'
    kr_homeRow += f'{data["gameStats"][h]["kickReturnsTouchdowns"]}|'

    # Punt return yds
    kr_headerRow += "Punt Returns|"
    kr_alignmentRow += ":--|"
    kr_visitorRow += f'{data["gameStats"][v]["puntReturns"]}|'
    kr_homeRow += f'{data["gameStats"][h]["puntReturns"]}|'

    # Punt return fair catches
    kr_headerRow += "PR FC|"
    kr_alignmentRow += ":--|"
    kr_visitorRow += f'{data["gameStats"][v]["puntReturnsFairCatches"]}|'
    kr_homeRow += f'{data["gameStats"][h]["puntReturnsFairCatches"]}|'

    # Punt return yds
    kr_headerRow += "PR Yds Tot/Avg/Lng|"
    kr_alignmentRow += ":--|"
    kr_visitorRow += f'{data["gameStats"][v]["puntReturnsYards"]}/{data["gameStats"][v]["puntReturnsAverageYards"]}/{data["gameStats"][v]["puntReturnsLong"]}|'
    kr_homeRow += f'{data["gameStats"][h]["puntReturnsYards"]}/{data["gameStats"][h]["puntReturnsAverageYards"]}/{data["gameStats"][h]["puntReturnsLong"]}|'

    # Punt return TD
    kr_headerRow += "PR TD|"
    kr_alignmentRow += ":--|"
    kr_visitorRow += f'{data["gameStats"][v]["puntReturnsTouchdowns"]}|'
    kr_homeRow += f'{data["gameStats"][h]["puntReturnsTouchdowns"]}|'
%>\
${'##'} Team Stats

${gen_headerRow}
${gen_alignmentRow}
${gen_visitorRow}
${gen_homeRow}

${pass_headerRow}
${pass_alignmentRow}
${pass_visitorRow}
${pass_homeRow}

${rush_headerRow}
${rush_alignmentRow}
${rush_visitorRow}
${rush_homeRow}

${kr_headerRow}
${kr_alignmentRow}
${kr_visitorRow}
${kr_homeRow}
