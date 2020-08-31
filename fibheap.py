#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
"""Pure-python implementation of Fibonacci Heaps.
"""

from linkedlist import CircDblLnkList

import sys
import weakref


class HeapNode:

    def __init__(self, value):
        """Initialize `HeapNode` with value."""
        self.__value = value
        self.prev = None
        self.next = None
        self.__root = False
        self.children = set()
        self.__parent = None
        self.__marked = False

    def unlink(self):
        """Remove `prev` and `next` pointers."""
        self.prev = None
        self.next = None

    def link(self, child):
        """Add a child."""
        child.make_child_of(self)
        self.children.add(child)

    def cut(self, child):
        """Remove a given child."""
        self.children.remove(child)
        # The following call will fail!
        child.__parent = None
        return child

    def make_root(self):
        """Make this node a root node."""
        self.__root = True
        self.__parent = None

    def make_child_of(self, parent):
        """Make this node a child of another."""
        self.__root = False
        self.__parent = weakref.ref(parent)

    @property
    def is_root(self):
        """Return if node is root."""
        return self.__root

    def mark(self):
        """Mark node."""
        self.__marked = True

    def unmark(self):
        """Unmark node."""
        self.__marked = False

    @property
    def is_marked(self):
        """Return if marked or not."""
        return self.__marked

    def check_order(self):
        """Check heap order."""
        return (not self.parent) or (self.parent.value < self.value)

    def update(self, repl):
        """Update node with the replacement."""
        repl.prev = self.prev
        repl.next = self.next

        if self.__root:
            repl.make_root()

        repl.children = self.children

        if self.is_marked:
            repl.mark()

        parent = self.parent
        parent.cut(self)
        parent.link(repl)

        return repl.check_order()

    @property
    def value(self):
        """Return the value stored in the node."""
        return self.__value

    @property
    def rank(self):
        """Return the node rank."""
        return len(self.children)

    @property
    def parent(self):
        """Return parent, if exists, of the node."""
        return self.__parent() if self.__parent else None

    def __lt__(self, other):
        if not other:
            return True
        return self.__value < other.value

    def __eq__(self, other):
        return (self.__value == other.value) and (self.children == other.children)

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        root_tag = "°" if self.__root else ""

        if self.prev:
            prev_tag = "«" if self.prev() != self else ""
        else:
            prev_tag = ""

        if self.next:
            _n = self.next if type(self.next) is HeapNode else self.next()
            next_tag = "»" if _n != self else ""
        else:
            next_tag = ""

        return f"{prev_tag}({root_tag}{self.value})·[{self.rank}]{next_tag}"


class FibonacciHeap:

    __err = sys.stderr.write

    def __init__(self):
        """Initialize a `FibonacciHeap`."""
        # List of trees.
        self.__trees = CircDblLnkList()

    def add_tree(self, tree):
        """Add a tree to the heap."""
        tree.make_root()
        self.__trees.ins(tree)

    def rem_tree(self, tree):
        """Remove a tree from the heap."""
        self.__trees.rem(tree)

    def __meld_children(self, root):
        """Meld children of the given root into the heap."""
        for child in root.children:
            self.add_tree(child)

    def __consolidate(self):
        """Consolidate trees so that no two roots have the same rank."""
        ranks = {}
        for curr in [elem for elem in self.__trees.elems() if elem]:
            while curr.rank in ranks:
                curr, prev = curr, ranks[curr.rank]
                # Ensure that `curr` is the smaller root.
                if curr > prev:
                    curr, prev = prev, curr
                del ranks[curr.rank]

                # Make larger root be a child of smaller root.
                self.rem_tree(prev)
                curr.link(prev)

            ranks[curr.rank] = curr

    def ins(self, value):
        """Insert a value into the `FibonacciHeap`."""
        tree = HeapNode(value)
        self.add_tree(tree)

    def extract_min(self):
        """Delete minimum value."""
        if not self.min_elem:
            return None

        self.__meld_children(self.min_elem)
        elem = self.__trees.rem(self.min_elem)
        self.__consolidate()
        return elem

    def __graft(self, parent, child):
        """Cut the child from the parent and meld it into the heap."""
        parent.cut(child)
        self.add_tree(child)
        child.unmark()

    def dec_key(self, curr, value):
        """Decrease the value of the given node."""
        # Replacement node.
        repl = HeapNode(value)
        if curr.update(repl):
            return repl

        # Head order violated.

        child = repl
        parent = child.parent
        self.__graft(parent, child)

        while parent and not parent.is_root:
            if not parent.is_marked:
                parent.mark()
                return repl

            child = parent
            parent = child.parent
            self.__graft(parent, child)

        return repl

    @property
    def min_elem(self):
        """Return minimum element."""
        return self.__trees.min_elem

    @property
    def trees(self):
        """Return number of trees in the heap."""
        return self.__trees.size

    def iter_trees(self):
        """Retrieve the roots of the trees in the heap."""
        yield from self.__trees.elems()

    def show_tree_roots(self):
        """Display the tree roots in the Fibonacci heap."""
        print("  ¦  ".join((str(n) for n in self.iter_trees())))
