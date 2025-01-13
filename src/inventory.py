import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Product:
    """Класс для инициализации продуктов"""

    name: str
    description: str
    price: float
    quantity: int

    created_products: list = []

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product: dict):
        created_products = Category.get_products()

        for el in created_products:
            if el.name == product["name"] and el.description == product["description"]:
                total_quantity = el.quantity + product["quantity"]
                highest_price = max(el.price, product["price"])
                return cls(product["name"], product["description"], highest_price, total_quantity)

        return cls(product["name"], product["description"], product["price"], product["quantity"])

    @property
    def price(self) -> float | int:
        return self.__price

    @price.setter
    def price(self, new_price: float | int) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        elif new_price < self.__price:
            user_answer = ""

            while user_answer.lower() != "y" and user_answer.lower() != "n":
                user_answer = input(
                    f"Новая цена ниже предыдущей, вы точно хотите изменить цену?\n" f"Введите Y(Да) или N(Нет): "
                )

            if user_answer.lower() == "y":
                self.__price = new_price
            else:
                return


class Category:
    """Класс для инициализации категорий, в том числе полученных из json файлов,
    а так же для подсчета количества продуктов и категорий"""

    name: str
    description: str
    products: list

    list_products: list = []

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products
        Category.list_products = products

        Category.category_count += 1
        self.product_count = len(products)

    def add_product(self, product):
        self.__products.append(product)
        self.product_count += 1

    @staticmethod
    def get_products() -> list:
        return Category.list_products

    @property
    def products(self) -> str:
        product_str = ""
        for el in self.__products:
            product_str += f"{el.name}, {el.price} руб. Остаток: {el.quantity} шт.\n"
        return product_str

    @staticmethod
    def read_from_json(file_path: str = "products.json") -> list:
        full_path_file_data = os.path.join(base_dir, "data", file_path)

        with open(full_path_file_data, encoding="utf-8") as file_json:
            data = json.load(file_json)

        categories_ = []

        Category.category_count = 0

        for el in data:
            cat_name = el["name"]
            cat_desc = el["description"]
            cat_products = el["products"]
            cat_obj = Category(cat_name, cat_desc, cat_products)
            categories_.append(cat_obj)

        return categories_
