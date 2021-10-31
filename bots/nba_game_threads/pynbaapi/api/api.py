from datetime import datetime
import logging
import requests
from typing import Union
from uuid import uuid4

from .. import constants
from .endpoints.commonallplayers import CommonAllPlayers
from .endpoints.commonteamroster import CommonTeamRoster
from .endpoints.leaguestandings import LeagueStandings
from .endpoints.scoreboardv2 import ScoreboardV2
from .endpoints.teamdetails import TeamDetails
from .endpoints.teaminfocommon import TeamInfoCommon
from .models.base import NestedAPIObject

logger = logging.getLogger(__name__)


class API:
    def __init__(
        self,
        api_url: str = constants.API_URL,
        user_agent: str = None,
        referer: str = constants.API_URL,
    ):
        self.api_url = api_url
        self.user_agent = user_agent
        self.referer = referer

    def boxscoresummaryv3(
        self,
        game_id: str,
        **kwargs,
    ) -> NestedAPIObject:
        endpoint = constants.API_BOXSCORESUMMARYV3_ENDPOINT.format(
            game_id=game_id
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        return self.from_url(url, "BoxScoreSummaryV3")

    def boxscoretraditionalv3(
        self,
        game_id: str,
        start_period: int = 0,
        end_period: int = 14,
        start_range: int = 0,
        end_range: int = 99,
        range_type: int = 1,
        **kwargs,
    ) -> NestedAPIObject:
        endpoint = constants.API_BOXSCORETRADITIONALV3_ENDPOINT.format(
            game_id=game_id,
            start_period=start_period,
            end_period=end_period,
            start_range=start_range,
            end_range=end_range,
            range_type=range_type,
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        return self.from_url(url, "BoxScoreTraditionalV3")

    def commonallplayers(
        self,
        season: str = datetime.today().strftime("%Y"),
        league_id: str = "00",
        current_season_only: bool = True,
        **kwargs,
    ) -> CommonAllPlayers:
        # Retrieve/parse data from API and return CommonTeamRoster object
        endpoint = constants.API_COMMONALLPLAYERS_ENDPOINT.format(
            league_id=league_id,
            season=season,
            current_season_only=1 if current_season_only else 0,
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        api_response = self.get_json(url)

        # Create endpoint object to parse api response
        return_obj = CommonAllPlayers(api_response)

        return return_obj

    def commonteamroster(
        self,
        team_id: int,
        season: str = "",
        league_id: str = "00",
        **kwargs,
    ) -> CommonTeamRoster:
        # Retrieve/parse data from API and return CommonTeamRoster object
        endpoint = constants.API_COMMONTEAMROSTER_ENDPOINT.format(
            league_id=league_id, season=season, team_id=team_id
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        api_response = self.get_json(url)

        # Create endpoint object to parse api response
        return_obj = CommonTeamRoster(api_response)

        return return_obj

    def leaguestandings(
        self,
        season: str = datetime.today().strftime("%Y"),
        season_type: str = "Regular Season",
        league_id: str = "00",
        **kwargs,
    ) -> LeagueStandings:
        # Retrieve/parse data from API and return CommonTeamRoster object
        endpoint = constants.API_LEAGUESTANDINGSV3_ENDPOINT.format(
            league_id=league_id, season=season, season_type=season_type
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        api_response = self.get_json(url)

        # Create endpoint object to parse api response
        return_obj = LeagueStandings(api_response)

        return return_obj

    def playbyplayv3(
        self,
        game_id: str,
        start_period: int = 0,
        end_period: int = 14,
        **kwargs,
    ) -> NestedAPIObject:
        endpoint = constants.API_PLAYBYPLAYV3_ENDPOINT.format(
            game_id=game_id, start_period=start_period, end_period=end_period
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        return self.from_url(url, "PlayByPlayV3")

    def scheduleleaguev2(
        self,
        season: str = datetime.today().strftime("%Y"),
        league_id: str = "",
        team_id: Union[int, None] = None,
        **kwargs,
    ) -> NestedAPIObject:
        endpoint = constants.API_SCHEDULELEAGUEV2_ENDPOINT.format(
            season=season, league_id=league_id
        )
        url = f"{self.api_url}{endpoint}"
        url += f"&TeamID={team_id}" if team_id else ""
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        return self.from_url(url, "ScheduleLeagueV2")

    def scoreboardv2(
        self,
        game_date: str = datetime.today().strftime("%Y-%m-%d"),
        league_id: str = "00",
        day_offset: Union[int, str] = 0,
        **kwargs,
    ) -> ScoreboardV2:
        # Retrieve/parse data from API and return ScoreboardV2 object
        if not self.check_date_format(game_date):
            raise ValueError(
                "Parameter game_date contains invalid value (format should be %Y-%m-%d e.g. '2021-10-23')."
            )
        endpoint = constants.API_SCOREBOARDV2_ENDPOINT.format(
            game_date=game_date, league_id=league_id, day_offset=day_offset
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        api_response = self.get_json(url)

        # Create endpoint object to parse api response
        scoreboardv2_obj = ScoreboardV2(api_response)

        return scoreboardv2_obj

    def scoreboardv3(
        self,
        game_date: str = datetime.today().strftime("%Y-%m-%d"),
        league_id: str = "00",
        day_offset: Union[int, str] = 0,
        **kwargs,
    ) -> NestedAPIObject:
        # Retrieve/parse data from API and return ScoreBoardV3 object
        if not self.check_date_format(game_date):
            raise ValueError(
                "Parameter game_date contains invalid value (format should be %Y-%m-%d e.g. '2021-10-23')."
            )
        endpoint = constants.API_SCOREBOARDV3_ENDPOINT.format(
            game_date=game_date, league_id=league_id, day_offset=day_offset
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        return self.from_url(url, "ScoreBoardV3")

    def teamdetails(self, team_id: int, **kwargs) -> TeamDetails:
        # Retrieve/parse data from API and return TeamDetails object
        endpoint = constants.API_TEAMDETAILS_ENDPOINT.format(team_id=team_id)
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        api_response = self.get_json(url)

        # Create endpoint object to parse api response
        teamdetails_obj = TeamDetails(api_response)

        return teamdetails_obj

    def teaminfocommon(
        self,
        team_id: int,
        league_id: str = "00",
        season: str = "",
        season_type: str = "",
        **kwargs,
    ) -> TeamInfoCommon:
        # Retrieve/parse data from API and return TeamInfo object
        endpoint = constants.API_TEAMINFOCOMMON_ENDPOINT.format(
            league_id=league_id, season=season, season_type=season_type, team_id=team_id
        )
        url = f"{self.api_url}{endpoint}"
        url = self.add_kwargs_to_url(url, kwargs)
        logger.debug(f"Generated API URL: {url}")

        api_response = self.get_json(url)

        # Create endpoint object to parse api response
        teaminfo_obj = TeamInfoCommon(api_response)

        return teaminfo_obj

    def from_url(self, url: str, endpoint_name: str = "Custom") -> NestedAPIObject:
        api_response = self.get_json(url)
        return_obj = NestedAPIObject(api_response, endpoint_name)
        return return_obj

    def get_json(self, url: str, timeout: int = 30) -> dict:
        h = {
            "User-Agent": self.user_agent + f" {uuid4().hex[:8]}/1.0.0",
            "Referer": self.referer,
        }
        logger.debug(f"Requesting URL: {url} with headers: {h}")
        r = requests.get(url, headers=h, timeout=timeout)
        if r.status_code not in [200, 201]:
            r.raise_for_status()
        else:
            return r.json()

    @staticmethod
    def add_kwargs_to_url(url: str, kwargs: Union[dict, None] = None) -> str:
        if not kwargs or not len(kwargs):
            return url
        for k, v in kwargs.items():
            sep = "?" if url.find("?") == -1 else "&"
            url += f"{sep}{k}={v}"
        return url

    @staticmethod
    def check_date_format(d: str, f: str = "%Y-%m-%d") -> bool:
        try:
            datetime.strptime(d, f)
        except ValueError:
            return False
        return True
