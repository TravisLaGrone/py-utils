

import re
from itertools import *
from typing import *
from trintech.string import quote


def quote_string(
        string: str
) -> str:
    """Quotes T-SQL string literal.

    Args:
        string: The string literal to quote.

    Returns:
        The escaped and quoted form of `string` as a T-SQL string literal.

    Examples:
        >>> quote_string('my string')
        "'my string'"
        >>> quote_string("my 'quoted' string")
        "'my ''quoted'' string'"

    """
    return quote(string, '\'', escape=None)


def quote_identifier(
        ident: str
) -> str:
    """Quotes a T-SQL identifier.

    Args:
        ident: The identifier to quote. Assumed to be unqualified and unquoted.

    Returns:
        str: The escaped and quoted form of `ident` as a T-SQL identifier.

    Examples:
        >>> quote_identifier('identifier')
        '[identifier]'
        >>> quote_identifier('spaced identifier')
        '[spaced identifier]'
        >>> quote_identifier('weird[identifier]')
        '[weird[identifier]]]'

    """
    return quote(ident, lquote='[', rquote=']', escape=None)


def qualify_identifier(
        parts: Iterable[str],
        quote=False
) -> str:
    """Constructs a qualified T-SQL identifier.

    Args:
        parts Iterable[str]: The parts (in order) from which to construct a
            qualified T-SQL identifier.
        quote: Whether to quote each part according to `quote_identifier`.

    Returns:
        str: A qualified T-SQL identifier consisting of `parts`.

    Examples:
        >>> qualify_identifier([\'table\', \'column\'])
        'table.column'
        >>> qualify_identifier([\'database\', \'schema\', \'object\'])
        'database.schema.object'
        >>> qualify_identifier([\'object\'])
        'object'
        >>> qualify_identifier([\'My Table\', \'My Column\'], quote=True)
        '[My Table].[My Column]'

    """
    parts = list(parts)
    if len(parts) == 0:
        raise ValueError("An identifier may not be empty.")
    if any(len(part) == 0 for part in parts):
        raise ValueError("No identifier part may be empty.")
    return '.'.join([quote_identifier(part) for part in parts] if quote else parts)
