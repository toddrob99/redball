from datetime import datetime
import logging

from .constants import APP_NAME, API_URL
from .api.api import API
from .api.models.base import NestedAPIObject
from typing import Union

from .__version__ import __version__

logger = logging.Logger(__name__)


class NBA:
    def __init__(
        self,
        api_user_agent: str = f"{APP_NAME}/{__version__}",
        api_url: str = API_URL,
        api_referer: str = API_URL,
    ) -> None:
        self.__version__ = __version__
        self.api = API(api_url, api_user_agent, api_referer)

        # Create endpoint aliases
        self.scoreboardv2 = self.api.scoreboardv2
        self.team_history = self.api.teamdetails
        self.team = self.api.teaminfocommon
        self.team_roster = self.api.commonteamroster
        self.standings = self.api.leaguestandings
        self.all_players = self.api.commonallplayers
        self.play_by_play = self.api.playbyplayv3
        self.scoreboard = self.api.scoreboardv3
        self.schedule = self.api.scheduleleaguev2
        self.boxscore_summary = self.api.boxscoresummaryv3
        self.boxscore_traditional = self.api.boxscoretraditionalv3

    def find_team(
        self, search_keyword: str, season: str = datetime.now().strftime("%Y")
    ) -> list[NestedAPIObject]:
        # There is no endpoint to look up a team without team id
        # so get full schedule, extract all teams, and search that
        all_teams = self.all_teams(season)
        lookup_by_abbr = [
            x for x in all_teams if search_keyword.lower() in x.team_tricode.lower()
        ]
        if len(lookup_by_abbr):
            return lookup_by_abbr
        lookup_by_name = [
            x for x in all_teams if search_keyword.lower() in x.team_name.lower()
        ]
        if len(lookup_by_name):
            return lookup_by_name
        lookup_by_city = [
            x for x in all_teams if search_keyword.lower() in x.team_city.lower()
        ]
        if len(lookup_by_city):
            return lookup_by_city

        return []

    def all_teams(
        self,
        season: str = datetime.now().strftime("%Y"),
        force_refresh: bool = False,
    ) -> list[NestedAPIObject]:
        if not force_refresh and hasattr(self, "_all_teams_cache"):
            # Use cached data since this data should not change
            return self._all_teams_cache
        # There is no endpoint to look up all teams,
        # so get full schedule for the season and extract.
        sched = self.schedule(season)
        teams = []
        for d in sched.league_schedule.game_dates:
            for g in d.games:
                if not next(
                    (x for x in teams if x.team_id == g.away_team.team_id), False
                ):
                    delattr(g.away_team, "losses")
                    delattr(g.away_team, "score")
                    delattr(g.away_team, "seed")
                    delattr(g.away_team, "wins")
                    g.away_team.object_type = "Team"
                    teams.append(g.away_team)
                if not next(
                    (x for x in teams if x.team_id == g.home_team.team_id), False
                ):
                    delattr(g.home_team, "losses")
                    delattr(g.home_team, "score")
                    delattr(g.home_team, "seed")
                    delattr(g.home_team, "wins")
                    g.home_team.object_type = "Team"
                    teams.append(g.home_team)

        setattr(self, "_all_teams_cache", teams)
        return self._all_teams_cache

    def next_game(
        self,
        team_id: int,
        season: str = datetime.now().strftime("%Y"),
        after_datetime: datetime = datetime.now(),
    ) -> Union[NestedAPIObject, None]:
        sched = self.schedule(season)
        game_date_gen = (
            x
            for x in sched.league_schedule.game_dates
            if datetime.strptime(x.game_date, "%m/%d/%Y %H:%M:%S %p")
            >= after_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        )
        for d in game_date_gen:
            if next_game := next(
                (
                    g
                    for g in d.games
                    if team_id in [g.away_team.team_id, g.home_team.team_id]
                    and g.game_status == 1
                    and "PPD" not in g.game_status_text
                ),
                None,
            ):
                return next_game
        return None
