# -*- coding: utf-8 -*-
""" test_printer.py: Tests printer helper
"""
__author__ = "Charan Mahesan"

from core.helpers.printer import generate_csv_avg_comparison

AVG_COMPARISON_DATA = {"ALL": {"old": 1500.0, "new": 500.0}, "ep1": {"old": 2000.00, "new": 0},
                       "ep2": {"old": 3000.00, "new": 1000.0}, "ep3": {"old": 1500.1515, "new": 500.0505},
                       "ep4": {"old": 4000.00, "new": 0}, "ep5": {"old": 0, "new": 500}}
EXPECTED_CSV_OUPTUT = "URL, old, new\n" \
                      "ALL, 1500.0, 500.0\n" \
                      "ep1, 2000.0, 0\n" \
                      "ep2, 3000.0, 1000.0\n" \
                      "ep3, 1500.1515, 500.0505\n" \
                      "ep4, 4000.0, 0\n" \
                      "ep5, 0, 500\n"


def test_printer_valid(tmpdir):
    csv_file = tmpdir.join("comparison.csv")
    gen_csv = generate_csv_avg_comparison(AVG_COMPARISON_DATA, "old", ["new"], csv_file)
    assert csv_file.read() == EXPECTED_CSV_OUPTUT
    assert gen_csv


def test_printer_invalid_file(caplog):
    invalid_file = ("/invalid_comparison.csv")
    gen_csv = generate_csv_avg_comparison(AVG_COMPARISON_DATA, "old", ["new"], invalid_file)
    assert not gen_csv
    assert "Unable to write to file {}".format(invalid_file) in caplog.text
