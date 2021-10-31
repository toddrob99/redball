import logging

from ...constants import APP_NAME
from ..models.base import APIObject
from .base import APIEndpoint

logger = logging.getLogger(__name__)


class LeagueStandings(APIEndpoint):
    def __str__(self) -> str:
        return f"<{APP_NAME}.LeagueStandings: Season: {self.api_parameters['SeasonYear']}, Season Type: {self.api_parameters['SeasonType']}, League: {self.api_parameters['LeagueID']}>"

    def _parse_api_response(self, api_response: dict) -> None:
        # Parse Standings result set
        setattr(self, "standings", [])
        if result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "Standings"
            ),
            None,
        ):
            for row in result_set["rowSet"]:
                self.standings.append(
                    APIObject(
                        attr_keys=result_set["headers"],
                        attr_vals=row,
                        object_type=result_set["name"],
                    )
                )
        else:
            # No Standings result set found in the response. Something is wrong.
            logger.warning(
                "No Standings result set found in LeagueStandings API response"
            )
