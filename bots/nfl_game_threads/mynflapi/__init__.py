"""# nflapi

Python wrapper for NFL API

Created by Todd Roberts

https://pypi.org/project/nflapi

Issues: https://github.com/toddrob99/nflapi/issues

Wiki/Documentation: https://github.com/toddrob99/nflapi/wiki

NOTICE REGARDING API TOKEN: This API wrapper does not facilitate obtaining
an access token, which is required to submit requests to the NFL API. The
author of this API wrapper is not aware of any documented method to obtain
an access token, and will not assist with this. If you do not have a valid
method of obtaining an access token, this API wrapper will be useless.
"""

from datetime import datetime
import logging
import requests
import time

from . import version

__version__ = version.VERSION
API_BASE_URL = "https://api.nfl.com"
OPEN_BRACE = "{"
CLOSE_BRACE = "}"

logger = logging.getLogger("nflapi")

logger.debug(
    f"nflapi v{__version__} - Logging started @ "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M %p')}"
)

ENDPOINTS = {
    "currentWeek": "/v1/currentWeek",
    "games": "/v1/games",
    "teams": "/v1/teams",
    "shield": "/v3/shield",
}

QUERIES = {
    "teams": {
        "bySeason": (
            '?s={open_brace}"$query":{open_brace}"season":'
            "{param_season}{close_brace}{close_brace}"
        ),
        "byId": ("?"),
        "standings": (
            '?s={open_brace}"$query":{open_brace}{param_teamAbbr}"season":'
            '{param_season},"standings":{open_brace}"$query":{open_brace}"week.'
            'seasonType":"{param_seasonType}"{close_brace}{close_brace},"$takeLast":1'
            '{close_brace},"$take":{param_take}{close_brace}'
        ),
        "topOffense": (
            '?s={open_brace}"$query":{open_brace}"season":{param_season}{close_brace},'
            '"$sort":{open_brace}"{param_seasonType}TeamSeasonStats.teamStats.'
            'totalPointScore":1{close_brace}{close_brace}'
        ),
        "topDefense": (
            '?s={open_brace}"$query":{open_brace}"season":{param_season}{close_brace},'
            '"$sort":{open_brace}"{param_seasonType}TeamSeasonStats.opponentStats.'
            'totalPointScore":1{close_brace}{close_brace}'
        ),
    },
    "games": {
        "byWeek": (
            '?s={open_brace}"$query":{open_brace}"week.season":{param_season},'
            '"week.seasonType":"{param_seasonType}","week.week":{param_week}'
            "{close_brace}{close_brace}"
        ),
        "byWeekType": (
            '?s={open_brace}"$query":{open_brace}"week.weekType":"'
            '{param_weekType}"{close_brace},"$take":{param_take},"$skip":'
            "{param_skip}{close_brace}"
        ),
        "byTeam": (
            '?s={open_brace}"$query":{open_brace}"week.season":{param_season},'
            '"$or":[{open_brace}"homeTeam.abbr":"{param_teamAbbr}"{close_brace},'
            '{open_brace}"visitorTeam.abbr":"{param_teamAbbr}"{close_brace}]'
            "{close_brace}{close_brace}"
        ),
        "byMatchup": (
            '?s={open_brace}"$query":{open_brace}"$or":[{open_brace}"visitorTeam.'
            'abbr":"{param_team1}","homeTeam.abbr":"{param_team2}"{close_brace},'
            '{open_brace}"homeTeam.abbr":"{param_team1}","visitorTeam.abbr":"'
            '{param_team2}"{close_brace}]{close_brace},"$sort":{open_brace}"gameTime'
            '":1{close_brace},"$take":{param_take}{close_brace}'
        ),
    },
    "shield": {
        "gameById": (
            "query%7Bviewer%7Bgame(id%3A%22{param_gameId}%22)%7Bid%20networkChannels%20"
            "gameTime%20gsisId%20slug%20awayTeam%7Babbreviation%20fullName%20id%20"
            "nickName%20cityStateRegion%20franchise%7Bid%20slug%20currentLogo%7Burl"
            "%7D%7D%7DhomeTeam%7Babbreviation%20fullName%20id%20nickName%20"
            "cityStateRegion%20division%20conference%20franchise%7Bid%20slug%20"
            "currentLogo%7Burl%7D%7D%7Dweek%7BseasonValue%20id%20seasonType%20"
            "weekValue%20weekType%7DradioLinks%20ticketUrl%20venue%7BfullName%20"
            "city%20state%7DgameDetailId%7D%7D%7D"
        ),
        "gameDetails": (
            "query%7Bviewer%7BgameDetail(id%3A%22{param_gameDetailId}%22)%7Bid%20"
            "attendance%20distance%20down%20gameClock%20goalToGo%20homePointsOvertime"
            "%20homePointsTotal%20homePointsQ1%20homePointsQ2%20homePointsQ3%20"
            "homePointsQ4%20homeTeam%7Babbreviation%20nickName%7DhomeTimeoutsUsed%20"
            "homeTimeoutsRemaining%20period%20phase%20playReview%20possessionTeam%7B"
            "abbreviation%20nickName%7Dredzone%20scoringSummaries%7BplayId%20"
            "playDescription%20patPlayId%20homeScore%20visitorScore%7Dstadium%20"
            "startTime%20visitorPointsOvertime%20visitorPointsOvertimeTotal%20"
            "visitorPointsQ1%20visitorPointsQ2%20visitorPointsQ3%20visitorPointsQ4%20"
            "visitorPointsTotal%20visitorTeam%7Babbreviation%20nickName%7D"
            "visitorTimeoutsUsed%20visitorTimeoutsRemaining%20homePointsOvertimeTotal"
            "%20visitorPointsOvertimeTotal%20possessionTeam%7BnickName%7Dweather%7B"
            "currentFahrenheit%20location%20longDescription%20shortDescription%20"
            "currentRealFeelFahrenheit%7DyardLine%20yardsToGo%20drives%7BquarterStart"
            "%20endTransition%20endYardLine%20endedWithScore%20firstDowns%20"
            "gameClockEnd%20gameClockStart%20howEndedDescription%20"
            "howStartedDescription%20inside20%20orderSequence%20playCount%20playIdEnded"
            "%20playIdStarted%20playSeqEnded%20playSeqStarted%20possessionTeam%7B"
            "abbreviation%20nickName%7DquarterEnd%20realStartTime%20startTransition%20"
            "startYardLine%20timeOfPossession%20yards%20yardsPenalized%7Dplays%7B"
            "clockTime%20down%20driveNetYards%20drivePlayCount%20driveSequenceNumber%20"
            "driveTimeOfPossession%20endClockTime%20endYardLine%20firstDown%20goalToGo"
            "%20nextPlayIsGoalToGo%20nextPlayType%20orderSequence%20penaltyOnPlay%20"
            "playClock%20playDeleted%20playDescription%20"
            "playDescriptionWithJerseyNumbers%20playId%20playReviewStatus%20isBigPlay"
            "%20playType%20playStats%7BstatId%20yards%20team%7Bid%20abbreviation%7D"
            "playerName%20gsisPlayer%7Bid%7D%7DpossessionTeam%7Babbreviation%20nickName"
            "%7DprePlayByPlay%20quarter%20scoringPlay%20scoringPlayType%20scoringTeam"
            "%7Bid%20abbreviation%20nickName%7DshortDescription%20specialTeamsPlay%20"
            "stPlayType%20timeOfDay%20yardLine%20yards%20yardsToGo%20latestPlay%7D%20"
            "liveHomeTeamGameStats%7BteamGameStats%7BpassingAttempts%20"
            "passingCompletions%20passingNetYards%20passingAverageYards%20"
            "passingFirstDowns%20passingFirstDownPercentage%20passingLong%20"
            "passingTouchdowns%20passingTouchdownPercentage%20passingInterceptions%20"
            "passingSacked%20passingSackedYardsLost%20rushingAttempts%20rushingYards%20"
            "rushingAverageYards%20rushingTouchdowns%20rushingFirstDowns%20"
            "rushingFirstDownPercentage%20rushingLong%20rushingFumbles%20"
            "totalPointsScored%20fumblesLost%20scrimmageYds%20scrimmagePlays%20"
            "down3rdAttempted%20down3rdFdMade%20timeOfPossSeconds%20penaltiesTotal%20"
            "penaltiesYardsPenalized%20kickReturns%20kickReturnsFairCatches%20"
            "kickReturnsYards%20kickReturnsAverageYards%20kickReturnsLong%20"
            "kickReturnsTouchdowns%20puntReturns%20puntReturnsYards%20"
            "puntReturnsAverageYards%20puntReturnsFairCatches%20puntReturnsLong%20"
            "puntReturnsTouchdowns%7D%7D%20liveVisitorTeamGameStats%7BteamGameStats%7B"
            "passingAttempts%20passingCompletions%20passingNetYards%20"
            "passingAverageYards%20passingFirstDowns%20passingFirstDownPercentage%20"
            "passingLong%20passingTouchdowns%20passingTouchdownPercentage%20"
            "passingInterceptions%20passingSacked%20passingSackedYardsLost%20"
            "rushingAttempts%20rushingYards%20rushingAverageYards%20rushingTouchdowns"
            "%20rushingFirstDowns%20rushingFirstDownPercentage%20rushingLong%20"
            "rushingFumbles%20totalPointsScored%20fumblesLost%20scrimmageYds%20"
            "scrimmagePlays%20down3rdAttempted%20down3rdFdMade%20timeOfPossSeconds%20"
            "penaltiesTotal%20penaltiesYardsPenalized%20kickReturns%20"
            "kickReturnsFairCatches%20kickReturnsYards%20kickReturnsAverageYards%20"
            "kickReturnsLong%20kickReturnsTouchdowns%20puntReturns%20puntReturnsYards"
            "%20puntReturnsAverageYards%20puntReturnsFairCatches%20puntReturnsLong%20"
            "puntReturnsTouchdowns%7D%7D%7D%7D%7D"
        ),
        "gameInsights": (
            "%7Bviewer%7BgameInsight%7BinsightsByGames(ids%3A%5B{param_gameIds}%5D)%7B"
            "gameId%20headline%20insight%20id%20insightType%20createdDate%20"
            "lastModifiedDate%20items%7Bteam%7BfullName%20nickName%20abbreviation%20id"
            "%20franchise%7Bslug%7D%7Dplayer%7Bid%20position%20esbId%20currentTeam%7B"
            "abbreviation%20nickName%7Dperson%7Bheadshot%7Basset%7Burl%7D%7DfirstName"
            "%20lastName%20displayName%20slug%7D%7Dpicker%20facts%7D%7D%7D%7D%7D"
        ),
        "gameStats": (
            "query%7Bviewer%7Bstats%7BteamGameStats(team_id%3A%22{param_teamId}%22%2C"
            "first%3A100%2Cgame_id%3A%22{param_gameId}%22)%7Bedges%7Bnode%7Bteam%7B"
            "abbreviation%7DteamGameStats%7BpassingAttempts%20passingCompletions%20"
            "passingNetYards%20passingAverageYards%20passingFirstDowns%20"
            "passingFirstDownPercentage%20passingLong%20passingTouchdowns%20"
            "passingTouchdownPercentage%20passingInterceptions%20passingSacked%20"
            "passingSackedYardsLost%20rushingAttempts%20rushingYards%20"
            "rushingAverageYards%20rushingTouchdowns%20rushingFirstDowns%20"
            "rushingFirstDownPercentage%20rushingLong%20rushingFumbles%20"
            "totalPointsScored%20fumblesLost%20scrimmageYds%20scrimmagePlays%20"
            "down3rdAttempted%20down3rdFdMade%20timeOfPossSeconds%20penaltiesTotal"
            "%20penaltiesYardsPenalized%20kickReturns%20kickReturnsFairCatches%20"
            "kickReturnsYards%20kickReturnsAverageYards%20kickReturnsLong%20"
            "kickReturnsTouchdowns%20puntReturns%20puntReturnsYards%20"
            "puntReturnsAverageYards%20puntReturnsFairCatches%20puntReturnsLong%20"
            "puntReturnsTouchdowns%7DopponentGameStats%7BpassingAttempts%20"
            "passingCompletions%20passingNetYards%20passingAverageYards%20"
            "passingFirstDowns%20passingFirstDownPercentage%20passingLong%20"
            "passingTouchdowns%20passingTouchdownPercentage%20passingInterceptions%20"
            "passingSacked%20passingSackedYardsLost%20rushingAttempts%20rushingYards%20"
            "rushingAverageYards%20rushingTouchdowns%20rushingFirstDowns%20"
            "rushingFirstDownPercentage%20rushingLong%20rushingFumbles%20"
            "totalPointsScored%20fumblesLost%20scrimmageYds%20scrimmagePlays%20"
            "down3rdAttempted%20down3rdFdMade%20timeOfPossSeconds%20penaltiesTotal%20"
            "penaltiesYardsPenalized%20kickReturns%20kickReturnsFairCatches%20"
            "kickReturnsYards%20kickReturnsAverageYards%20kickReturnsLong%20"
            "kickReturnsTouchdowns%20puntReturns%20puntReturnsYards%20"
            "puntReturnsAverageYards%20puntReturnsFairCatches%20puntReturnsLong%20"
            "puntReturnsTouchdowns%7D%7D%7D%7D%7D%7D%7D"
        ),
        "teamById": (
            "query%7Bviewer%7Bteam(id%3A%22{param_teamId}%22)%7Bid%20abbreviation%20"
            "fullName%20id%20nickName%20cityStateRegion%20franchise%7Bid%20slug%20"
            "currentLogo%7Burl%7D%7D%20season%7Bid%20season%7D%20division%20players%7B"
            "id%20status%20position%20jerseyNumber%20person%7BfirstName%20lastName%20"
            "displayName%20highSchool%7D%7D%20injuries%7Bid%7D%7D%7D%7D"
        ),
    },
}

