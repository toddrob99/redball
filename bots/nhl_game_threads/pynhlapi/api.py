from . import constants

from datetime import datetime, timedelta
import logging
import requests

logger = logging.getLogger(f"{constants.APP_NAME}.api")


class API:
    def __init__(self, api_url=constants.API_URL):
        self.api_url = api_url
        logger.debug(f"Set API URL to {self.api_url}")

    def game(self, game_pk, json=True, **kwargs):
        url = f"{self.api_url}{constants.GAME_ENDPOINT.format(game_pk=game_pk)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json

    def game_content(self, game_pk, json=True, **kwargs):
        url = f"{self.api_url}{constants.GAME_CONTENT_ENDPOINT.format(game_pk=game_pk)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json

    def schedule(
        self,
        start_date=datetime.today().strftime("%Y-%m-%d"),
        end_date=None,
        team_id=None,
        json=True,
        **kwargs,
    ):
        url = f"{self.api_url}{constants.SCHEDULE_ENDPOINT}"
        if not self.check_date_format(start_date):
            raise ValueError(
                "Parameter start_date contains invalid value (format should be %Y-%m-%d e.g. '2021-10-05')."
            )
        if end_date and not self.check_date_format(end_date):
            raise ValueError(
                "Parameter end_date contains invalid value (format should be %Y-%m-%d e.g. '2021-10-05')."
            )
        url += f"?startDate={start_date}&endDate={end_date if end_date else start_date}"
        url += f"&teamId={team_id}" if team_id else ""
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json

    def season_by_date(
        self, date_str, pre_season_allowance_days=30, json=True, **kwargs
    ):
        if not self.check_date_format(date_str):
            raise ValueError(
                "Parameter date_str contains invalid value (format should be %Y-%m-%d e.g. '2021-10-05')."
            )
        all_seasons = self.seasons(ids=[], **kwargs)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        given_year = date_obj.strftime("%Y")
        relevant_seasons = [x for x in all_seasons if given_year in str(x["seasonId"])]
        in_season = next(
            (
                x
                for x in relevant_seasons
                if date_obj
                >= (
                    datetime.strptime(x["regularSeasonStartDate"], "%Y-%m-%d")
                    - timedelta(days=pre_season_allowance_days)
                )
                and date_obj <= datetime.strptime(x["seasonEndDate"], "%Y-%m-%d")
            ),
            None,
        )
        if in_season:
            return in_season
        return (
            relevant_seasons[0]
            if (
                date_obj
                - datetime.strptime(relevant_seasons[0]["seasonEndDate"], "%Y-%m-%d")
                < (
                    datetime.strptime(
                        relevant_seasons[1]["regularSeasonStartDate"], "%Y-%m-%d"
                    )
                    - timedelta(days=pre_season_allowance_days)
                )
                - date_obj
            )
            else relevant_seasons[1]
        )

    def season_by_id(self, season_id, json=True, **kwargs):
        url = f"{self.api_url}{constants.SEASON_ENDPOINT.format(season_id=season_id)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json.get("seasons", [])[0]

    def seasons(self, ids=[], json=True, **kwargs):
        url = f"{self.api_url}{constants.SEASONS_ENDPOINT}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if ids == []:
            return json["seasons"]
        if isinstance(ids, int) or isinstance(ids, str):
            ids = [str(ids)]
        ids = [str(i) for i in ids]
        seasons = [s for s in json["seasons"] if s["seasonId"] in ids]
        if json:
            return seasons

    def standings(self, season=None, **kwargs):
        url = f"{self.api_url}{constants.STANDINGS_ENDPOINT}"
        if season:
            url += f"?season={season}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json.get("records", [])

    def team_by_id(self, team_id, json=True, **kwargs):
        url = f"{self.api_url}{constants.TEAM_ENDPOINT.format(team_id=team_id)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json.get("teams", [])[0]

    def teams(self, ids=[], json=True, **kwargs):
        if isinstance(ids, list):
            ids = ",".join([str(id) for id in ids])
        elif isinstance(ids, int):
            ids = str(ids)
        url = f"{self.api_url}{constants.TEAMS_ENDPOINT}"
        if len(ids):
            url += f"?teamId={ids}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json["teams"]

    @staticmethod
    def add_kwargs_to_url(url, kwargs=None):
        if not kwargs or not len(kwargs):
            return url
        for k, v in kwargs.items():
            sep = "?" if url.find("?") == -1 else "&"
            url += f"{sep}{k}={v}"
        return url

    @staticmethod
    def check_date_format(d):
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except ValueError:
            return False
        return True

    @staticmethod
    def get_json(url):
        logger.debug(f"Requesting URL: {url}")
        r = requests.get(url)
        if r.status_code not in [200, 201]:
            r.raise_for_status()
        else:
            return r.json()
