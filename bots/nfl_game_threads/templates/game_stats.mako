<%
    from datetime import timedelta

    game = data["todayGames"][data["myGameIndex"]]
    v = data["gameDetails"].get("liveVisitorTeamGameStats", {}).get("teamGameStats")
    h = data["gameDetails"].get("liveHomeTeamGameStats", {}).get("teamGameStats")
    awayTeam = data["myTeam"] if data["homeAway"] == "away" else data["oppTeam"]
    homeTeam = data["myTeam"] if data["homeAway"] == "home" else data["oppTeam"]
    if not (v and h):
        return

    headerRowTemplate = "|"
    alignmentRowTemplate = "|:--|"
    awayRowTemplate = f'|{awayTeam["abbreviation"]}|'
    homeRowTemplate = f'|{homeTeam["abbreviation"]}|'

    # General table
    gen_headerRow = headerRowTemplate + "|"
    gen_alignmentRow = alignmentRowTemplate
    gen_awayRow = awayRowTemplate
    gen_homeRow = homeRowTemplate

    # Time of possession
    gen_headerRow += "Time/Poss|"
    gen_alignmentRow += ":--|"
    gen_awayRow += f'{str(timedelta(seconds=v["timeOfPossSeconds"]))[-5:]}|'
    gen_homeRow += f'{str(timedelta(seconds=h["timeOfPossSeconds"]))[-5:]}|'

    # Total plays
    gen_headerRow += "Plays (Yds)|"
    gen_alignmentRow += ":--|"
    gen_awayRow += f'{v["scrimmagePlays"]} ({v["scrimmageYds"]})|'
    gen_homeRow += f'{h["scrimmagePlays"]} ({h["scrimmageYds"]})|'

    # Third downs
    gen_headerRow += "3rd downs (Conv)|"
    gen_alignmentRow += ":--|"
    gen_awayRow += f'{v["down3rdAttempted"]} ({v["down3rdFdMade"]})|'
    gen_homeRow += f'{h["down3rdAttempted"]} ({h["down3rdFdMade"]})|'

    # Penalties
    gen_headerRow += "Penalties (Yds)|"
    gen_alignmentRow += ":--|"
    gen_awayRow += f'{v["penaltiesTotal"]} ({v["penaltiesYardsPenalized"]})|'
    gen_homeRow += f'{h["penaltiesTotal"]} ({h["penaltiesYardsPenalized"]})|'

    # Turnovers
    gen_headerRow += "Turnovers|"
    gen_alignmentRow += ":--|"
    gen_awayRow += f'{v["fumblesLost"] + v["passingInterceptions"]}|'
    gen_homeRow += f'{h["fumblesLost"] + h["passingInterceptions"]}|'

    # Passing table
    pass_headerRow = headerRowTemplate + "Passing|"
    pass_alignmentRow = alignmentRowTemplate
    pass_awayRow = awayRowTemplate
    pass_homeRow = homeRowTemplate

    # Pass completions/attempts
    pass_headerRow += "Comp/Att|"
    pass_alignmentRow += ":--|"
    pass_awayRow += f'{v["passingCompletions"]}/{v["passingAttempts"]}|'
    pass_homeRow += f'{h["passingCompletions"]}/{h["passingAttempts"]}|'

    # Pass yds
    pass_headerRow += "Yds Tot/Avg|"
    pass_alignmentRow += ":--|"
    pass_awayRow += f'{v["passingNetYards"]}/{v["passingAverageYards"] if v["passingAverageYards"] else 0}|'
    pass_homeRow += f'{h["passingNetYards"]}/{h["passingAverageYards"] if h["passingAverageYards"] else 0}|'

    # Pass 1st downs
    pass_headerRow += "1st Dn|"
    pass_alignmentRow += ":--|"
    pass_awayRow += f'{v["passingFirstDowns"]}|'
    pass_homeRow += f'{h["passingFirstDowns"]}|'

    # Pass TD
    pass_headerRow += "TD|"
    pass_alignmentRow += ":--|"
    pass_awayRow += f'{v["passingTouchdowns"]}|'
    pass_homeRow += f'{h["passingTouchdowns"]}|'

    # Sacked
    pass_headerRow += "Sacked (Yds)|"
    pass_alignmentRow += ":--|"
    pass_awayRow += f'{v["passingSacked"] if v["passingSacked"] else 0} ({v["passingSackedYardsLost"] if v["passingSackedYardsLost"] else "-"})|'
    pass_homeRow += f'{h["passingSacked"] if h["passingSacked"] else 0} ({h["passingSackedYardsLost"] if h["passingSackedYardsLost"] else "-"})|'

    # Interceptions
    pass_headerRow += "Int|"
    pass_alignmentRow += ":--|"
    pass_awayRow += f'{v["passingInterceptions"]}|'
    pass_homeRow += f'{h["passingInterceptions"]}|'

    # Rushing table
    rush_headerRow = headerRowTemplate + "Rushing|"
    rush_alignmentRow = alignmentRowTemplate
    rush_awayRow = awayRowTemplate
    rush_homeRow = homeRowTemplate

    # Rushing attempts
    rush_headerRow += "Att|"
    rush_alignmentRow += ":--|"
    rush_awayRow += f'{v["rushingAttempts"]}|'
    rush_homeRow += f'{h["rushingAttempts"]}|'

    # Rushing yds
    rush_headerRow += "Yds Tot/Avg|"
    rush_alignmentRow += ":--|"
    rush_awayRow += f'{v["rushingYards"]}/{v["rushingAverageYards"] if v["rushingAverageYards"] else 0}|'
    rush_homeRow += f'{h["rushingYards"]}/{h["rushingAverageYards"] if h["rushingAverageYards"] else 0}|'

    # Rushing 1st downs
    rush_headerRow += "1st Dn|"
    rush_alignmentRow += ":--|"
    rush_awayRow += f'{v["rushingFirstDowns"]}|'
    rush_homeRow += f'{h["rushingFirstDowns"]}|'

    # Rushing TD
    rush_headerRow += "TD|"
    rush_alignmentRow += ":--|"
    rush_awayRow += f'{v["rushingTouchdowns"]}|'
    rush_homeRow += f'{h["rushingTouchdowns"]}|'

    # Rushing Fumbles
    rush_headerRow += "Fumbles|"
    rush_alignmentRow += ":--|"
    rush_awayRow += f'{v["rushingFumbles"] if v["rushingFumbles"] else 0}|'
    rush_homeRow += f'{h["rushingFumbles"] if h["rushingFumbles"] else 0}|'

    # Kick/punt return table
    kr_headerRow = headerRowTemplate + "Kick/Punt Ret|"
    kr_alignmentRow = alignmentRowTemplate
    kr_awayRow = awayRowTemplate
    kr_homeRow = homeRowTemplate

    # Kick returns
    kr_headerRow += "Kick Returns|"
    kr_alignmentRow += ":--|"
    kr_awayRow += f'{v["kickReturns"]}|'
    kr_homeRow += f'{h["kickReturns"]}|'

    # Kick return fair catches
    kr_headerRow += "KR FC|"
    kr_alignmentRow += ":--|"
    kr_awayRow += f'{v["kickReturnsFairCatches"]}|'
    kr_homeRow += f'{h["kickReturnsFairCatches"]}|'

    # Kick returns
    kr_headerRow += "KR Yds Tot/Avg/Lng|"
    kr_alignmentRow += ":--|"
    kr_awayRow += f'{v["kickReturnsYards"]}/{v["kickReturnsAverageYards"]}/{v["kickReturnsLong"]}|'
    kr_homeRow += f'{h["kickReturnsYards"]}/{h["kickReturnsAverageYards"]}/{h["kickReturnsLong"]}|'

    # Kick return TD
    kr_headerRow += "KR TD|"
    kr_alignmentRow += ":--|"
    kr_awayRow += f'{v["kickReturnsTouchdowns"]}|'
    kr_homeRow += f'{h["kickReturnsTouchdowns"]}|'

    # Punt return yds
    kr_headerRow += "Punt Returns|"
    kr_alignmentRow += ":--|"
    kr_awayRow += f'{v["puntReturns"]}|'
    kr_homeRow += f'{h["puntReturns"]}|'

    # Punt return fair catches
    kr_headerRow += "PR FC|"
    kr_alignmentRow += ":--|"
    kr_awayRow += f'{v["puntReturnsFairCatches"]}|'
    kr_homeRow += f'{h["puntReturnsFairCatches"]}|'

    # Punt return yds
    kr_headerRow += "PR Yds Tot/Avg/Lng|"
    kr_alignmentRow += ":--|"
    kr_awayRow += f'{v["puntReturnsYards"]}/{v["puntReturnsAverageYards"]}/{v["puntReturnsLong"]}|'
    kr_homeRow += f'{h["puntReturnsYards"]}/{h["puntReturnsAverageYards"]}/{h["puntReturnsLong"]}|'

    # Punt return TD
    kr_headerRow += "PR TD|"
    kr_alignmentRow += ":--|"
    kr_awayRow += f'{v["puntReturnsTouchdowns"]}|'
    kr_homeRow += f'{h["puntReturnsTouchdowns"]}|'
%>\
${'##'} Team Stats

${gen_headerRow}
${gen_alignmentRow}
${gen_awayRow}
${gen_homeRow}

${pass_headerRow}
${pass_alignmentRow}
${pass_awayRow}
${pass_homeRow}

${rush_headerRow}
${rush_alignmentRow}
${rush_awayRow}
${rush_homeRow}

##${kr_headerRow}
##${kr_alignmentRow}
##${kr_awayRow}
##${kr_homeRow}
