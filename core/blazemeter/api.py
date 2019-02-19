# -*- coding: utf-8 -*-
""" api.py: Wrapper to make BlazeMeter API calls
"""
__author__ = "Charan Mahesan"

import logging
import requests
from requests.auth import HTTPBasicAuth


LOGGER = logging.getLogger('core.blazemeter.api')
API_KEY_ID = "API_KEY_ID"
API_KEY_SECRET = "API_KEY_SECRET"
BLAZEMETER_API_URL = "https://a.blazemeter.com:443/api/v4"

def get_authentication():
    return HTTPBasicAuth(API_KEY_ID, API_KEY_SECRET)


def bm_api(method, **kwargs):
    """
    Makes API request to BlazeMeter
    :param method: Method of call
    :param kwargs: args to be sent to BlazeMeter - must include URL
    :return: Returns the response of the API call, or None if it fails
    """
    if "url" in kwargs:
        kwargs['url'] = BLAZEMETER_API_URL + kwargs['url']
    else:
        LOGGER.error("Must provide url to bm_api()")
        return None

    try:
        LOGGER.debug("Making request with method = {method}, {kwargs}")
        response = requests.request(method, **kwargs, auth=get_authentication())
        if response.json().get("error"):
            LOGGER.error("Error making request, received response: %s", response.json()['error'])
            return None
        return response.json()
    except ValueError as value_error:
        LOGGER.error(value_error)
