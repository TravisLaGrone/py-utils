from enum import Enum, auto
from typing import Iterable, NewType, Any, Callable, Union, Optional

E = NewType('E', Any)


def contains_weakly_ordered(
        it: Iterable[Optional[E]],
        a: Optional[E]=None,
        b: Optional[E]=None,
        a_matches: Optional[Callable[[Optional[E]], bool]]=None,
        b_matches: Optional[Callable[[Optional[E]], bool]]=None,
) -> bool:
    """Whether the given poset contains `a` and `b` in weak order.

    Args:
        it (Iterable[Optional[E]]): Assumes to be a partially ordered set
            ("poset"). May contains `None` as an element.
        a (Optional[E]): The element for which to determine if it occurs before
            `b` in weak order within `it`. May be `None`, in which case nulls
            are considered homogeneous.
        b (Optional[E]): The element for which to determine if it occurs after
            `a` in weak order within `it`. May be `None`, in which case nulls
            are considered homogeneous.
        a_matches (Optional[Callable[[Optional[E]], bool]]): A predicate that
            matches some element `a`. If non-null, then used instead of `a.__eq__`
            to identify the "a" element. It is assumed that `a_matches` will not
            match any element other than "a".
        a_matches (Optional[Callable[[Optional[E]], bool]]): A predicate that
            matches some element `b`. If non-null, then used instead of `b.__eq__`
            to identify the "b" element. It is assumed that `b_matches` will not
            match any element other than "b".

    Returns:
        bool: Whether `it` contains `a` before `b` in weak order. `False` if `it`
            does not contain both `a` and `b`.

    Tests:
        >>> it = [3, 2, 1]
        >>> contains_weakly_ordered(it, 3, 1)
        True
        >>> contains_weakly_ordered(it, 3, 4)
        False
        >>> contains_weakly_ordered(it, 4, 3)
        False
        >>> contains_weakly_ordered(it, 1, 3)
        False
        >>> contains_weakly_ordered(it, 2, 2)
        True
        >>> contains_weakly_ordered(it,
        ...                         a_matches=lambda a: a == 3,
        ...                         b_matches=lambda b: b == 1)
        True
        >>> contains_weakly_ordered(it, 3, b_matches=lambda b: b == 1)
        True

    """
    a_matches = a_matches if a_matches else lambda other: a == other
    b_matches = b_matches if b_matches else lambda other: b == other
    it_contains_a = False
    for e in it:
        if a_matches(e):
            it_contains_a = True
        if b_matches(e):
            return it_contains_a
    return False


def contains_strictly_ordered(
        it: Iterable[Optional[E]],
        a: Optional[E] = None,
        b: Optional[E] = None,
        a_matches: Optional[Callable[[Optional[E]], bool]] = None,
        b_matches: Optional[Callable[[Optional[E]], bool]] = None,
) -> bool:
    """Whether the given poset contains `a` and `b` in strict order.

    Args:
        it (Iterable[Optional[E]]): Assumes to be a partially ordered set
            ("poset"). May contains `None` as an element.
        a (Optional[E]): The element for which to determine if it occurs before
            `b` in strict order within `it`. May be `None`, in which case nulls
            are considered homogeneous.
        b (Optional[E]): The element for which to determine if it occurs after
            `a` in strict order within `it`. May be `None`, in which case nulls
            are considered homogeneous.
        a_matches (Optional[Callable[[Optional[E]], bool]]): A predicate that
            matches some element `a`. If non-null, then used instead of `a.__eq__`
            to identify the "a" element. It is assumed that `a_matches` will not
            match any element other than "a".
        a_matches (Optional[Callable[[Optional[E]], bool]]): A predicate that
            matches some element `b`. If non-null, then used instead of `b.__eq__`
            to identify the "b" element. It is assumed that `b_matches` will not
            match any element other than "b".

    Returns:
        bool: Whether `it` contains `a` before `b` in strict order. `False` if `it`
            does not contain both `a` and `b`.

    Tests:
        >>> it = [3, 2, 1]
        >>> contains_strictly_ordered(it, 3, 1)
        True
        >>> contains_strictly_ordered(it, 3, 4)
        False
        >>> contains_strictly_ordered(it, 4, 3)
        False
        >>> contains_strictly_ordered(it, 1, 3)
        False
        >>> contains_strictly_ordered(it, 2, 2)
        False
        >>> contains_strictly_ordered(it,
        ...                           a_matches=lambda a: a == 3,
        ...                           b_matches=lambda b: b == 1)
        True
        >>> contains_strictly_ordered(it,
        ...                           a_matches=lambda a: a == 2,
        ...                           b_matches=lambda b: b == 2)
        False
        >>> contains_strictly_ordered(it, 3, b_matches=lambda b: b == 1)
        True

    """
    a_matches = a_matches if a_matches else lambda other: a == other
    b_matches = b_matches if b_matches else lambda other: b == other
    it_contains_a = False
    a_matched_on = None
    for e in it:
        if a_matches(e):
            it_contains_a = True
            a_matched_on = e
        if b_matches(e):
            return it_contains_a and a_matched_on is not e
    return False
