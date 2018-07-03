"""

"""


# from itertools import *
# from functools import *


class IndexableMapper:

    def __init__(self, mapper):
        self._mapper = mapper

    def __getitem__(self, item):
        return self._mapper(item)

