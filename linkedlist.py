#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
"""Simple linked list implementation.
"""

import weakref


class CircDblLnkList:
    """Circular, doubly linked list."""

    def __init__(self):
        """Instantiate a circular, doubly linked list."""
        self.__head = None
        self.__tail = None
        self.__sz = 0
        self.__min = None

    def ins(self, elem):
        """Insert at head."""
        self.__sz += 1

        if self.__head:
            elem.next = self.__head
            self.__head.prev = weakref.ref(elem)
        else:
            elem.next = weakref.ref(elem)
        self.__head = elem

        if self.__tail:
            self.__tail.next = elem
        else:
            self.__tail = elem
        elem.prev = weakref.ref(self.__tail)

        # Update min. element.
        if not self.__min or self.__min > elem:
            self.__min = elem

    def rem(self, elem):
        """Remove a given element from the list."""
        if self.is_empty:
            return elem

        self.__sz -= 1

        if not self.__sz:
            self.__head = None
            self.__tail = None
            elem.unlink()
            return elem

        elem.prev().next = elem.next
        elem.next.prev = elem.prev

        # Update head if required.
        if self.__head == elem:
            self.__head = elem.next

        # Update tail if required.
        if self.__tail == elem:
            self.__tail = elem.prev()

        elem.unlink()

        if self.__min == elem:
            self.__min = self.__find_min()

        return elem

    def pop(self):
        """Remove at tail"""
        return self.rem(self.__tail)

    def elems(self):
        """Iterate through the elements in the list."""
        head = self.__head
        while True:
            yield head
            if head != self.__tail:
                head = head.next
            else:
                break

    def __find_min(self):
        """Find element with minimum value."""
        min_elem = self.__head
        for elem in self.elems():
            if min_elem > elem:
                min_elem = elem
        return min_elem

    @property
    def min_elem(self):
        return self.__min

    @property
    def size(self):
        return self.__sz

    @property
    def is_empty(self):
        return self.__sz == 0
