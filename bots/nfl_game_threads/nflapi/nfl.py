import logging
from pprint import pformat
from typing import Dict, Optional

import pendulum
import requests
from fcache.cache import FileCache
from requests.exceptions import HTTPError
from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation

from .const import *
from .helpers import *
from .__version__ import __version__

logger = logging.getLogger(__name__)

EPOCH = pendulum.datetime(1970, 1, 1)


class NFLClientCredentials(requests.auth.AuthBase):
    """
    A requests Auth object that maintains a token for the nfl.com api

    The token is cached using a file cache that may or may not work
    across multiple processes. The worst that can happen is that it
    is refreshed unnecessarily.
    """

    def __init__(self, cache_name: str = 'nflapi'):
        self.cache = FileCache(cache_name, flag='cs')
        self.cache.clear()

    def __call__(self, r: requests.Request):
        r.headers['Authorization'] = self.__get_token(ua=r.headers.get('User-Agent', None))
        return r

    def __get_token(self, ua):
        if self.cache.get('expire', EPOCH) < pendulum.now():
            self.__update_token(ua)
        token = self.cache.get('token')
        logger.debug("Using token: %s" % token)
        return token

    def __update_token(self, ua):
        logger.debug('Updating auth token')
        data = {
            'grant_type': 'client_credentials'
        }
        response = self.__token_request(ENDPOINT_V1_REROUTE, data, ua)
        token = '{token_type} {access_token}'.format(**response)
        expire = pendulum.now().add(seconds=response['expires_in'] - 30)
        self.cache['token'] = token
        self.cache['expire'] = expire
        logger.debug('Updated token: %s - expires %s', token, expire)

    @staticmethod
    def __token_request(path, data, ua):
        headers = {'X-Domain-Id': '100', 'User-Agent': ua}
        logger.debug('Request: POST %s, data=<%s>', path, pformat(data))

        url = API_HOST + path
        logger.debug('Request headers: %s', pformat(headers))
        response = requests.request('POST', url, data=data,
                                    headers=headers)
        try:
            js = response.json()
            response.raise_for_status()
            logger.debug('Response: %s', pformat(js))
            return js
        except HTTPError as e:
            raise Exception("Unsuccessful response: %r" % response.data) from e
        except ValueError as e:
            raise Exception("Response from API was not json: %s"
                            % response.data) from e


class NFL:
    def __init__(self, ua: str, auth: requests.auth.AuthBase = False):
        self.__version__ = __version__
        self.ua = ua
        base_headers = {
            'X-Domain-Id': '100',
            'User-Agent': self.ua,
        }
        if auth is False:
            auth = NFLClientCredentials('nflapi')
        self.endpoint = RequestsEndpoint(API_HOST + ENDPOINT_V3, base_headers=base_headers, auth=auth)

        self.team = TeamHelper(self)
        self.schedule = ScheduleHelper(self)
        self.standings = StandingsHelper(self)
        self.game = GameHelper(self)
        self.game_detail = GameDetailHelper(self)
        self.roster = RosterHelper(self)
        self.player = PlayerHelper(self)

    def query(self, op: Operation, variables: Optional[Dict] = None, return_json=False):
        logger.debug("Running query: %s", op)
        data = self.endpoint(op, variables)
        logger.debug("Return data: %s", data)
        if return_json:
            return (op + data), data
        else:
            return op + data
