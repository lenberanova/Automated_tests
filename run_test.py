#!/usr/bin/env python3

from test import FileListTestCase, RandomFileTestCase
from pathlib import Path
from logger import log


def run_tests(tests):
    return [test.execute() for test in tests]


def log_test_results(tests, results):
    log.info("Test results:")
    for i in range(len(tests)):
        log.info("Test case {} - {}: {}".format(tests[i].get_tc_id(), tests[i].get_name(), results[i].name))


list_of_test = [FileListTestCase(str(Path.home())), RandomFileTestCase()]

test_results = run_tests(list_of_test)

log_test_results(list_of_test, test_results)
