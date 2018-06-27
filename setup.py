#!/usr/bin/env python
"""The project setup script.

Use with the `setuptools` package.

"""
from setuptools import setup, find_packages

setup(
    name='Utilities for Python',  # FIXME: Is this suppposed to be the name of the project, or of the package?
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-datadir'],
)
