from functools import singledispatch
from typing import Optional, Union, Callable, Iterable, NewType, Iterator
import itertools as it
import cytoolz.itertoolz as itz

E = NewType('Element')
D = NewType('Default')


def reversed_iter(
        iterator: Iterator[E],
) -> Iterable[E]:
    return list(iterator).reverse()


def first_true(
        iterable: Iterable[E],
        default: Optional[D]=None,
        predicate: Optional[Union[int, Callable]]=None,
) -> Optional[D, E]:
    if not predicate:
        predicate = lambda: True
    for e in iterable:
        if predicate:
            return e
    else:
        return default


def last_true(
        iterable: Iterable[E],
        default: Optional[D]=None,
        predicate: Optional[Union[int, Callable]]=None,
) -> Optional[D, E]:
    return first_true(reversed(iterable), default, predicate)


