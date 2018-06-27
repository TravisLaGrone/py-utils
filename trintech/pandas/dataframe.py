from itertools import count

from cytoolz.itertoolz import first
import pandas as pd
from typing import Tuple, Callable, Any, Iterable, Optional

from trintech.iter import first_true


def groupby_row(
        df: pd.Dataframe
) -> pd.core.groupby.DataFrameGroupBy:
    return df.groupby([*df.index, *df.columns])


def cross(
        a: pd.DataFrame,
        b: pd.DataFrame,
        suffixes: Tuple[str, str]=('_x', '_y'),
) -> pd.DataFrame:
    a2 = a.rename(columns={c: c + suffixes[0] for c in a.columns}, inplace=False)
    b2 = b.rename(columns={c: c + suffixes[0] for c in b.columns}, inplace=False)
    key = first_true((f'key_{n}' for n in count()),
                     lambda k: k not in a.index and k not in b.index)
    a2[key] = 0
    b2[key] = 0
    a2.set_index(key, drop=True, append=True, inplace=True)
    b2.set_index(key, drop=True, append=True, inplace=True)
    return pd.merge(a2, b2, on=key, suffixes=('', ''))


def cross_apply(
        df: pd.DataFrame,
        func: Callable[[Any, pd.Series], pd.DataFrame]=lambda idx, row: row.to_frame().T,
) -> pd.DataFrame:
    """Equivalent to `CROSS APPLY` in T-SQL.

    Assumes `[*df.index, *df.columns]` constitutes a unique row identifier.

    """
    gb = pd.groupby([*df.index, *df.columns])
    return gb.apply(lambda grp: func(*first(grp.iterrows())))
