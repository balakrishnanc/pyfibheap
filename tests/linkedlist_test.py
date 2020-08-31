#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
"""Test cases for `linkedlist`.
"""

from linkedlist import CircDblLnkList
from fibheap import HeapNode

import random
import unittest


class EmptyListTestCase(unittest.TestCase):

    def setUp(self):
        self.lst = CircDblLnkList()

    def test_sz(self):
        self.assertEqual(self.lst.size, 0)

    def test_empty(self):
        self.assertTrue(self.lst.is_empty)


class BasicListTestCase(unittest.TestCase):

    def setUp(self):
        self.lst = CircDblLnkList()

        self.num_elems = 30
        self.elems = [HeapNode(random.randint(1, 100))
                      for i in range(self.num_elems)]
        self.min_elem = min(self.elems)

        for elem in self.elems:
            self.lst.ins(elem)

    def test_sz(self):
        self.assertEqual(self.lst.size, self.num_elems)

    def test_empty(self):
        self.assertFalse(self.lst.is_empty)

    def test_min_elem(self):
        self.assertEqual(self.lst.min_elem, self.min_elem)


def get_test_cases():
    return [EmptyListTestCase, BasicListTestCase]
