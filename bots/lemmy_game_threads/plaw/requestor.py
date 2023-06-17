from enum import Enum
import requests
import json
from typing import Dict, Any, TypeVar

T = TypeVar("T")

class HttpType(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    # ... any other HTTP methods you need

class Requestor:
    def __init__(self, headers: Dict[str, str]):
        self.headers = headers

    def request(self, type_: HttpType, url: str, form: Dict[str, Any]) -> T:
        if type_ == HttpType.GET:
            response = requests.get(url, params=form, headers=self.headers)
        else:
            headers = {
                "Content-Type": "application/json",
                **self.headers,
            }
            response = requests.request(type_.value, url, data=json.dumps(form), headers=headers)

        if response.status_code != 200:
            raise Exception(response.text)  # Adjust this according to how your API returns errors

        return response.json()
