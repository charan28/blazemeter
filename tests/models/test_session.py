# -*- coding: utf-8 -*-
""" test_session.py: Tests session class
"""
__author__ = "Charan Mahesan"

import pytest
from core.models.session import Session
from unittest import mock
from unittest.mock import patch
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


def mock_valid_session():
    session = Session(MOCK_SESSION_ID)
    for label in session.session_info.get("result", {}).get("summary", []):
        label['avg'] = 777.56034482759
        label['hits'] = 116
    return session


@pytest.fixture
def valid_session():
    mock_session = mock_valid_session()
    with patch.object(Session, "__init__", lambda x, y: None):
        valid_session = Session(MOCK_SESSION_ID)
        valid_session.session_id = mock_session.session_id
        valid_session.session_info = mock_session.session_info
        valid_session.average_info = mock_session.average_info
        return valid_session


@pytest.fixture
def invalid_session():
    return Session('invalid')


def test_no_session_id():
    with pytest.raises(TypeError):
        Session()


def test_valid_average_info(valid_session):
    valid_session.get_average_info()
    assert valid_session.average_info
    assert valid_session.average_info['ALL']['hits'] == 116
    assert valid_session.average_info['ALL']['avg'] == 777.56034482759


def test_valid_creation(valid_session):
    assert valid_session.session_id == MOCK_SESSION_ID
    assert valid_session.session_info
    assert not valid_session.average_info


def test_invalid_creation(invalid_session):
    assert invalid_session.session_id == "invalid"
    assert not invalid_session.session_info

    invalid_session.get_average_info()
    assert not invalid_session.average_info
