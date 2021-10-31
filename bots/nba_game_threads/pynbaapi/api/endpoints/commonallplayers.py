import logging

from ...constants import APP_NAME
from ..models.base import APIObject
from .base import APIEndpoint

logger = logging.getLogger(__name__)


class CommonAllPlayers(APIEndpoint):
    def __str__(self) -> str:
        return f"<{APP_NAME}.CommonAllPlayers: League: {self.api_parameters['LeagueID']}, Season: {self.api_parameters['Season']}, Current Season Only: {self.api_parameters['IsOnlyCurrentSeason'] == 1}>"

    def _parse_api_response(self, api_response: dict) -> None:
        # Parse CommonAllPlayers result set
        setattr(self, "players", [])
        if result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "CommonAllPlayers"
            ),
            None,
        ):
            for row in result_set["rowSet"]:
                self.players.append(
                    APIObject(
                        attr_keys=result_set["headers"],
                        attr_vals=row,
                        object_type=result_set["name"],
                    )
                )
        else:
            # No CommonAllPlayers result set found in the response. Something is wrong.
            logger.warning(
                "No CommonAllPlayers result set found in CommonAllPlayers API response"
            )
