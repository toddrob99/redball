import logging

from ...constants import APP_NAME
from ..models.base import APIObject
from .base import APIEndpoint

logger = logging.getLogger(__name__)


class CommonTeamRoster(APIEndpoint):
    def __str__(self) -> str:
        return f"<{APP_NAME}.CommonTeamRoster: TeamID: {self.api_parameters['TeamID']}>"

    def _parse_api_response(self, api_response: dict) -> None:
        # Parse ComonTeamRoster result set
        setattr(self, "team_roster", [])
        if result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "CommonTeamRoster"
            ),
            None,
        ):
            for row in result_set["rowSet"]:
                self.team_roster.append(
                    APIObject(
                        attr_keys=result_set["headers"],
                        attr_vals=row,
                        object_type=f"{result_set['name']}Player",
                    )
                )
        else:
            # No CommonTeamRoster result set found in the response. Something is wrong.
            logger.warning(
                "No CommonTeamRosterPlayer result set found in commonteamroster API response"
            )
            setattr(self, "team_info", None)

        # Parse Coaches result set
        setattr(self, "team_coaches", [])
        if result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "Coaches"
            ),
            None,
        ):
            for row in result_set["rowSet"]:
                self.team_coaches.append(
                    APIObject(
                        attr_keys=result_set["headers"],
                        attr_vals=row,
                        object_type=result_set["name"],
                    )
                )
