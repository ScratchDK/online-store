import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Product:

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:

    name: str
    description: str
    products: list

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        self.product_count = len(products)

    @staticmethod
    def read_from_json(file_path: str = "products.json") -> list:
        full_path_file_data = os.path.join(base_dir, "data", file_path)

        with open(full_path_file_data, encoding="utf-8") as file_json:
            data = json.load(file_json)

        categories_ = []

        for el in data:
            cat_name = el["name"]
            cat_desc = el["description"]
            cat_products = el["products"]
            cat_obj = Category(cat_name, cat_desc, cat_products)
            categories_.append(cat_obj)

        return categories_
