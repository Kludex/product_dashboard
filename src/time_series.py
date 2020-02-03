#!/usr/bin/env python

import pandas as pd

class TimeSeries():

    def __init__(self, filename: str):
        self._ts = self.read(filename)

    def read(self, filename: str) -> pd.DataFrame:
        if filename.endswith('csv'):
            return pd.read_csv(filename)
        if filename.endswith('xlsx'):
            return pd.read_excel(filename)
        raise OSError(filename=filename)
