

import re
from itertools import *
from typing import *


def to_sql_string_literal(str_):
    escaped = ''.join([chr_ * 2 if chr_ == '\'' else chr_ for chr_ in str_])
    quoted = '\'' + escaped + '\''
    return quoted

def to_VALUES_table(data: 'iterable of iterables'):
    num_cols = [max(len(record_of_entries)) for record_of_entries in data]
    records = []
    for record in data:
        entries = islice(chain(record, repeat('')), num_cols)
        entries = ','.join(entries)
        records.append('(' + entries + ')')
    records = ','.join(records)
    values = '(VALUES ' + records + ') '
    values += 'AS values_(' + ', '.join(['col' + str(num+1) for num in range()]) + ')'
    return values

def to_VALUES_list(data: 'iterable'):
    return '(' + ','.join(data) + ')'

def format_snippet(snippet):
    """
    Formats the given snippet of SQL code as json "body" for SQL Operations Studio and/or VS Code.
    Each line in the snippet should be (but is not required to be) idented as intended using spaces.
    """
    lines = snippet.splitlines()
    lines = map(lambda str_: '"' + str_ + '",', lines)  # quote and delimit each line
    return '\n'.join(lines)

def csv_to_VALUES(*, data=None, file=None, column_separator='\t', row_separator='\n'):
    """
    Transforms CSV data to a T-SQL 'VALUES' statement.

    At least one of 'data' (a string) or 'file' (a string or unopened handle) must be non-null.
    If both are non-null, then 'file' is ignored.

    Assumes all values are strings.
    """
    if data is None:
        with open(file) as f:
            data = f.read()
    max_fields = 0
    lines = []
    for line in data.split(row_separator):
        if line == '':
            continue
        fields = []
        for field in line.split(column_separator):
            field = to_sql_string_literal(field)
            fields.append(field)
        max_fields = max(max_fields, len(fields))  # COMBAK do on first iteration only (optimize)
        line = '\t(' + ', '.join(fields) + ')'
        lines.append(line)
    values = ',\n'.join(lines)
    values = '(VALUES\n{}\n)'.format(values)
    aliases = ',\n'.join('\tcol' + str(col+1) for col in range(max_fields))
    aliases = '[values] (\n{}\n)'.format(aliases)
    data = values + ' AS ' + aliases
    return data

def quote(ident: str) -> str:
    """Quotes a T-SQL ident. Assumes the ident is not already quoted."""
    ident = ident.replace(']', ']]')  # escape
    return f'[{ident}]'  # quote

def qualify(*idents: List[str]) -> str:
    """Constructs a possibly multi-part T-SQL identifier string. Does not perform any quotation."""
    if len(idents) == 0:
        raise ValueError("An identifier may not be empty.")
    if any(len(part) == 0 for part in idents):
        raise ValueError("No identifier part may be empty.")
    return '.'.join(idents)

def quote_and_qualify(*idents: List[str]) -> str:
    return qualify(quote(ident) for ident in idents)