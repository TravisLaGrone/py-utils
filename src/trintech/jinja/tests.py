import re
from typing import Any, Iterator, Iterable, Union


from rnet93dd.templating import (PUNCTUATION_PAIRS_LEFT_TO_RIGHT as L2R,
                                 PUNCTUATION_PAIRS_RIGHT_TO_LEFT as R2L)
from rnet93dd.utils import is_iter, is_str


def _is_quoted_helper(value: Any, chL: str, chR: str) -> bool:
    val = str(value)
    return (len(val) > 1
        and val.startswith(chL)
        and val.endswith(chR)
        and len(re.search(f'{re.escape(chR)}+$', val[1:]).string) % 2 != 0)  # is odd


def is_quoted(value: Union[Any, Iterable[Any]], quote_character: str=']') -> Iterator[bool]:
    ch = str(quote_character)
    chL = R2L.get(ch, ch)
    chR = L2R.get(ch, ch)
    if is_iter(value) and not is_str(value):
        for elem in value:
            yield _is_quoted_helper(elem, chL, chR)
    else:
        yield _is_quoted_helper(value, chL, chR)


TESTS = {
    'is_quoted': is_quoted
}
