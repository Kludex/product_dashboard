#!/usr/bin/env python

from pathlib import Path

import pandas as pd

def project_root() -> Path:
    """
    Gets the project root.

    Returns:
        Path: project root path.
    """
    return Path(__file__).parent.parent

def merge_dataframes(dataframe: pd.DataFrame, file_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Merges two dataframes.

    Args:
        dataframe (pd.DataFrame): main dataframe.
        file_dataframe (pd.DataFrame): dataframe to append.

    Returns:
        pd.DataFrame: merged dataframe.
    """
    if dataframe is not None:
        return dataframe.merge(file_dataframe, on='date', how='outer')
    return file_dataframe
