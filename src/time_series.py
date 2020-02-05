#!/usr/bin/env python

from __future__ import annotations
import os
from copy import deepcopy
import pandas as pd
import numpy as np

from src.utils import merge_dataframes

class TimeSeries():
    """
    This class handles time series from products.

    Attributes:
        _time_series (list): representation of scenarios.
    """
    base = 'base_scenario'
    readable = {
        'csv': pd.read_csv,
        'xlsx': pd.read_excel,
    }

    @property
    def time_series(self) -> pd.DataFrame:
        """
        Get the time series.

        Returns:
            pd.DataFrame: time series which represents scenarios.
        """
        return self._time_series

    def scenarios(self) -> list:
        """
        Get the name of the time series (scenarios).

        Returns:
            list: scenarios.
        """
        return self.time_series.columns[1:]

    def __init__(self, product_dir: str):
        self._time_series = self.time_series_from(product_dir)

    def time_series_from(self, product_dir: str) -> pd.DataFrame:
        """
        Extracts time series found from product directory.

        Parameters:
            product_dir (str): product directory name.

        Returns:
            pd.DataFrame: time series from product.
        """
        time_series = self.dataframe_from(product_dir)
        return time_series

    def dataframe_from(self, product_dir: str) -> pd.DataFrame:
        """
        Extracts data from product.

        Parameters:
            product_dir (str): product directory name.

        Returns:
            pd.DataFrame: time series from product.
        """
        dataframe = None
        for filename in os.listdir(product_dir):
            name, extension = filename.split('.')
            names = ['date', name]
            if extension in self.readable.keys():
                file_path = os.path.join(product_dir, filename)
                file_dataframe = self.readable[extension](file_path, names=names)
                dataframe = merge_dataframes(dataframe, TimeSeries.clean(file_dataframe, name))
        dataframe.interpolate(limit_direction='both', inplace=True)
        return self.sum_base_to(dataframe)

    def remove(self, outliers: int) -> pd.DataFrame:
        """
        Remove outliers.

        Parameters:
            outliers (int): number of standard deviations to remove.

        Returns:
            pd.DataFrame: dataframe without outliers (based on the parameters).
        """
        if not outliers:
            return self.time_series
        time_series = deepcopy(self.time_series)
        for column in time_series.columns[1:]:
            mask = (time_series[column] - time_series[column].mean()).abs() >= \
                   (outliers * time_series[column].std())
            time_series.loc[mask, column] = np.NaN
        return time_series.interpolate(limit_direction='both')

    def sum_base_to(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Sums base to all dataframe columns that are not the base.

        Parameters:
            dataframe (pd.DataFrame): [description]

        Returns:
            [type]: [description]
        """
        for column in dataframe.columns[1:]:
            if column != self.base:
                dataframe[column] = dataframe[column] + dataframe[self.base]
        return dataframe

    @staticmethod
    def clean(dataframe: pd.DataFrame, time_series_name: str) -> pd.DataFrame:
        """
        Cleans a serie from the dataframe. It performs operations to cleans
        the date column and the time series itself.

        Parameters:
            dataframe (pd.DataFrame): product data.
            time_series_name (str): time series column name.

        Returns:
            pd.DataFrame: cleaned data.
        """
        dataframe['date'] = pd.to_datetime(dataframe['date'], errors='coerce')
        dataframe[time_series_name] = pd.to_numeric(dataframe[time_series_name], errors='coerce')
        dataframe.dropna(inplace=True)
        return dataframe
