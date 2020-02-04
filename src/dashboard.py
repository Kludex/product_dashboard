#!/usr/bin/env python

import os
import pandas as pd
from pathlib import Path
from typing import Iterator

from src.utils import project_root
from src.product import Product

class Dashboard():

    @property
    def products(self) -> list:
        return self._products

    # Done
    def __init__(self, data_path: str = 'data'):
        self._products = self.products_from(data_path)

    # Done
    def products_from(self, data_path: Path) -> list:
        products = []
        for product_dir in os.listdir(data_path):
            product = Product(os.path.join(data_path, product_dir))
            products.append(product)
        return products

    # Done
    def product_names(self) -> Iterator[str]:
        for product in self.products:
            yield product.name

    def scenarios_from(self, product_name):
        for product in self.products:
            if product.name == product_name:
                return product.scenarios
        return []

    def data_from(self, product_name, outliers):
        for product in self.products:
            if product.name == product_name:
                return product.data_from(outliers)
        return None

    @staticmethod
    def annual_growth_for(serie: pd.Series) -> list:
        annual_growth = [0.0] * serie.size
        for date in range(serie.size - 12):
            annual_growth[date] = (serie[date + 12] - serie[date]) / 100
        return annual_growth
