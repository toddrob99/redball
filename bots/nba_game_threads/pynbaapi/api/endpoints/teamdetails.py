import logging

from ...constants import APP_NAME
from ..models.base import APIObject
from .base import APIEndpoint

logger = logging.getLogger(__name__)


class TeamDetails(APIEndpoint):
    def __str__(self) -> str:
        return f"<{APP_NAME}.TeamHistory: {self.background.city} {self.background.nickname}>"

    def _parse_api_response(self, api_response: dict) -> None:
        # Parse TeamBackground result set
        if team_background_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamBackground"
            ),
            None,
        ):
            if not len(team_background_result_set["rowSet"]):
                logger.warning(
                    "No TeamBackground rows returned in teamdetails API call"
                )
                setattr(self, "background", None)
            else:
                setattr(
                    self,
                    "background",
                    APIObject(
                        attr_keys=team_background_result_set["headers"],
                        attr_vals=team_background_result_set["rowSet"][0],
                        object_type=team_background_result_set["name"],
                    ),
                )
        else:
            # No TeamBackground found in the response. Something is wrong.
            logger.warning(
                "No TeamBackground result set found in teamdetails API response"
            )

        # Parse the TeamHistory result set
        setattr(self, "history", [])
        if team_history_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamHistory"
            ),
            None,
        ):
            for team_history in team_history_result_set["rowSet"]:
                self.history.append(
                    APIObject(
                        attr_keys=team_history_result_set["headers"],
                        attr_vals=team_history,
                        object_type=team_history_result_set["name"],
                    )
                )

        # Parse the TeamSocialSites result set
        setattr(self, "social_sites", [])
        if team_social_sites_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamSocialSites"
            ),
            None,
        ):
            for team_social_site in team_social_sites_result_set["rowSet"]:
                self.social_sites.append(
                    APIObject(
                        attr_keys=team_social_sites_result_set["headers"],
                        attr_vals=team_social_site,
                        object_type=team_social_sites_result_set["name"],
                    )
                )

        # Parse the TeamAwardsChampionships result set
        setattr(self, "awards_championships", [])
        if team_awards_championships_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamAwardsChampionships"
            ),
            None,
        ):
            for team_championship in team_awards_championships_result_set["rowSet"]:
                self.awards_championships.append(
                    APIObject(
                        attr_keys=team_awards_championships_result_set["headers"],
                        attr_vals=team_championship,
                        object_type=team_awards_championships_result_set["name"],
                    )
                )

        # Parse the TeamAwardsConf result set
        setattr(self, "awards_conf", [])
        if team_awards_conf_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamAwardsConf"
            ),
            None,
        ):
            for team_conf_championship in team_awards_conf_result_set["rowSet"]:
                self.awards_conf.append(
                    APIObject(
                        attr_keys=team_awards_conf_result_set["headers"],
                        attr_vals=team_conf_championship,
                        object_type=team_awards_conf_result_set["name"],
                    )
                )

        # Parse the TeamAwardsDiv result set
        setattr(self, "awards_div", [])
        if team_awards_div_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamAwardsDiv"
            ),
            None,
        ):
            for team_div_championship in team_awards_div_result_set["rowSet"]:
                self.awards_div.append(
                    APIObject(
                        attr_keys=team_awards_div_result_set["headers"],
                        attr_vals=team_div_championship,
                        object_type=team_awards_div_result_set["name"],
                    )
                )

        # Parse the TeamHof result set
        setattr(self, "hof_players", [])
        if team_hof_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamHof"
            ),
            None,
        ):
            for hof_player in team_hof_result_set["rowSet"]:
                self.hof_players.append(
                    APIObject(
                        attr_keys=team_hof_result_set["headers"],
                        attr_vals=hof_player,
                        object_type="TeamHOFPlayer",
                    )
                )

        # Parse the TeamRetired result set
        setattr(self, "retired_numbers", [])
        if team_retired_result_set := next(
            (
                x
                for x in self.api_response.get("resultSets", [])
                if x["name"] == "TeamRetired"
            ),
            None,
        ):
            for retired_number in team_retired_result_set["rowSet"]:
                self.retired_numbers.append(
                    APIObject(
                        attr_keys=team_retired_result_set["headers"],
                        attr_vals=retired_number,
                        object_type=team_retired_result_set["name"],
                    )
                )
