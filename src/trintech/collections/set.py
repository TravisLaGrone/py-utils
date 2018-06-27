

from functools import reduce
from typing import Set


def union(*sets) -> set:
    if len(sets) == 0:
        return set()
    return reduce(lambda a,b: a.union(b), sets)


def intersection(*sets) -> set:
    if len(sets) == 0:
        return set()
    return reduce(lambda a,b: a.intersection(b), sets)


class UniversalSet(frozenset):
    pass
    # TODO

UNIVERSAL_SET = UniversalSet()


class EmptySet(frozenset):
    pass
    # TODO

EMPTY_SET = EmptySet()


