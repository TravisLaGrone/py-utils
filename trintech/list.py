

from typing import List, Any, NewType, Optional, Callable, Iterable
from itertools import dropwhile

E = NewType('Element', Any)


def lstrip(
        L: List[Optional[E]],
        value: Optional[E]=None,
        matcher: Optional[Callable[[Optional[E]], bool]]=None,
        inplace=False,
) -> List[Optional[E]]:
    if inplace:
        stripped = delwhile(L, value, matcher)
    else:
        matcher = matcher if matcher else lambda e: value == e
        stripped = dropwhile(matcher, L)
    return stripped


def rstrip(
        L: List[Optional[E]],
        value: Optional[E]=None,
        matcher: Optional[Callable[[Optional[E]], bool]]=None,
        inplace=False,
) -> List[Optional[E]]:
    if inplace:
        stripped = delwhile(L.reverse(), value, matcher).reverse()
    else:
        matcher = matcher if matcher else lambda e: value == e
        stripped = reversed(dropwhile(matcher, reversed(L)))
    return stripped


def strip(
        L: List[Optional[E]],
        value: Optional[E]=None,
        matcher: Optional[Callable[[Optional[E]], bool]]=None,
        inplace=False,
) -> List[Optional[E]]:
    matcher = matcher if matcher else lambda e: value == e
    stripped = lstrip(L, matcher, inplace)
    stripped = rstrip(stripped, matcher, inplace)
    return stripped


def delwhile(
        L: List[Optional[E]],
        value: Optional[E] = None,
        matcher: Optional[Callable[[Optional[E]], bool]] = None,
) -> List[Optional[E]]:
    matcher = matcher if matcher else lambda e: value == e
    while L and not matcher(L[0]):
        del L[0]
    return L
