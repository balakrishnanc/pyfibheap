#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
"""Test cases for `fibheap`.
"""

from fibheap import FibonacciHeap, HeapNode

import random
import unittest


class EmptyHeapTestCase(unittest.TestCase):

    def setUp(self):
        self.fh = FibonacciHeap()

    def test_min_elem(self):
        self.assertEqual(self.fh.min_elem, None)

    def test_trees(self):
        self.assertEqual(self.fh.trees, 0)

    def test_extract_min(self):
        self.assertEqual(self.fh.extract_min(), None)


class OneElemHeapTestCase(unittest.TestCase):

    def setUp(self):
        self.fh = FibonacciHeap()
        self.elem = HeapNode(random.randint(1, 100))
        self.fh.add_tree(self.elem)

    def test_min_elem(self):
        self.assertEqual(self.fh.min_elem, self.elem)

    def test_trees(self):
        self.assertEqual(self.fh.trees, 1)

    def test_extract_min(self):
        self.assertEqual(self.fh.extract_min(), self.elem)


class ManyElemHeapTestCase(unittest.TestCase):

    def setUp(self):
        self.fh = FibonacciHeap()
        self.num_elems = 30
        self.elems = [HeapNode(random.randint(1, 100))
                      for i in range(self.num_elems)]
        self.min_elem = min(self.elems)
        for elem in self.elems:
            self.fh.add_tree(elem)

    def test_min_elem(self):
        self.assertEqual(self.fh.min_elem, self.min_elem)

    def test_trees(self):
        self.assertEqual(self.fh.trees, self.num_elems)

    def test_extract_min(self):
        self.assertEqual(self.fh.extract_min(), self.min_elem)


class Cmplx1HeapTestCase(unittest.TestCase):

    def setUp(self):
        self.fh = FibonacciHeap()
        #
        # 17    24    23  7  21     3
        #  |    /\                / | \
            # 30  26  46            18 52 41
        #      |                 |     |
        #     35                39    44
        #
        self.elems = {v: HeapNode(v)
                      for v in (30,  7, 35, 26,
                               46, 24, 23, 17,
                               21, 39, 18, 52,
                               44, 41, 3)}
        self.snd_min_elem = sorted(self.elems.values())[1]

        self.elems[41].link(self.elems[44])
        self.elems[18].link(self.elems[39])
        self.elems[3].link(self.elems[41])
        self.elems[3].link(self.elems[52])
        self.elems[3].link(self.elems[18])
        self.fh.add_tree(self.elems[3])
        self.fh.add_tree(self.elems[21])
        self.fh.add_tree(self.elems[7])
        self.fh.add_tree(self.elems[23])
        self.elems[26].link(self.elems[35])
        self.elems[24].link(self.elems[46])
        self.elems[24].link(self.elems[26])
        self.fh.add_tree(self.elems[24])
        self.elems[17].link(self.elems[30])
        self.fh.add_tree(self.elems[17])

        # Remove `3`
        self.fh.extract_min()
        self.exp_num_trees = 3

    def test_snd_min_elem(self):
        self.assertEqual(self.fh.min_elem, self.snd_min_elem)

    def test_trees(self):
        self.assertEqual(self.fh.trees, self.exp_num_trees)


class Cmplx2HeapTestCase(unittest.TestCase):

    def setUp(self):
        self.fh = FibonacciHeap()
        #
        #            7         18    38
        #        /   |  \      /\     |
        #     24    17   23  21  39  41
        #     / \    |        |
        #   26  46  30       52
        #  / \   |
        # 35 88 72
        #
        self.elems = {v: HeapNode(v)
                      for v in (41, 38, 39, 52, 21,
                               18, 23, 30, 17, 72,
                               46, 88, 35, 26, 24, 7)}

        self.elems[38].link(self.elems[41])
        self.fh.add_tree(self.elems[38])
        self.elems[21].link(self.elems[52])
        self.elems[18].link(self.elems[39])
        self.elems[18].link(self.elems[21])
        self.fh.add_tree(self.elems[18])
        self.elems[17].link(self.elems[30])
        self.elems[46].link(self.elems[72])
        self.elems[26].link(self.elems[88])
        self.elems[26].link(self.elems[35])
        self.elems[24].link(self.elems[46])
        self.elems[24].link(self.elems[26])
        self.elems[7].link(self.elems[23])
        self.elems[7].link(self.elems[17])
        self.elems[7].link(self.elems[24])
        self.fh.add_tree(self.elems[7])

        self.elems[29] = self.fh.dec_key(self.elems[46], 29)
        del self.elems[46]

        self.elems[15] = self.fh.dec_key(self.elems[29], 15)
        del self.elems[29]

        self.elems[35].parent.mark()
        self.elems[35].parent.parent.mark()
        self.elems[5] = self.fh.dec_key(self.elems[35], 5)
        self.exp_num_trees = 7

        self.min_elem = min(self.elems.values())

    def test_min_elem(self):
        self.assertEqual(self.fh.min_elem, self.min_elem)

    def test_trees(self):
        self.assertEqual(self.fh.trees, self.exp_num_trees)
