import pandas as pd


def count_na(series: pd.Series) -> int:
    return len(series) - series.count()


count_null = count_na  # alias
