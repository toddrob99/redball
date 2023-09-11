"""# nflapi

Python wrapper for NFL API

Created by Todd Roberts

Issues: https://github.com/toddrob99/mynflapi/issues

Wiki/Documentation: https://github.com/toddrob99/mynflapi/wiki

NOTICE REGARDING API TOKEN: This API wrapper does not facilitate obtaining
an access token, which is required to submit requests to the NFL API. The
author of this API wrapper is not aware of any documented method to obtain
an access token, and will not assist with this. If you do not have a valid
method of obtaining an access token, this API wrapper will be useless.
"""

from datetime import datetime
from json import dumps
import logging
import requests
from urllib.parse import unquote

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
    "games": "/football/v2/games",
    "teams": "/football/v2/teams/history",
    "standings": "/football/v2/standings",
    "shield": "/v3/shield",
    "football": "/football/v2",
    "experience": "/experience/v1",
}

QUERIES = {
    "shield": {
        "currentWeek": (
            "query%7Bviewer%7Bleague%7Bcurrent%7Bweek%7BdateBegin%20dateEnd%20"
            "seasonValue%20seasonType%20weekOrder%20weekType%20weekValue%7D%7D%7D%7D%7D"
        ),
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
            "visitorPointsQ1%20visitorPointsQ2%20visitorPointsQ3%20visitorPointsQ4"
            "%20visitorPointsTotal%20visitorTeam%7Babbreviation%20nickName%7D"
            "visitorTimeoutsUsed%20visitorTimeoutsRemaining%20homePointsOvertimeTotal"
            "%20visitorPointsOvertimeTotal%20possessionTeam%7BnickName%7Dweather%7B"
            "currentFahrenheit%20location%20longDescription%20shortDescription%20"
            "currentRealFeelFahrenheit%7DyardLine%20yardsToGo%20drives%7BquarterStart"
            "%20endTransition%20endYardLine%20endedWithScore%20firstDowns%20gameClockEnd"
            "%20gameClockStart%20howEndedDescription%20howStartedDescription%20inside20"
            "%20orderSequence%20playCount%20playIdEnded%20playIdStarted%20playSeqEnded"
            "%20playSeqStarted%20possessionTeam%7Babbreviation%20nickName%7DquarterEnd"
            "%20realStartTime%20startTransition%20startYardLine%20timeOfPossession%20"
            "yards%20yardsPenalized%7Dplays%7BclockTime%20down%20driveNetYards%20"
            "drivePlayCount%20driveSequenceNumber%20driveTimeOfPossession%20endClockTime"
            "%20endYardLine%20firstDown%20goalToGo%20nextPlayIsGoalToGo%20nextPlayType"
            "%20orderSequence%20penaltyOnPlay%20playClock%20playDeleted%20"
            "playDescription%20playDescriptionWithJerseyNumbers%20playId%20"
            "playReviewStatus%20isBigPlay%20playType%20playStats%7BstatId%20yards%20team"
            "%7Bid%20abbreviation%7DplayerName%20gsisPlayer%7Bid%7D%7DpossessionTeam%7B"
            "abbreviation%20nickName%7DprePlayByPlay%20quarter%20scoringPlay%20"
            "scoringPlayType%20scoringTeam%7Bid%20abbreviation%20nickName%7D"
            "shortDescription%20specialTeamsPlay%20stPlayType%20timeOfDay%20yardLine%20"
            "yards%20yardsToGo%20latestPlay%7D%20liveHomeTeamGameStats%7BteamGameStats%7B"
            "passingAttempts%20passingCompletions%20passingNetYards%20passingAverageYards"
            "%20passingFirstDowns%20passingFirstDownPercentage%20passingLong%20"
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
            "kickReturnsLong%20kickReturnsTouchdowns%20puntReturns%20puntReturnsYards%20"
            "puntReturnsAverageYards%20puntReturnsFairCatches%20puntReturnsLong%20"
            "puntReturnsTouchdowns%7D%7D%20homeLiveGameRoster%7Bposition%20jerseyNumber"
            "%20lastName%20firstName%20status%7D%20visitorLiveGameRoster%7Bposition%20"
            "jerseyNumber%20lastName%20firstName%20status%7D%7D%7D%7D"
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
        "teamRoster": (
            "query%7Bviewer%7Bclubs%7BcurrentClubRoster(propertyId%3A%20%22"
            "{param_propertyId}%22)%20%7Bcollege%20displayName%20firstName%20height%20"
            "jerseyNumber%20lastName%20nflExperience%20person%7BcollegeName%20"
            "displayName%20highSchool%20id%20nickName%20status%20summary%7D%20"
            "personId%20position%20status%20weight%7D%7D%7D%7D"
        ),
    },
}


