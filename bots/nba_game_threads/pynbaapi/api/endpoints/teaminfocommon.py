import logging

from ...constants import APP_NAME
from ..models.base import APIObject
from .base import APIEndpoint

logger = logging.getLogger(__name__)


class TeamInfoCommon(APIEndpoint):
    def __str__(self) -> str:
        return f"<{APP_NAME}.TeamInfoCommon: {self.team_info.team_city} {self.team_info.team_name} ({self.team_info.team_abbreviation})>"

    def _parse_api_response(self, api_response: dict) -> None:
        # Parse TeamInfoCommon result set
        if result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamInfoCommon"
            ),
            None,
        ):
            if not len(result_set["rowSet"]):
                logger.warning(
                    "No TeamInfoCommon rows returned in teaminfocommon API call"
                )
                setattr(self, "team_info", None)
            else:
                setattr(
                    self,
                    "team_info",
                    APIObject(
                        attr_keys=result_set["headers"],
                        attr_vals=result_set["rowSet"][0],
                        object_type=result_set["name"],
                    ),
                )
        else:
            # No TeamInfoCommon found in the response. Something is wrong.
            logger.warning(
                "No TeamInfoCommon result set found in teaminfocommon API response"
            )
            setattr(self, "team_info", None)

        # Parse TeamSeasonRanks result set
        if result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamSeasonRanks"
            ),
            None,
        ):
            if not len(result_set["rowSet"]):
                logger.warning(
                    "No TeamSeasonRanks rows returned in teaminfocommon API call"
                )
                setattr(self, "team_season_ranks", None)
            else:
                setattr(
                    self,
                    "team_season_ranks",
                    APIObject(
                        attr_keys=result_set["headers"],
                        attr_vals=result_set["rowSet"][0],
                        object_type=result_set["name"],
                    ),
                )
        else:
            setattr(self, "team_season_ranks", None)

        # Parse AvailableSeasons result set
        setattr(self, "available_seasons", [])
        if result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "AvailableSeasons"
            ),
            None,
        ):
            for row in result_set["rowSet"]:
                self.available_seasons.append(
                    APIObject(
                        attr_keys=result_set["headers"],
                        attr_vals=row,
                        object_type=result_set["name"],
                    )
                )
