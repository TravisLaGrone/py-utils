

from typing import *

from trintech.enum import DefinitionOrderedEnum
from trintech.list import strip
from trintech.string import quote


def quote_string(
        string: str,
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
        ident: str,
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
        quote: bool=False,
) -> str:
    """Constructs a qualified T-SQL identifier.

    Args:
        parts (Iterable[str]): The parts (in order) from which to construct a
            qualified T-SQL identifier.
        quote (bool): Whether to quote each part according to `quote_identifier`.

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


class QualifiedIdentifier:
    class Part(DefinitionOrderedEnum):
        SERVER = 'server'
        DATABASE = 'database'
        SCHEMA = 'schema'
        OBJECT = 'object'
        MINOR = 'minor'

    def __init__(self, server=None, database=None, schema=None, object=None, minor=None):
        self._server = server
        self._database = database
        self._schema = schema
        self._object = object
        self._minor = minor
        if not self._is_valid():
            raise ValueError("A T-SQL qualified identifier may not have an "
                             "empty intermediate part with a non-empty predecessor "
                             "part and a non-empty successor part.")

    def __iter__(self):
        return self._server, self._database, self._schema, self._object, self._minor

    def to_list(self):
        return [self._server, self._database, self._schema, self._object, self._minor]

    def to_tuple(self):
        return self._server, self._database, self._schema, self._object, self._minor

    def _is_valid(self):
        L = self.to_list()
        L = strip(L, value=None, inplace=True)
        return None in L

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, value):
        old_server = self._server
        self._server = value
        if not self._is_valid():
            self._server = old_server
            raise ValueError("A T-SQL qualified identifier may not have an "
                             "empty intermediate part with a non-empty predecessor "
                             "part and a non-empty successor part.")

    @server.deleter
    def server(self):
        self.server = None

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        old_database = self._database
        self._database = value
        if not self._is_valid():
            self._database = old_database
            raise ValueError("A T-SQL qualified identifier may not have an "
                             "empty intermediate part with a non-empty predecessor "
                             "part and a non-empty successor part.")

    @database.deleter
    def database(self):
        self.database = None

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value):
        old_schema = self._schema
        self._schema = value
        if not self._is_valid():
            self._schema = old_schema
            raise ValueError("A T-SQL qualified identifier may not have an "
                             "empty intermediate part with a non-empty predecessor "
                             "part and a non-empty successor part.")

    @schema.deleter
    def schema(self):
        self.schema = None

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, value):
        old_object = self._object
        self._object = value
        if not self._is_valid():
            self._object = old_object
            raise ValueError("A T-SQL qualified identifier may not have an "
                             "empty intermediate part with a non-empty predecessor "
                             "part and a non-empty successor part.")

    @object.deleter
    def object(self):
        self.object = None

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, value):
        old_minor = self._minor
        self._minor = value
        if not self._is_valid():
            self._minor = old_minor
            raise ValueError("A T-SQL qualified identifier may not have an "
                             "empty intermediate part with a non-empty predecessor "
                             "part and a non-empty successor part.")

    @minor.deleter
    def minor(self):
        self.minor = None
