"""
Provides an installation -agnostic import context for tests.

Tests should import local modules to be tested by invoking::

    from tests.context import ...

For example::

    from tests.context import trintech

This file provides a mechanism by which tests may import the module(s) to be
tested without regard to how they are installed:  project source or packaged wheel.

"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# noinspection PyUnresolvedReferences
import trintech
