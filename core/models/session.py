# -*- coding: utf-8 -*-
""" session.py: Test Run (or Session) object class
"""
__author__ = "Charan Mahesan"
import re
from core.blazemeter.api import bm_api


class Session:
    """Representation of a individual test run/test session"""
    def __init__(self, session_id):
        self.session_id = session_id
        self.session_info = None
        self.average_info = None

        self.get_session_data()

    def get_session_data(self):
        session_info = bm_api(method="GET", url=f'/sessions/{self.session_id}/reports/main/summary')
        if session_info:
            self.session_info = session_info

    def get_average_info(self):
        average_info = {}
        if self.session_info:
            for label in self.session_info.get("result", {}).get("summary", []):
                regexed_label = re.sub(r'\/(\d+)', '/{{id}}', label.get('lb'))
                average_info[regexed_label] = {}
                average_info[regexed_label]['avg'] = label.get('avg')
                average_info[regexed_label]['hits'] = label.get('hits')

            self.average_info = average_info