class APISession(object):
    def __init__(self, token):
        self.token = token

    def api_call(self, endpoint, query="", headers={}, data={}, method="GET"):
        headers.update({"Authorization": f"Bearer {self.token['access_token']}"})
        if method == "GET":
            r = requests.get(API_BASE_URL + endpoint + query, headers=headers)
        elif method == "POST":
            r = requests.post(
                API_BASE_URL + endpoint + query, data=data, headers=headers
            )
        if r.status_code not in [200, 201]:
            r.raise_for_status()
        else:
            return r.json()

    def shieldQuery(self, query, variables=None, attempts=1):
        success = False
        while not success and attempts >= 1:
            result = self.api_call(
                ENDPOINTS["shield"],
                data=dumps(
                    {
                        "query": unquote(query),
                        "variables": variables or "null",
                    }
                ),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            logger.debug(f"Shield query result: {result}")
            if not result.get("code"):
                success = True
            else:
                attempts -= 1

        return result

    def currentWeek(self, query=None):
        return self.shieldQuery(query or QUERIES["shield"]["currentWeek"])

    def weekByDate(self, date):
        return self.api_call(f"{ENDPOINTS['football']}/weeks/date/{date}")

    def gamesByWeek(self, season, week, seasonType, limit=100):
        return self.api_call(
            f"{ENDPOINTS['games']}/season/{season}/seasonType/{seasonType}/week/{week}",
            query=f"?withExternalIds=true&limit={limit}",
        )

    def gameById(self, gameId):
        return self.api_call(
            f"{ENDPOINTS['games']}/{gameId}", query="?withExternalIds=true"
        )

    def teams(self, season, limit=100):
        return self.api_call(
            ENDPOINTS["teams"], query=f"?season={season}&limit={limit}"
        )

    def teamById(self, teamId, season=None):
        # There is an endpoint to query a team by id, but it returns hardly any info
        # So retrieve all teams and extract the one we want
        if not season:
            current_year = datetime.now().strftime("%Y")
            season = (
                current_year
                if int(datetime.now().strftime("%m")) >= 4
                else int(current_year) - 1
            )
        teams = self.teams(season)
        return next((x for x in teams["teams"] if x["id"] == teamId), None)

    def teamById_shield(self, teamId, query=None):
        if not query:
            query = QUERIES["shield"]["teamById"].format(param_teamId=teamId)
        return self.api_call(
            ENDPOINTS["shield"],
            query=f"?query={query}&variables=null",
        )

    def team_roster(self, propertyId, query=None):
        if not query:
            query = QUERIES["shield"]["teamRoster"].format(param_propertyId=propertyId)
        return self.api_call(
            ENDPOINTS["shield"],
            query=f"?query={query}&variables=null",
        )

    def standings(self, season, seasonType, week, limit=100):
        return self.api_call(
            ENDPOINTS["standings"],
            query=f"?season={season}&seasonType={seasonType}&week={week}&limit={limit}",
        )

    def gameById_shield(self, gameId, query=None):
        if not query:
            query = QUERIES["shield"]["gameById"].format(param_gameId=gameId)
        return self.api_call(
            ENDPOINTS["shield"],
            query=f"?query={query}&variables=null",
        )

    def gameDetails_shield(self, gameDetailId, query=None):
        if not query:
            query = QUERIES["shield"]["gameDetails"].format(
                param_gameDetailId=gameDetailId
            )
        return self.shieldQuery(query)

    def gameDetails(self, gameId):
        return self.api_call(f"{ENDPOINTS['experience']}/gamedetails/{gameId}")

    def gameSummaryById(self, gameId):
        return self.api_call(
            f"{ENDPOINTS['football']}/stats/live/game-summaries/{gameId}"
        )

    def gameSummariesByWeek(self, season, seasonType, week):
        return self.api_call(
            f"{ENDPOINTS['football']}/stats/live/game-summaries",
            query=f"?season={season}&seasonType={seasonType}&week={week}",
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
            ENDPOINTS["shield"],
            query=f"?query={query}&variables=null",
        )

    def gameStats(self, gameId, teamId, query=None):
        if not query:
            query = QUERIES["shield"]["gameStats"].format(
                param_gameId=gameId, param_teamId=teamId
            )
        return self.api_call(
            ENDPOINTS["shield"],
            query=f"?query={query}&variables=null",
        )
