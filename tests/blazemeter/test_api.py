# -*- coding: utf-8 -*-
""" test_api.py: Tests blazemeter api wrapper
"""
__author__ = "Charan Mahesan"

import pytest
from unittest import mock
from core.blazemeter import api


PROJECT_ID = "PROJECT_ID"
WORKSPACE_ID = "WORKSPACE_ID"
MOCK_SESSION_ID = ""


@pytest.fixture(autouse=True)
def get_session_id():
    global MOCK_SESSION_ID
    with mock.patch('core.blazemeter.api.BLAZEMETER_API_URL', "https://a.blazemeter.com/api/v4"):
        response = api.bm_api(method="GET",
                              url="/sessions?projectId="+PROJECT_ID+"&workspaceId="+WORKSPACE_ID+"&limit=1")
        MOCK_SESSION_ID = response['result'][0]['id']


    
def test_invalid_url():
    response = api.bm_api(method="GET", url="/endpoint_does_not_exit")
    assert not response


def test_valid_url():
    response = api.bm_api(method="GET", url="/sessions/"+MOCK_SESSION_ID+"/reports/main/summary")
    assert response
    assert not response['error']


def test_no_url():
    response = api.bm_api(method="GET")
    assert not response


def test_invalid_blazemeter_api_url():
    with mock.patch('core.blazemeter.api.BLAZEMETER_API_URL', "http://invalid.com"):
        response = api.bm_api(method="GET", url="/sessions/"+MOCK_SESSION_ID+"/reports/main/summary")
        assert not response


def test_invalid_request_method():
    with mock.patch('core.blazemeter.api.BLAZEMETER_API_URL', ""):
        response = api.bm_api(method="GET", url="/sessions/"+MOCK_SESSION_ID+"/reports/main/summary")
        assert not response
