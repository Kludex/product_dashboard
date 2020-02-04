#!/usr/bin/env python

from src.time_series import TimeSeries
import json
import os

class Product():

    @property
    def name(self):
        return self._config['name']

    @property
    def time_series(self):
        return self._time_series

    @property
    def scenarios(self):
        return self.time_series.scenarios

    # Done
    def __init__(self, product_dir: str):
        self._config = self.config_from(product_dir)
        self._time_series = self.time_series_from(product_dir)

    # Done
    def time_series_from(self, product_dir: str) -> TimeSeries:
        return TimeSeries(product_dir)

    # Done
    def config_from(self, product_dir: str) -> dict:
        filename = os.path.join(product_dir, 'config.json')
        with open(filename) as f:
            return json.load(f)

    def data_from(self, outliers):
        return self.time_series.remove(outliers)