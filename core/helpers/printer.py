# -*- coding: utf-8 -*-
""" printer.py: Collection of print calls to output data
"""
__author__ = "Charan Mahesan"
import logging

LOGGER = logging.getLogger('core.helpers.printer')


def generate_csv_avg_comparison(avg_comparison, old_label, new_labels, output_file):
    """
    Generates a CSV file of average comparison
    :param avg_comparison:(dict) Dictionary of URL, run_label, and data
    Expected input format:
    {"/some/url":{"old_label": {"avg": 100}, "new_label1": {"avg": 200 }, "new_label2": {"avg": 150}}}
    :param old_label:(str)  Baseline run label, e.g. "old_label"
    :param new_labels:[list of strings] list of run labels, in the order to print out in the CSV.
    e.g. ["new_label1", "new_label2"]
    :param output_file: Location to print CSV
    """

    output_message = "URL, {old_label}, {new_labels}\n".format(old_label=old_label, new_labels=", ".join(new_labels))
    for url in avg_comparison:
        # get all the new_label info first
        new_run_avgs = []
        for label in new_labels:
            new_run_avgs.append(str(avg_comparison[url].get(label, 0)))
        output_message = output_message + "{url}, {old_avg}, {new_avg}\n".\
            format(url=url, old_avg=avg_comparison[url].get(old_label, 0), new_avg=", ".join(new_run_avgs))

    try:
        with open(output_file, "w") as my_out:
            my_out.write(output_message)
        return True
    except IOError:
        LOGGER.error("Unable to write to file %s", output_file)
        return False
