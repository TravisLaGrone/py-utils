

from typing import Any, Optional
from rnet93dd.templating import (PUNCTUATION_PAIRS_LEFT_TO_RIGHT as L2R,
                                 PUNCTUATION_PAIRS_RIGHT_TO_LEFT as R2L)


def raise_helper(msg: str):
    raise Exception(msg)


def quote(value: Any, quotation_mark: str=']') -> str:
    ch = str(quotation_mark)
    chL = R2L.get(ch, ch)
    chR = L2R.get(ch, ch)
    str_ = str(value)
    escaped = str_.replace(chR, chR + chR)
    quoted = chL + escaped + chR
    return quoted


def identify(*varargs) -> str:
    return '.'.join(quote(id_, ']') for id_ in varargs)


def stringify(*varargs) -> str:
    quotable = varargs[0] if len(varargs) == 1 else identify(varargs)
    return quote(quotable, '\'')


def sqlcmd_connect_string(server: Optional[str]=None, timeout: Optional[int]=None,
                          uid: Optional[str]=None, pwd: Optional[str]=None) -> Optional[str]:
    con_str = None
    if server:
        con_str  = server
        con_str += f' -l {timeout}' if timeout != None else ''
        con_str += f' -U {uid}' if uid else ''
        con_str += f' -P {pwd}' if pwd else ''
    return con_str


GLOBALS = {
    'raise':                    raise_helper,
    'quote':                    quote,
    'identify':                 identify,
    'stringify':                stringify,
    'sqlcmd_connect_string':    sqlcmd_connect_string
}
