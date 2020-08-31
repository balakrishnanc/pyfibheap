#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
"""Bundles test cases.
"""

import context
import fibheap_test
import linkedlist_test
import unittest


def __get_modules():
    return [fibheap_test, linkedlist_test]


def main():
    loader = unittest.TestLoader()
    ts_list = [loader.loadTestsFromTestCase(tc)
               for mod in __get_modules()
               for tc in mod.get_test_cases()]
    suite = unittest.TestSuite(ts_list)
    unittest.TextTestRunner().run(suite)

    
if __name__ == '__main__':
    main()
