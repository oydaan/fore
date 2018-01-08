# -*- coding: utf-8 -*-
import requests
import time
from fore.log import logger
from .models import TwitchException, TwitchAuthException

# Rate Limit Headers #
######################
# RateLimit-Limit — The number of requests you can use for the rate-limit window.
# RateLimit-Remaining — The number of requests you have left to use for the rate-limit window.
# RateLimit-Reset — A Unix epoch timestamp of when your rate-limit window will reset.


class TwitchAPI(object):
    headers = None

    rate_limit = None
    rate_remaining = None
    rate_reset = None

    req_date = None

    @staticmethod
    def set_auth(client_id):
        TwitchAPI.headers = {'Client-ID': client_id}

    @staticmethod
    def get(url, payload=None):
        payload = payload or {}
        logger.debug([url, payload])
        retries = 3
        res = None

        while retries > 0:
            try:
                res = requests.get(url, params=payload, headers=TwitchAPI.headers, verify=False)

                # rate limiting
                TwitchAPI.rate_limit = res.headers['Ratelimit-Limit']
                TwitchAPI.rate_remaining = res.headers['Ratelimit-Remaining']
                TwitchAPI.rate_reset = res.headers['Ratelimit-Reset']
                TwitchAPI.req_date = res.headers['Date']

                j = res.json()

                if j.get('error', None):
                    err = '{} ({}): {}'.format(j.get("error"), j.get("status"), j.get["message"])
                    raise TwitchException(err)
                return j
            except ValueError as e:
                logger.exception(e)
                if res:
                    logger.warning(res.text)
                retries -= 1
                if retries <= 0:
                    raise
                time.sleep(0.3)
            except Exception as e:
                logger.exception(e)
                raise e
