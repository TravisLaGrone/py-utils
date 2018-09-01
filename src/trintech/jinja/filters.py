

from typing import Any, Union, Iterator, Iterable
from rnet93dd.templating import (PUNCTUATION_PAIRS_LEFT_TO_RIGHT as L2R,
                                 PUNCTUATION_PAIRS_RIGHT_TO_LEFT as R2L)
from rnet93dd.utils import is_iter, is_str, ensure_iterable
from .tests import is_quoted


def _quote_helper(elem: Any, chL: str, chR: str) -> str:
    escaped = str(elem).replace(chR, chR + chR)
    quoted = chL + escaped + chR
    return quoted


def quote(value: Union[Any, Iterable[Any]], quote_character: str=']') -> Iterator[str]:
    ch = str(quote_character)
    chL = R2L.get(ch, ch)  # left quote character
    chR = L2R.get(ch, ch)  # right quote character
    if is_iter(value) and not is_str(value):
        for elem in value:
            yield _quote_helper(elem, chL, chR)
    else:
        yield _quote_helper(value, chL, chR)


def quote_identifier(value: Union[Any, Iterable[Any]]) -> Iterator[str]:
    yield from quote(value, ']')


def quote_string(value: Union[Any, Iterable[Any]]) -> Iterator[str]:
    yield from quote(value, '\'')


def _ensure_quoted_helper(elem, chL: str, chR: str) -> str:
    elem = str(elem)
    if not is_quoted(elem, chR):
        elem = quote(elem, chR)
    return elem


def ensure_quoted(value: Union[Any, Iterable[Any]], quote_character: str=']') -> Iterator[str]:
    ch = str(quote_character)
    chL = R2L.get(ch, ch)  # left quote character
    chR = L2R.get(ch, ch)  # right quote character
    if is_iter(value) and not is_str(value):
        for elem in value:
            yield _ensure_quoted_helper(elem, chL, chR)
    else:
        yield _ensure_quoted_helper(value, chL, chR)


def _unquote_helper(value: Any, chL: str, chR: str) -> str:
    val = str(value)
    if is_quoted(val, chR):
        val = val[1:-1]  # unquote
        val = val.replace(chR + chR, chR)  # unescape
    return val


def unquote(value: Union[Any, Iterable[Any]], quote_character: str=']') -> Iterator[str]:
    ch = str(quote_character)
    chL = R2L.get(ch, ch)  # left quote character
    chR = L2R.get(ch, ch)  # right quote character
    if is_iter(value) and not is_str(value):
        for elem in value:
            yield _unquote_helper(elem, chL, chR)
    else:
        yield _unquote_helper(value, chL, chR)


def qualify(value: Union[Any, Iterable[Any]], separator: str='.') -> str:
    if is_iter(value) and not is_str(value):
        value = separator.join(str(elem) for elem in value)
    return value


def identify(value: Union[Any, Iterable[Any]]) -> str:
    it = ensure_iterable(value) # wrap as iterable (if not already)
    it = [e for e in it if e]   # filter by truthiness (on raw types)
    it = [str(e) for e in it]   # convert to strings (if not already)
    it = [e for e in it if e]   # filter by truthiness (on str representations)
    it = quote(it)              # quote each
    ident = qualify(it)         # qualify all
    return ident


FILTERS =  {
    'quote':    quote,
    'unquote':  unquote,
    'qualify':  qualify,
    'identify': identify,
}