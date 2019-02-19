# -*- coding: utf-8 -*-
""" combine_runs.py: Collection of functions used to combine data from multiple test runs
"""
__author__ = "Charan Mahesan"
import collections


def aggregate_session_averages(list_of_sessions):
    """Generates the average response time per URL for a set of sessions"""
    avg_data = collections.defaultdict(dict)
    for session in list_of_sessions:
        if session.average_info:
            for url in session.average_info:
                avg_data[url]['total_time'] = avg_data.get(url, {}).get('total_time', 0) + \
                    session.average_info[url]['avg']*session.average_info[url]['hits']
                avg_data[url]['total_hits'] = avg_data.get(url, {}).get('total_hits', 0) + \
                    session.average_info[url]['hits']

    for url in avg_data:
        avg_data[url]['avg'] = round(avg_data[url]['total_time'] / avg_data[url]['total_hits'], 4)

    return avg_data


def compare_averages(run_data):
    """Generates a dictionary containing URL and run name response times"""
    avg_comparison = collections.defaultdict(dict)
    for run_name in run_data:
        for url in run_data[run_name]['session_averages']:
            avg_comparison[url][run_name] = run_data[run_name]['session_averages'][url]['avg']

    return avg_comparison
