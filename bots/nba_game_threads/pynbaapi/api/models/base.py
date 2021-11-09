import logging
from re import sub
from typing import Union

from ...constants import APP_NAME

logger = logging.getLogger(__name__)

model_str_formats = {
    "Available": ": GameID: {game_id}, PT Available: {pt_available}",
    "AvailableSeasons": ".Season: {season_id}",
    "Coaches": ": {coach_name}, ID: {coach_id}",
    "CommonAllPlayers": ": {display_first_last} ({team_abbreviation})",
    "CommonTeamRosterPlayer": ": {player}, ID: {player_id}",
    "ConfStandingsByDay": ": Team: {team}, Conference: {conference}, Date: {standingsdate}",
    "GameHeader": ": {gamecode}, {game_status_text}",
    "LastMeeting": ": {last_game_date_est}, {last_game_visitor_team_name} ({last_game_visitor_team_points}) @ ({last_game_home_team_points}) {last_game_home_team_name}",
    "LineScore": ": {visitor.team_abbreviation} @ {home.team_abbreviation} GameID: {visitor.game_id}",
    "Standings": ": Season: {seasonid}, Conf: {conference}, Div: {division}, Team: {teamname}",
    "TeamLineScore": ": GameID: {game_id}, Team: {team_abbreviation}",
    "SeriesStandings": ": Series Leader: {series_leader}",
    "TeamAwardsChampionships": ": {yearawarded}",
    "TeamAwardsConf": ": {yearawarded}",
    "TeamAwardsDiv": ": {yearawarded}",
    "TeamBackground": ": {city} {nickname} ({abbreviation})",
    "TeamHistory": ": {city} {nickname} {yearfounded}-{yearactivetill}",
    "TeamHOFPlayer": ": {player} ({year})",
    "TeamInfoCommon": ": {team_city} {team_name} ({team_abbreviation})",
    "TeamLeadersBase": ": GameID: {game_id}",
    "TeamLeaders": ": Team: {team_abbreviation}, GameID: {game_id}",
    "TeamRetired": "Number: #{jersey} {player} ({year})",
    "TeamSeasonRanks": ": TeamID: {team_id}, Season: {season_id}",
    "TeamSocialSites": ": {accounttype}",
    "TicketLinks": ": GameID: {game_id}",
    "WinProbability": ": GameID: {game_id}",
}

nested_model_str_formats = {
    "AwayTeam": ": {team_name} ({team_tricode})",
    "BoxScoreSummary": ": {game_code} {game_status_text}",
    "BoxScoreSummaryV3": ": {box_score_summary.game_code} {box_score_summary.game_status_text}",
    "GameDates": ": {game_date}",
    "Games": ": {game_code}, {game_status_text}",
    "HomeTeam": ": {team_name} ({team_tricode})",
    "LeagueSchedule": ": Season: {season_year}",
    "Periods": ": {period}",
    "PlayByPlayV3": ": GameID: {game.game_id}",
    "ScheduleLeagueV2": ": Season: {league_schedule.season_year}",
    "ScoreBoardV3": ": {scoreboard.game_date}",
    "Team": ": {team_name} ({team_tricode})",
}


class APIObject:
    def __init__(
        self,
        attr_keys: list = [],
        attr_vals: list = [],
        object_type: Union[str, None] = None,
    ) -> None:
        self.object_type = object_type
        for i in range(0, len(attr_keys)):
            setattr(self, attr_keys[i].lower(), attr_vals[i])

    def __str__(self) -> str:
        return f"<{APP_NAME}.{self.object_type}{model_str_formats.get(self.object_type, '').format(**self.__dict__)}>"


class NestedAPIObject:
    def __init__(
        self, object_data: Union[list, dict], object_type: Union[str, None] = None
    ) -> None:
        self.object_type = object_type
        for k, v in object_data.items():
            if isinstance(v, list):
                setattr(
                    self,
                    self.camel_to_snake(k),
                    [
                        NestedAPIObject(s, self.capitalize_first_letter(k))
                        if isinstance(s, dict)
                        else s
                        for s in v
                    ],
                )
            else:
                setattr(
                    self,
                    self.camel_to_snake(k),
                    NestedAPIObject(v, self.capitalize_first_letter(k))
                    if isinstance(v, dict)
                    else v,
                )

    def __str__(self) -> str:
        return f"<{APP_NAME}.{self.object_type}{nested_model_str_formats.get(self.object_type, '').format(**self.__dict__)}>"

    @staticmethod
    def camel_to_snake(name: str) -> str:
        # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
        name = sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

    @staticmethod
    def capitalize_first_letter(name: str) -> str:
        return f"{name[0:1].upper()}{name[1:]}"
