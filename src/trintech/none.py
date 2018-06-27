

from typing import Iterable


def ifPresent(it: Iterable) -> Iterable:
    return (obj for obj in it if obj != None)


def ifPresentElse(obj, alternative):
    if obj != None:
        return obj
    else:
        return alternative


def ifPresentElseGet(obj, supplier):
    if obj != None:
        return obj
    else:
        return supplier()


def ifPresentElseMap(obj, mapper):
    if obj != None:
        return obj
    else:
        return mapper(obj)


def ifPresentElseSet(obj, consumer):
    if obj != None:
        return obj
    else:
        consumer(obj)


def ifPresentElseDo(obj, action):
    if obj != None:
        return obj
    else:
        action()


def mapIfPresentElse(obj, mapper, alternative):
    if obj != None:
        return mapper(obj)
    else:
        return alternative


def ifAbsent(it: Iterable) -> Iterable:
    return (obj for obj in it if obj == None)