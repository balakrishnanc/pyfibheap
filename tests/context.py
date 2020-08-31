#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
"""Set up the context for the unit tests.
"""

import os
import sys


__PKG_DIR__ = os.path.dirname(__file__)
__SRC_DIR__ = os.path.abspath(os.path.join(__PKG_DIR__, '../src'))

sys.path.insert(0, __SRC_DIR__)
