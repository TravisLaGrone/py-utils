from enum import Enum, auto
from typing import Iterable, NewType, Any

E = NewType('E', Any)


def contains_weakly_ordered(it: Iterable[E], a: E, b: E) -> bool:
    """Whether the given iterable contains `a` and `b` in weak order.

    Returns false if the given iterable does not contain both `a` and `b`.

    Assumptions:
    - The iterable constitutes a weak partially-ordered set.
    - Nulls are homogeneous.

    Tests:
        >>> it = ['A', 'B', 'C']
        >>> contains_weakly_ordered(it, 'A', 'A')
        True
        >>> contains_weakly_ordered(it, 'A', 'B')
        True
        >>> contains_weakly_ordered(it, 'A', 'C')
        True
        >>> contains_weakly_ordered(it, 'A', 'D')
        False
        >>> contains_weakly_ordered(it, 'D', 'A')
        False
        >>> contains_weakly_ordered(it, 'C', 'A')
        False
        >>> contains_weakly_ordered(it, 'B', 'A')
        False

    """
    if a == b:
        return a in it
    contains_a = False
    for e in it:
        if a == e:
            contains_a = True
        if b == e:
            if contains_a:
                return True
            else:
                return False
    return False


def contains_strictly_ordered(it: Iterable[E], a: E, b: E) -> bool:
    """Whether the given iterable contains `a` and `b` in strict order.

    Returns false if the given iterable does not contains both `a` and `b`.
    Returns false if `a` and `b` are equal.

    Assumptions:
    - The iterable constitutes a strict partially-ordered set.
    - Nulls are homogeneous.

    Tests:
        >>> it = ['A', 'B', 'C']
        >>> contains_strictly_ordered(it, 'A', 'A')
        False
        >>> contains_strictly_ordered(it, 'A', 'B')
        True
        >>> contains_strictly_ordered(it, 'A', 'C')
        True
        >>> contains_strictly_ordered(it, 'A', 'D')
        False
        >>> contains_strictly_ordered(it, 'D', 'A')
        False
        >>> contains_strictly_ordered(it, 'C', 'A')
        False
        >>> contains_strictly_ordered(it, 'B', 'A')
        False

    """
    if a == b:
        return False
    return contains_weakly_ordered(it, a, b)