DEFAULT_FIELDS = {
    "teams": (
        "{id,season,fullName,nickName,cityStateRegion,abbr,teamType,conference{abbr},"
        "division{abbr},standings{overallWins,overallLosses,overallTies,overallWinPct,"
        "divisionWins,divisionLosses,divisionTies,clinchDivision,"
        "clinchDivisionAndHomefield,clinchWildcard,clinchPlayoff,conferenceRank,"
        "divisionRank}}"
        # "{id,season,fullName,nickName,abbr,teamType,conference{abbr},division{abbr}}"
    ),
    "teamsById": (
        "{id,season,fullName,nickName,abbr,type,cityStateRegion,conference{abbr},"
        "division{abbr},roster{id,type,firstName,lastName,displayName,homeTown,"
        "college{id,name,type},highSchool,activeRole,player,coach},injuries{status,"
        "injuryStatus,practiceStatus,type,person{id,firstName,lastName,displayName,"
        "activeRole,player}}}"
    ),
    "games": (
        "{week{id,season,weekOrder,seasonType,week,weekType,name},id,type,"
        "lastModifiedDate,gameTime,gameStatus{gameClock,down,yardsToGo,yardLineSide,"
        "yardLineNumber,period,scoringPlayType,phase,possessionTeam{abbr}},homeTeam{"
        "id,season,fullName,nickName,cityStateRegion,abbr,teamType,conference{abbr},"
        "division{abbr}},visitorTeam{id,season,fullName,nickName,cityStateRegion,abbr,"
        "teamType,conference{abbr},division{abbr}},homeTeamScore,visitorTeamScore,"
        "networkChannel,venue{id,type,name}}"
    ),
}


