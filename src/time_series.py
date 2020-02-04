#!/usr/bin/env python

from __future__ import annotations
import os
from copy import deepcopy
import pandas as pd
import numpy as np

from src.utils import date_parser, filename_from

class TimeSeries():
    base = 'base_scenario'
    readable = {
        'csv': pd.read_csv,
        'xlsx': pd.read_excel
    }

    @property
    def time_series(self):
        return self._time_series

    @property
    def scenarios(self):
        return self.time_series.columns[1:]

    # Done
    def __init__(self, product_dir: str):
        self._time_series = self.time_series_from(product_dir)

    # Done
    def time_series_from(self, product_dir: str) -> pd.DataFrame:
        time_series = self.dataframe_from(product_dir)
        return time_series

    def dataframe_from(self, product_dir: str) -> pd.DataFrame:
        dataframe = None
        for filename in os.listdir(product_dir):
            name, extension = filename.split('.')
            names = ['date', name]
            if extension in self.readable.keys():
                file_path = os.path.join(product_dir, filename)
                file_dataframe = self.readable[extension](file_path, names=names)
                dataframe = self.merge_dataframes(dataframe, self.clean(file_dataframe, name))
        dataframe.interpolate(limit_direction='both', inplace=True)
        return self.sum_base_to(dataframe)

    def clean(self, dataframe: pd.DataFrame, time_series_name: str): #-> pd.DataFrame:
        dataframe['date'] = pd.to_datetime(dataframe['date'], errors='coerce')
        dataframe[time_series_name] = pd.to_numeric(dataframe[time_series_name], errors='coerce')
        dataframe.dropna(inplace=True)
        return dataframe

    def merge_dataframes(self, dataframe, file_dataframe):
        if dataframe is not None:
            return dataframe.merge(file_dataframe, on='date', how='outer')
        return file_dataframe

    def remove(self, outliers: int) -> pd.DataFrame:
        if not outliers:
            return self.time_series
        ts = deepcopy(self.time_series)
        for column in ts.columns[1:]:
            mask = (ts[column] - ts[column].mean()).abs() >= (outliers * ts[column].std())
            ts.loc[mask, column] = np.NaN
        return ts.interpolate(limit_direction='both')

    def sum_base_to(self, dataframe):
        for column in dataframe.columns[1:]:
            if column != self.base:
                dataframe[column] = dataframe[column] + dataframe[self.base]
        return dataframe