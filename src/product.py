#!/usr/bin/env python

from src.time_series import TimeSeries
import os

class Product():
    scenarios = {
        'base': 'base',
        'best': 'best_case',
        'worst': 'worst_case',
    }

    def __init__(self, dir: str):
        self._base_ts = self.extract_ts_from(dir, 'base')
        self._best_ts = self.extract_ts_from(dir, 'best')
        self._worst_ts = self.extract_ts_from(dir, 'worst')

    def extract_ts_from(self, dir: str, scenario: str) -> TimeSeries:
        for filename in os.listdir(dir):
            if filename.startswith(self.scenarios[scenario]):
                return TimeSeries(os.path.join(dir, filename))
        return None