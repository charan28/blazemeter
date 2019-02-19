# -*- coding: utf-8 -*-
""" compare_runs.py: Compares the results from two sets of runs.
"""
__author__ = "Charan Mahesan"
import argparse
import collections
from core.models.session import Session
from core.helpers import combine_runs, printer


def usage_msg():
    """
    Provides default help message
    """
    return '''compare_runs.py
         Sample usage:
         `python3 compare_runs.py -n r-v4-5be0a8d4bc024 -o r-v4-5be0a8d4bc024 r-v4-5be31064a2609`
        '''


def get_args():
    """
    Validates arguments provided via command line, and returns them back to the main function
    """
    parser = argparse.ArgumentParser(description='Generate request stat comparison', usage=usage_msg())
    parser.add_argument("-o", "--old", help="Space separated list of session IDs to be used as the baseline",
                        required=True, nargs='+')
    parser.add_argument("-n", "--new", help="Space separated list of session IDs to be used as the new data set",
                        required=True, nargs='+')
    parser.add_argument("-c", "--csv_file", help="Output location (default is 'comparison.csv' in current directory",
                        required=False, type=str, default="./comparison.csv")

    args = parser.parse_args()
    return args.old, args.new, args.csv_file


def compare_runs():
    """Gets information on each session in old and new, generates a comparison CSV of averages"""
    old_sessions, new_sessions, csv_output = get_args()
    run_data = collections.defaultdict(dict)
    run_data['old']['session_ids'] = old_sessions
    run_data['new']['session_ids'] = new_sessions

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
    if printer.generate_csv_avg_comparison(avg_comparison, 'old', ["new"], csv_output):
        exit(0)
    exit(1)


if __name__ == '__main__':
    compare_runs()
