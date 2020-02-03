#!/usr/bin/env python

import os
from src.utils import get_project_root
from src.product import Product

class Dashboard():

    def __init__(self):
        data_dir = os.path.join(get_project_root(), 'data')
        self._products = self.products_from(data_dir)

    def products_from(self, data_dir: str) -> list:
        products = []
        for product_dir in os.listdir(data_dir):
            product = Product(os.path.join(data_dir, product_dir))
            products.append(product)
        return products
