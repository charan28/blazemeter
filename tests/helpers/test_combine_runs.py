# -*- coding: utf-8 -*-
""" test_combine_runs.py: Tests combining run data
"""
__author__ = "Charan Mahesan"

import collections
import pytest
from core.helpers import combine_runs
from core.models.session import Session

SESSION_1_DATA = {"ALL": {"avg": 1000, "hits": 10}, "ep1": {"avg": 2000, "hits": 10},
              "ep2": {"avg": 2000.0, "hits": 5}, "ep3": {"avg": 1000.101010, "hits": 10}}
SESSION_2_DATA = {"ALL": {"avg": 2000, "hits": 10}, "ep2": {"avg": 4000.0, "hits": 5},
              "ep3": {"avg": 2000.202020, "hits": 10}, "ep4": {"avg": 4000, "hits": 10}}
SESSION_3_DATA = {"ALL": {"avg": 500, "hits": 10}, "ep2": {"avg": 1000.0, "hits": 5},
                  "ep3": {"avg": 500.050505, "hits": 10}, "ep5": {"avg": 500, "hits": 10}}


@pytest.fixture(scope='module')
def run_1_data():
    session_1 = Session('invalid')
    session_2 = Session('invalid')
    session_1.average_info = SESSION_1_DATA
    session_2.average_info = SESSION_2_DATA

    return combine_runs.aggregate_session_averages([session_1, session_2])


@pytest.fixture(scope='module')
def run_2_data():
    session_3 = Session('invalid')
    session_3.average_info = SESSION_3_DATA

    return combine_runs.aggregate_session_averages([session_3])


def test_multiple_aggregate_session_averages(run_1_data):
    assert run_1_data['ALL']['total_time'] == 30000
    assert run_1_data['ALL']['total_hits'] == 20
    assert run_1_data['ALL']['avg'] == 1500.0

    assert run_1_data['ep1']['avg'] == 2000.00
    assert run_1_data['ep2']['avg'] == 3000.00
    assert run_1_data['ep3']['avg'] == 1500.1515
    assert run_1_data['ep4']['avg'] == 4000.00


def test_single_aggregate_session_averages(run_2_data):
    assert run_2_data['ALL']['total_time'] == 5000
    assert run_2_data['ALL']['total_hits'] == 10
    assert run_2_data['ALL']['avg'] == 500.0

    assert run_2_data['ep2']['avg'] == 1000.0
    assert run_2_data['ep3']['avg'] == 500.0505
    assert run_2_data['ep5']['avg'] == 500


def test_invalid_aggregate_session_averages():
    invalid_session = Session('invalid')
    average_data = combine_runs.aggregate_session_averages([invalid_session])
    assert not average_data


def test_valid_compare_averages(run_1_data, run_2_data):
    run_data = collections.defaultdict(dict)
    run_data['old']['session_averages'] = run_1_data
    run_data['new']['session_averages'] = run_2_data

    average_comparison = combine_runs.compare_averages(run_data)
    assert average_comparison['ALL'].get('old', 0) == 1500.0
    assert average_comparison['ALL'].get('new', 0) == 500.0

    assert average_comparison['ep1'].get('old', 0)  == 2000.00
    assert average_comparison['ep1'].get('new', 0) == 0

    assert average_comparison['ep5'].get('old', 0)  == 0
    assert average_comparison['ep5'].get('new', 0) == 500