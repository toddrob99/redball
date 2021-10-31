import logging

from ...constants import APP_NAME
from ..models.base import APIObject
from .base import APIEndpoint

logger = logging.getLogger(__name__)


class ScoreboardV2(APIEndpoint):
    def __str__(self) -> str:
        return f"<{APP_NAME}.ScoreboardV2: {self.api_parameters['GameDate']}, {len(self.games)} Game(s)>"

    def _parse_api_response(self, api_response: dict) -> None:
        self.games = []
        # Parse GameHeader result set
        if game_header_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "GameHeader"
            ),
            None,
        ):
            # Parse the game header result set
            for x in game_header_result_set["rowSet"]:
                g = APIObject(
                    attr_keys=game_header_result_set["headers"],
                    attr_vals=x,
                    object_type=game_header_result_set["name"],
                )

                # Parse LineScore result set
                setattr(g, "linescore", APIObject(object_type="LineScore"))
                if linescore_result_set := next(
                    (
                        y
                        for y in self.api_response.get("resultSets", [])
                        if y["name"] == "LineScore"
                    ),
                    None,
                ):
                    ls_visitor = ls_home = None
                    linescore_rows = [
                        row
                        for row in linescore_result_set["rowSet"]
                        if row[linescore_result_set["headers"].index("GAME_ID")]
                        == g.game_id
                    ]
                    for ls_item in linescore_rows:
                        if (
                            ls_item[linescore_result_set["headers"].index("TEAM_ID")]
                            == x[
                                game_header_result_set["headers"].index(
                                    "VISITOR_TEAM_ID"
                                )
                            ]
                        ):
                            ls_visitor = ls_item
                        else:
                            ls_home = ls_item
                    setattr(
                        g.linescore,
                        "visitor",
                        APIObject(
                            attr_keys=linescore_result_set["headers"],
                            attr_vals=ls_visitor,
                            object_type="TeamLineScore",
                        ),
                    )
                    setattr(
                        g.linescore,
                        "home",
                        APIObject(
                            attr_keys=linescore_result_set["headers"],
                            attr_vals=ls_home,
                            object_type="TeamLineScore",
                        ),
                    )
                else:
                    setattr(g.linescore, "visitor", None)
                    setattr(g.linescore, "home", None)

                # Parse SeriesStandings
                if series_standings_result_set := next(
                    (
                        y
                        for y in self.api_response.get("resultSets", [])
                        if y["name"] == "SeriesStandings"
                    ),
                    None,
                ):
                    if series_standings := next(
                        (
                            row
                            for row in series_standings_result_set["rowSet"]
                            if row[
                                series_standings_result_set["headers"].index("GAME_ID")
                            ]
                            == g.game_id
                        ),
                        None,
                    ):
                        g.series_standings = APIObject(
                            attr_keys=series_standings_result_set["headers"],
                            attr_vals=series_standings,
                            object_type=series_standings_result_set["name"],
                        )
                    else:
                        g.series_standings = None
                else:
                    g.series_standings = None

                # Parse LastMeeting
                if last_meeting_result_set := next(
                    (
                        y
                        for y in self.api_response.get("resultSets", [])
                        if y["name"] == "LastMeeting"
                    ),
                    None,
                ):
                    if last_meeting := next(
                        (
                            row
                            for row in last_meeting_result_set["rowSet"]
                            if row[last_meeting_result_set["headers"].index("GAME_ID")]
                            == g.game_id
                        ),
                        None,
                    ):
                        g.last_meeting = APIObject(
                            attr_keys=last_meeting_result_set["headers"],
                            attr_vals=last_meeting,
                            object_type=last_meeting_result_set["name"],
                        )
                    else:
                        g.last_meeting = None
                else:
                    g.last_meeting = None

                # Parse Available
                if available_result_set := next(
                    (
                        y
                        for y in self.api_response.get("resultSets", [])
                        if y["name"] == "Available"
                    ),
                    None,
                ):
                    if available := next(
                        (
                            row
                            for row in available_result_set["rowSet"]
                            if row[available_result_set["headers"].index("GAME_ID")]
                            == g.game_id
                        ),
                        None,
                    ):
                        g.available = APIObject(
                            attr_keys=available_result_set["headers"],
                            attr_vals=available,
                            object_type=available_result_set["name"],
                        )
                    else:
                        g.available = None
                else:
                    g.available = None

                # Parse TeamLeaders
                g.team_leaders = APIObject(
                    attr_keys=["GAME_ID"],
                    attr_vals=[g.game_id],
                    object_type="TeamLeadersBase",
                )
                if team_leaders_result_set := next(
                    (
                        y
                        for y in self.api_response.get("resultSets", [])
                        if y["name"] == "TeamLeaders"
                    ),
                    None,
                ):
                    tl_visitor = tl_home = None
                    team_leaders_rows = [
                        row
                        for row in team_leaders_result_set["rowSet"]
                        if row[team_leaders_result_set["headers"].index("GAME_ID")]
                        == g.game_id
                    ]
                    for tl_item in team_leaders_rows:
                        if (
                            tl_item[team_leaders_result_set["headers"].index("TEAM_ID")]
                            == x[
                                game_header_result_set["headers"].index(
                                    "VISITOR_TEAM_ID"
                                )
                            ]
                        ):
                            tl_visitor = tl_item
                        else:
                            tl_home = tl_item
                    setattr(
                        g.team_leaders,
                        "visitor",
                        APIObject(
                            attr_keys=team_leaders_result_set["headers"],
                            attr_vals=tl_visitor,
                            object_type=team_leaders_result_set["name"],
                        ),
                    )
                    setattr(
                        g.team_leaders,
                        "home",
                        APIObject(
                            attr_keys=team_leaders_result_set["headers"],
                            attr_vals=tl_home,
                            object_type=team_leaders_result_set["name"],
                        ),
                    )
                else:
                    setattr(g.team_leaders, "visitor", None)
                    setattr(g.team_leaders, "home", None)

                # Parse TicketLinks
                # TODO: Validate with live data
                if ticket_links_result_set := next(
                    (
                        y
                        for y in self.api_response.get("resultSets", [])
                        if y["name"] == "TicketLinks"
                    ),
                    None,
                ):
                    if ticket_links := next(
                        (
                            row
                            for row in ticket_links_result_set["rowSet"]
                            if row[ticket_links_result_set["headers"].index("GAME_ID")]
                            == g.game_id
                        ),
                        None,
                    ):
                        g.ticket_links = APIObject(
                            attr_keys=ticket_links_result_set["headers"],
                            attr_vals=ticket_links,
                            object_type=ticket_links_result_set["name"],
                        )
                    else:
                        g.ticket_links = None
                else:
                    g.ticket_links = None

                # Parse WinProbability
                # TODO: Validate with live data, listed per team like linescore?
                if win_probability_result_set := next(
                    (
                        y
                        for y in self.api_response.get("resultSets", [])
                        if y["name"] == "WinProbability"
                    ),
                    None,
                ):
                    if win_probability := next(
                        (
                            row
                            for row in win_probability_result_set["rowSet"]
                            if row[
                                win_probability_result_set["headers"].index("GAME_ID")
                            ]
                            == g.game_id
                        ),
                        None,
                    ):
                        g.win_probability = APIObject(
                            attr_keys=win_probability_result_set["headers"],
                            attr_vals=win_probability,
                            object_type=win_probability_result_set["name"],
                        )
                    else:
                        g.win_probability = None
                else:
                    g.win_probability = None

                # Append the game to the list
                self.games.append(g)

        else:
            # No GameHeader found in the response. Something is wrong.
            logger.warning("No GameHeader found in scoreboardv2 API response")

        # Parse EastConfStandingsByDay & WestConfStandingsByDay
        self.east_conference_standings = []
        self.west_conference_standings = []
        for conf in ["East", "West"]:
            parent_standings = (
                self.east_conference_standings
                if conf == "East"
                else self.west_conference_standings
            )
            if conf_standings_result_set := next(
                (
                    x
                    for x in self.api_response.get("resultSets", [])
                    if x["name"] == f"{conf}ConfStandingsByDay"
                ),
                None,
            ):
                # Parse the east/west conference standings result set
                parent_standings.extend(
                    APIObject(
                        attr_keys=conf_standings_result_set["headers"],
                        attr_vals=z,
                        object_type=f"{conf}ConfStandingsByDay",
                    )
                    for z in conf_standings_result_set["rowSet"]
                )
