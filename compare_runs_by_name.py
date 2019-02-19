# -*- coding: utf-8 -*-
""" compare_runs.py: Compares the results from multiple test runs by name
"""
__author__ = "Charan Mahesan"
import argparse
import collections
from core.models.session import Session
from core.helpers import combine_runs, printer
from core.blazemeter import api


def usage_msg():
    """
    Provides default help message
    """
    return '''compare_runs_by_name.py
         Sample usage:
         `python3 compare_runs.py -n R33, R33.1 -o R32`
        '''


def get_args():
    """
    Validates arguments provided via command line, and returns them back to the main function
    """
    parser = argparse.ArgumentParser(description='Generate request stat comparison', usage=usage_msg())
    parser.add_argument("-o", "--old", help="The name of the test run to be used as the baseline",
                        required=True)
    parser.add_argument("-n", "--new", help="Comma separated list of test run names to be used as the new data set",
                        required=True)
    parser.add_argument("-c", "--csv_file", help="Output location (default is 'comparison.csv' in current directory",
                        required=False, type=str, default="./comparison.csv")

    args = parser.parse_args()
    new_list = [x.strip() for x in args.new.split(',')]
    return args.old.strip(), new_list, args.csv_file


def compare_runs():
    """Gets information on each run_name"""
    old_run, new_runs, csv_output = get_args()
    all_runs = new_runs[:]
    all_runs.append(old_run)

    run_data = collections.defaultdict(dict)
    for run in all_runs:
        run_info = api.bm_api("GET", url=f'/masters?projectId=PROJECT_ID&workspaceId=WORKSPACE_ID&limit=10&name={run}')
        run_sessions = [session for run in run_info.get('result', []) for session in run.get('sessionsId', [])]
        run_data[run]['session_ids'] = run_sessions
        if not run_sessions:
            print("Could not find any sessions associated with {run_name}".format(run_name=run))
            exit(1)

    # get session information for all runs
    for run_name in run_data:
        run_data[run_name]['session_data'] = []
        for session_id in run_data[run_name]['session_ids']:
            session = Session(session_id)
            session.get_average_info()
            run_data[run_name]['session_data'].append(session)

        # aggregate session averages
        run_data[run_name]['session_averages'] = combine_runs.aggregate_session_averages(
            run_data[run_name]['session_data'])

    avg_comparison = combine_runs.compare_averages(run_data)

    # GENERATE_SUMMARY
    if printer.generate_csv_avg_comparison(avg_comparison, old_run, new_runs, csv_output):
        exit(0)
    exit(1)


if __name__ == '__main__':
    compare_runs()
