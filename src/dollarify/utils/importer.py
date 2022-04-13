"""
Import data from files (csv, xls) and other data structures.
"""
import pandas as pd


def read_csv(file_path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(file_path, **kwargs)

