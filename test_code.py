#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
./test_code.py; red_green_bar.py $? $COLUMNS
red_green_bar.py is taken from https://github.com/kwadrat/rgb_tdd.git
"""

import sys
import unittest

from eisenstein import Eisenstein


class TestEisensteinNumbers(unittest.TestCase):
    def test_equal_values(self):
        """
        TestNumbers:
        """
        a = Eisenstein(1, 2)
        b = Eisenstein(20, 30)
        c = a + b
        self.assertEqual(c, Eisenstein(21, 32))

    def test_multiplication(self):
        """
        TestNumbers:
        wolframalfa.com
        query: w = ( -1 + i sqrt(3) ) / 2 ; a = ( 1 + 2 w ); b = ( 2 + 4 w ) ; c = a * b
        answer: c = -6
        """
        a = Eisenstein(1, 2)
        b = Eisenstein(2, 4)
        c = a * b
        self.assertEqual(c, Eisenstein(-6, 0))


fast_test_ls = [TestEisensteinNumbers]


def add_all_fast(suite):
    for one_test in fast_test_ls:
        suite.addTest(unittest.makeSuite(one_test))


def summary_status(suite):
    text_test_result = unittest.TextTestRunner().run(suite)
    return not not (text_test_result.failures or text_test_result.errors)


def perform_tests():
    suite = unittest.TestSuite()
    add_all_fast(suite)
    return summary_status(suite)


if __name__ == "__main__":
    result = perform_tests()
    sys.exit(result)
