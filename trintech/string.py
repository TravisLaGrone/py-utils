"""
Utilities for strings.
"""


from typing import Optional


def quote(
        string: str,
        quote: Optional[str]=None,
        lquote: Optional[str]=None,
        rquote: Optional[str]=None,
        escape: Optional[str]=None,
) -> str:
    """Quotes the given string.

    Quotes `string` by first escaping any instances of `rquote`, and then
    prepending `lquote` and appending `rquote`.

    If `quote` is non-null, then it is used as both `lquote` and `rquote`. Either
    `quote` must be non-null, or both `lquote` and `rquote` must be non-null.

    If `escape` is non-null, then escaping is performed by prefixing the
    character sequence to be escaped with `escape`. Otherwise, escaping is
    performed by doubling the character sequence to be escaped.

    Args:
        string (str): The string to quote.
        quote (str): The character(s) to use for both the left and right quotes.
        lquote (str): The character(s) to use for the left quote.
        rquote (str): The character(s) to use for the right quote.
        escape (str): The character(s) to use as a prefix escape sequence. If
            `None`, then escaping is performed by doubling the character(s) to be
            escaped.

    Returns:
        str: The escaped and quoted form of `string`.

    Examples:
        >>> quote('Hello, world!', quote="'", escape='\')
        "'Hello, world!'"
        >>> quote("This is a 'nested' string.", quote="'", escape='\\\\')
        "'This is a \\\\'nested\\\\' string.'"
        >>> quote('tsql[identifier]', lquote='[', rquote=']', escape=None)
        '[tsql[identifier]]]'
        >>> quote('"double quotes"', quote='"', escape='&&')
        '"&&"double quotes&&""'

    """
    if quote != None:
        lquote = rquote = quote
    escaped = string.replace(rquote, (escape if escape != None else rquote) + rquote)
    quoted = lquote + escaped + rquote
    return quoted


def quote_python(
        string: str
) -> str:
    """Quotes the given string as a Python string literal.

    Args:
        string: The string to quote.

    Returns:
        The escaped and quoted form of `string`.

    Examples:
        >>> quote_python("this is a 'python' string")
        "'this is a \\\\'python\\\\' string'"

    """
    return quote(string, quote='\'', escape='\\')
