#!/usr/bin/env python

import os
import json
import pandas as pd

from src.time_series import TimeSeries

class Product():
    """
    This class is the representation of a product.

    Attributes:
        _config (dict): product configurations.
        _time_series (list): time series which represents scenarios.
    """

    @property
    def name(self) -> str:
        """
        Get the name of the product.

        Returns:
            str: name of the product.
        """
        return self._config['name']

    @property
    def time_series(self) -> list:
        """
        Get the time series.

        Returns:
            list: time series which represents scenarios.
        """
        return self._time_series

    @property
    def scenarios(self) -> list:
        """
        Get the name of the time series (scenarios).

        Returns:
            list: scenarios.
        """
        return self.time_series.scenarios()

    def __init__(self, product_dir: str):
        self._config = self.config_from(product_dir)
        self._time_series = self.time_series_from(product_dir)

    def data_from(self, outliers: int) -> pd.DataFrame:
        """
        Extracts all the data and removes outliers based on a multiplier.

        Parameters:
            outliers (int): multiplier necessary to remove outlier numbers.

        Returns:
            pd.DataFrame: data from product.
        """
        return self.time_series.remove(outliers)

    @staticmethod
    def time_series_from(product_dir: str) -> TimeSeries:
        """
        Extracts time series found from product directory.

        Parameters:
            product_dir (str): product directory name.

        Returns:
            TimeSeries: time series found from product.
        """
        return TimeSeries(product_dir)

    @staticmethod
    def config_from(product_dir: str) -> dict:
        """
        Extracts product information from config file.

        Parameters:
            product_dir (str): product directory name.

        Returns:
            dict: product information.
        """
        filename = os.path.join(product_dir, 'config.json')
        with open(filename) as file:
            return json.load(file)
