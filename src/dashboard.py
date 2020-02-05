#!/usr/bin/env python

from pathlib import Path
import os
import pandas as pd

from src.product import Product

class Dashboard():
    """
    This class handles the dashboard operations.

    Attributes:
        _products (list): products.
    """

    def __init__(self, data_path: str = 'data'):
        self._products = Dashboard.products_from(data_path)

    @property
    def products(self) -> list:
        """
        Get the products list.

        Returns:
            list: products.
        """
        return self._products

    def product_names(self) -> list:
        """
        Extracts The name of products.

        Returns:
            list: name of products.
        """
        return [product.name for product in self.products]

    def scenarios_from(self, product_name: str) -> list:
        """
        Search the scenarios from a product based on its name.

        Parameters:
            product_name (str): name of the product.

        Returns:
            list: scenarios from product.
        """
        for product in self.products:
            if product.name == product_name:
                return product.scenarios
        return []

    def data_from(self, product_name: str, outliers: int) -> pd.DataFrame:
        """
        Extracts all the data from product based on its name and removes
        outliers based on a multiplier.

        Parameters:
            product_name (str): name of the product.
            outliers (int): multiplier necessary to remove outlier numbers.

        Returns:
            pd.DataFrame: data from product.
        """
        for product in self.products:
            if product.name == product_name:
                return product.data_from(outliers)
        return None

    @staticmethod
    def annual_growth_for(serie: pd.Series) -> list:
        """
        Computes annual growth for each observation.

        Parameters:
            serie (pd.Series): observation float values.

        Returns:
            list: annual growth for each observation.
        """
        annual_growth = [0.0] * serie.size
        for date in range(serie.size - 12):
            annual_growth[date] = (serie[date + 12] - serie[date]) / 100
        return annual_growth

    @staticmethod
    def products_from(data_path: Path) -> list:
        """
        Extracts products found from the data directory.

        Parameters:
            data_path (Path): data directory.

        Returns:
            list: products.
        """
        products = []
        for product_dir in os.listdir(data_path):
            product = Product(os.path.join(data_path, product_dir))
            products.append(product)
        return products
