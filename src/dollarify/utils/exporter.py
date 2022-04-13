"""
Export data to files (csv, xls) and other data structures.
"""
import os

import pandas as pd


def to_csv(file_path, dataframe: pd.DataFrame, **kwargs) -> bool:
    dataframe.to_csv(file_path, **kwargs)
    return os.path.isfile(file_path)