class APISession(object):
    def __init__(self, token):
        self.token = token

    def api_call(
        self, endpoint, query="", headers={}, data={}, method="GET"
    ):  # , wait=True):
        headers.update({"Authorization": f"Bearer {self.token['access_token']}"})
        if method == "GET":
            r = requests.get(API_BASE_URL + endpoint + query, headers=headers)
        elif method == "POST":
            r = requests.post(
                API_BASE_URL + endpoint + query, data=data, headers=headers
            )
        if r.status_code not in [200, 201]:
            r.raise_for_status()
        #  elif r.status_code == 429:  # Find status code for too many requests/wait
        #      # if wait:
        #      #     wait(r.json.get("wait_time"))  # Find the wait time in the response
        else:
            return r.json()

    def currentWeek(self):
        return self.api_call(ENDPOINTS["currentWeek"])

    def gamesByWeek(self, season, week, seasonType, fields=DEFAULT_FIELDS["games"]):
        return self.api_call(
            ENDPOINTS["games"],
            query=QUERIES["games"]["byWeek"].format(
                param_season=season,
                param_week=week,
                param_seasonType=seasonType,
                open_brace=OPEN_BRACE,
                close_brace=CLOSE_BRACE,
            )
            + "&fs="
            + fields,
        )

    def gamesByWeekType(
        self, weekType, take=10, skip=0, fields=DEFAULT_FIELDS["games"]
    ):
        return self.api_call(
            ENDPOINTS["games"],
            query=QUERIES["games"]["byWeekType"].format(
                param_weekType=weekType,
                param_take=take,
                param_skip=skip,
                open_brace=OPEN_BRACE,
                close_brace=CLOSE_BRACE,
            )
            + "&fs="
            + fields,
        )

    def gamesByTeam(self, season, teamAbbr, fields=DEFAULT_FIELDS["games"]):
        return self.api_call(
            ENDPOINTS["games"],
            query=QUERIES["games"]["byTeam"].format(
                param_season=season,
                param_teamAbbr=teamAbbr,
                open_brace=OPEN_BRACE,
                close_brace=CLOSE_BRACE,
            )
            + "&fs="
            + fields,
        )

    def gamesByMatchup(
        self, team1Abbr, team2Abbr, take=1, fields=DEFAULT_FIELDS["games"]
    ):
        return self.api_call(
            ENDPOINTS["games"],
            query=QUERIES["games"]["byMatchup"].format(
                param_team1=team1Abbr,
                param_team2=team2Abbr,
                param_take=take,
                open_brace=OPEN_BRACE,
                close_brace=CLOSE_BRACE,
            )
            + "&fs="
            + fields,
        )

    def teams(self, season=None, fields=DEFAULT_FIELDS["teams"]):
        return self.api_call(
            ENDPOINTS["teams"],
            query=QUERIES["teams"]["bySeason"].format(
                param_season=season, open_brace=OPEN_BRACE, close_brace=CLOSE_BRACE
            )
            + "&fs="
            + fields,
        )

    def teamById(self, teamId, fields=DEFAULT_FIELDS["teamsById"]):
        return self.api_call(
            f"{ENDPOINTS['teams']}/{teamId}",
            query=QUERIES["teams"]["byId"].format(
                open_brace=OPEN_BRACE, close_brace=CLOSE_BRACE
            )
            + "&fs="
            + fields,
        )

    def teamById_shield(self, teamId, query=None):
        if not query:
            query = QUERIES["shield"]["teamById"].format(param_teamId=teamId)
        return self.api_call(
            ENDPOINTS["shield"], query=f"?query={query}&variables=null",
        )

    def standings(
        self, season, seasonType, teamAbbr=None, take=40, fields=DEFAULT_FIELDS["teams"]
    ):
        return self.api_call(
            ENDPOINTS["teams"],
            query=QUERIES["teams"]["standings"].format(
                param_season=season,
                param_seasonType=seasonType,
                param_teamAbbr=f'"abbr":"{teamAbbr}",' if teamAbbr else "",
                param_take=take,
                open_brace=OPEN_BRACE,
                close_brace=CLOSE_BRACE,
            )
            + "&fs="
            + fields,
        )

    def teamsByDefensiveRanking(
        self, season, seasonType, fields=None,
    ):
        if not fields:
            fields = (
                "{id,season,fullName,nickName,cityStateRegion,abbr,teamType,"
                "conference{abbr},division{abbr},"
                "{param_seasonType}TeamSeasonStats"
                "{teamStats{teamStat{totalTouchdowns},passing{netYards}"
                ",rushing{yards}}}}".replace("{param_seasonType}", seasonType.lower())
            )
        return self.api_call(
            ENDPOINTS["teams"],
            query=QUERIES["teams"]["topDefense"].format(
                param_season=season,
                param_seasonType=seasonType.lower(),
                open_brace=OPEN_BRACE,
                close_brace=CLOSE_BRACE,
            )
            + "&fs="
            + fields,
        )

    def teamsByOffensiveRanking(
        self, season, seasonType, fields=None,
    ):
        if not fields:
            fields = (
                "{id,season,fullName,nickName,cityStateRegion,abbr,teamType,"
                "conference{abbr},division{abbr},"
                "{param_seasonType}TeamSeasonStats"
                "{teamStats{teamStat{totalTouchdowns},passing{netYards}"
                ",rushing{yards}}}}".replace("{param_seasonType}", seasonType.lower())
            )
        return self.api_call(
            ENDPOINTS["teams"],
            query=QUERIES["teams"]["topOffense"].format(
                param_season=season,
                param_seasonType=seasonType.lower(),
                open_brace=OPEN_BRACE,
                close_brace=CLOSE_BRACE,
            )
            + "&fs="
            + fields,
        )

    def gameById(self, gameId, query=None):
        if not query:
            query = QUERIES["shield"]["gameById"].format(param_gameId=gameId)
        return self.api_call(
            ENDPOINTS["shield"], query=f"?query={query}&variables=null",
        )

    def gameDetails(self, gameDetailId, query=None):
        if not query:
            query = QUERIES["shield"]["gameDetails"].format(
                param_gameDetailId=gameDetailId
            )
        return self.api_call(
            ENDPOINTS["shield"], query=f"?query={query}&variables=null",
        )

    def gameInsights(self, gameId=None, gameIds=None, query=None):
        if isinstance(gameId, str):
            unformattedGameIds = [gameId]
        elif isinstance(gameIds, list):
            unformattedGameIds = gameIds
        else:
            raise ValueError("Either gameId (str) or gameIds (list) must be provided.")
        formattedGameIdList = [f"%22{x}%22" for x in unformattedGameIds]
        formattedGameIds = ",".join(formattedGameIdList)
        if not query:
            query = QUERIES["shield"]["gameInsights"].format(
                param_gameIds=formattedGameIds
            )
        return self.api_call(
            ENDPOINTS["shield"], query=f"?query={query}&variables=null",
        )

    def gameStats(self, gameId, teamId, query=None):
        if not query:
            query = QUERIES["shield"]["gameStats"].format(
                param_gameId=gameId, param_teamId=teamId
            )
        return self.api_call(
            ENDPOINTS["shield"], query=f"?query={query}&variables=null",
        )

    def shieldQuery(self, query):
        return self.api_call(
            ENDPOINTS["shield"], query=f"?query={query}&variables=null",
        )


def wait(seconds):
    time.sleep(seconds)
