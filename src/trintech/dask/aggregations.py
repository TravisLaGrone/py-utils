

import dask.dataframe as dd


# FIXME: This results in errors.
unique = dd.Aggregation(
    'unique',
    lambda series: series.unique(),
    lambda series: series.unique(),
)


# FIXME: This results in errors.
set_ = dd.Aggregation(
    'set_',
    lambda series: set(series.unique()),
    lambda sets: set.intersection(sets)
)
