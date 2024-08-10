from . import constants

from datetime import datetime, timedelta
import logging
import requests

logger = logging.getLogger(f"{constants.APP_NAME}.api")


class API:
    def __init__(self):
        pass

    def game(self, game_pk, **kwargs):
        url = f"{constants.GAME_ENDPOINT.format(game_pk=game_pk)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json

    def game_boxscore(self, game_pk, **kwargs):
        url = f"{constants.GAME_BOXSCORE_ENDPOINT.format(game_pk=game_pk)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json

    def game_playbyplay(self, game_pk, **kwargs):
        url = f"{constants.GAME_PLAYBYPLAY_ENDPOINT.format(game_pk=game_pk)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json

    def scoreboard(
        self,
        start_date=datetime.today().strftime("%Y-%m-%d"),
        end_date=None,
        team_id=None,
        **kwargs,
    ):
        url = f"{constants.SCOREBOARD_ENDPOINT.format(ymd=start_date)}"
        if not self.check_date_format(start_date):
            raise ValueError(
                "Parameter start_date contains invalid value (format should be %Y-%m-%d e.g. '2021-10-05', or 'now')."
            )
        if end_date and not self.check_date_format(end_date):
            raise ValueError(
                "Parameter end_date contains invalid value (format should be %Y-%m-%d e.g. '2021-10-05', or 'now')."
            )
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            games = json.get("games", [])
            if games and end_date:
                games = [x for x in games if x["gameDate"] <= end_date]
            if games and team_id:
                games = [
                    x
                    for x in games
                    if team_id in [x["awayTeam"]["id"], x["homeTeam"]["id"]]
                ]
            return games

    def season_by_date(self, date_str, **kwargs):
        if not self.check_date_format(date_str):
            raise ValueError(
                "Parameter date_str contains invalid value (format should be %Y-%m-%d e.g. '2021-10-05')."
            )
        all_seasons = self.seasons(**kwargs)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        given_year = date_obj.strftime("%Y")
        relevant_seasons = [x for x in all_seasons if given_year in str(x["id"])]
        in_season = next(
            (
                x
                for x in relevant_seasons
                if date_obj
                >= (
                    datetime.fromisoformat(
                        x.get("preseasonStartdate", x.get("preseasonStartDate"))
                    )
                )
                and date_obj <= datetime.fromisoformat(x["endDate"])
            ),
            None,
        )
        if in_season:
            return in_season
        return (
            relevant_seasons[0]
            if (
                date_obj - datetime.fromisoformat(relevant_seasons[0]["endDate"])
                < (
                    datetime.fromisoformat(
                        relevant_seasons[1].get(
                            "preseasonStartdate",
                            relevant_seasons[1].get("preseasonStartDate"),
                        )
                    )
                )
                - date_obj
            )
            else relevant_seasons[1]
        )

    def season_by_id(self, season_id, **kwargs):
        all_seasons = self.seasons(**kwargs)
        return next(
            (x for x in all_seasons if x["id"] == season_id),
            None,
        )

    def seasons(self, ids=[], **kwargs):
        url = f"{constants.SEASONS_ENDPOINT}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if ids == []:
            return json["data"]
        if isinstance(ids, int) or isinstance(ids, str):
            ids = [str(ids)]
        ids = [str(i) for i in ids]
        seasons = [s for s in json["data"] if s["id"] in ids]
        if json:
            return seasons

    def standings(self, ymd="now", **kwargs):
        if not self.check_date_format(ymd):
            raise ValueError(
                "Parameter ymd contains invalid value (format should be %Y-%m-%d e.g. '2021-10-05', or 'now')."
            )
        url = f"{constants.STANDINGS_ENDPOINT.format(ymd=ymd)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if json:
            return json.get("standings", [])

    def team_by_id(self, team_id):
        return next((x for x in self.teams() if x["id"] == team_id), None)

    def teams(self, ymd="now", ids=[], **kwargs):
        if not self.check_date_format(ymd):
            raise ValueError(
                "Parameter ymd contains invalid value (format should be %Y-%m-%d e.g. '2021-10-05', or 'now')."
            )
        url = f"{constants.TEAMS_ENDPOINT.format(ymd=ymd)}"
        url = self.add_kwargs_to_url(url, kwargs)
        json = self.get_json(url)
        if not json:
            return []
        if ids:
            return [x for x in json["teams"] if x["id"] in ids]
        else:
            return json["teams"]

    def teams_with_conf_div(self, ymd="now", ids=[]):
        all_teams = self.teams(ymd=ymd, ids=ids)
        standings = self.standings()
        if not standings:
            logger.error(
                "No data returned for standings/now. Teams won't have valid division or conference data included!"
            )
            standings = []
        for t in all_teams:
            st = next(
                (x for x in standings if x["teamAbbrev"]["default"] == t["abbrev"]),
                {},
            )
            t.update(
                {
                    "conferenceAbbrev": st.get("conferenceAbbrev", "U"),
                    "conferenceName": st.get("conferenceName", "Unknown"),
                    "divisionAbbrev": st.get("divisionAbbrev", "U"),
                    "divisionName": st.get("divisionName", "Unknown"),
                }
            )

        return all_teams

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
        if d == "now":
            return True
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
