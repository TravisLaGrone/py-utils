"""The project setup script.

Use with the `setuptools` package.

"""
from setuptools import setup

setup(
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-datadir'],
)

