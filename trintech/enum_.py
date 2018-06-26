

from enum import Enum
from trintech.ordering import contains_weakly_ordered, contains_strictly_ordered


class OrderedEnum(Enum):
    """An enum whose names are ordered by their values.

    Tests:
        >>> class ABC(OrderedEnum):
        ...     A = 3
        ...     B = 2
        ...     C = 1
        >>> ABC.A > ABC.B > ABC.C
        True
        >>> ABC.C < ABC.B < ABC.A
        True
        >>> ABC.C <= ABC.B <= ABC.B
        True
        >>> ABC.A <= ABC.C
        False
        >>> print(list(ABC))
        [<ABC.A: 3>, <ABC.B: 2>, <ABC.C: 1>]
        >>> print(sorted(list(ABC)))
        [<ABC.C: 1>, <ABC.B: 2>, <ABC.A: 3>]

    """
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class DefinitionOrderedEnum(OrderedEnum):
    """An ordered enum whose names are ordered by their definition order.

    Tests:
        >>> from enum import auto
        >>> class ABC(DefinitionOrderedEnum):
        ...     A = auto()
        ...     B = auto()
        ...     C = auto()
        >>> A = ABC.A
        >>> B = ABC.B
        >>> C = ABC.C
        >>> A < B < C
        True
        >>> A > B > C
        False
        >>> A <= B <= C
        True
        >>> A >= B >= C
        False
        >>> B < B
        False
        >>> B > B
        False
        >>> B <= B
        True
        >>> B >= B
        True
        >>> print(list(abc.name for abc in ABC))
        ['A', 'B', 'C']
        >>> print(sorted(list(abc.name for abc in ABC)))
        ['A', 'B', 'C']

    """
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return contains_weakly_ordered(self.__class__, other, self)
        return NotImplemented
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return contains_strictly_ordered(self.__class__, other, self)
        return NotImplemented
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return contains_weakly_ordered(self.__class__, self, other)
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return contains_strictly_ordered(self.__class__, self, other)
        return NotImplemented
