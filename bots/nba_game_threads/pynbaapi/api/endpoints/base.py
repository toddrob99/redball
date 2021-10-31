import logging

logger = logging.getLogger(__name__)


class APIEndpoint:
    def __init__(
        self,
        api_response: dict,
    ) -> None:
        self.api_response = api_response
        self.api_resource = api_response.get("resource") or "unknown"
        self.api_parameters = api_response.get("parameters", {})
        self._parse_api_response(api_response)

    def _parse_api_response(self, api_response: dict) -> None:
        # Parse in a default way
        pass
