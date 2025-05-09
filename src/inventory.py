import json
import os
from typing import Any

from src.abstractions import BaseEntity, BaseProduct
from src.custom_exceptions import ZeroQuantityError
from src.mixin import PrintMixin

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Product(BaseProduct, PrintMixin):
    """Класс для инициализации продуктов"""

    name: str
    description: str
    __price: float
    quantity: int

    created_products: list = []

    def __init__(self, name: str, description: str, price: float, quantity: int):

        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен!")

        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__()

    def __eq__(self, other: Any) -> Any:
        if isinstance(other, Product):
            return (self.name == other.name and
                    self.description == other.description and
                    self.price == other.price and
                    self.quantity == other.quantity)
        return False

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> Any:
        if type(other) is self.__class__:
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Можно складывать только продукты одной группы!")

    @classmethod
    def new_product(cls, product: dict) -> Any:
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


class Smartphone(Product):
    """Дочерний класс для инициализации смартфонов"""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Дочерний класс для инициализации газонов"""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category(BaseEntity):
    """Класс для инициализации категорий, в том числе полученных из json файлов,
    а так же для подсчета количества продуктов и категорий"""

    name: str
    description: str
    __products: list

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

    def middle_price(self) -> Any:
        total_price = sum(el.price for el in self.__products)
        total_quantity = sum(el.quantity for el in self.__products)

        try:
            result = round(total_price / total_quantity, 2)
        except ZeroDivisionError:
            return 0
        else:
            return result

    def add_product(self, product: Any) -> None:
        if issubclass(product.__class__, Product) is False:
            raise TypeError("Вы пытаетесь добавить не продукт!!")
        self.__products.append(product)
        self.product_count += 1

    @staticmethod
    def get_products() -> list:
        return Category.list_products

    def __str__(self) -> str:
        total_number = 0
        for el in self.__products:
            total_number += el.quantity
        return f"{self.name}, количество продуктов: {total_number} шт."

    @property
    def products(self) -> str:
        product_str = ""
        for el in self.__products:
            product_str += f"{str(el)}\n"
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


class IterationCategory:
    """Класс позволяет перебирать продукты одной категорий"""

    def __init__(self, cat_obj: Any) -> None:
        self.cat = cat_obj
        self.index = 0

    def __iter__(self) -> Any:
        self.index = 0
        return self

    def __next__(self) -> Any:
        if self.index < len(self.cat.list_products):
            product = self.cat.list_products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration


class Order(BaseEntity):
    def __init__(self, name: str, quantity: int, price: float):
        try:
            if quantity <= 0:
                raise ZeroQuantityError
        except ZeroQuantityError as e:
            print(str(e))
        else:
            print("Списание товара прошло успешно!")
        finally:
            print("Обработка товара завершена!")

        self.products = Category.get_products()
        self.name = name
        self.quantity = self.__check_quantity(quantity)
        self.total_price = price * quantity if type(self.quantity) is int else 0

    def __check_quantity(self, quantity: int) -> int | str:
        for el in self.products:
            if self.name == el.name and quantity <= el.quantity:
                el.quantity -= quantity
                return quantity
        return "Не возможно списать товар так как количество списываемого товара превышает количество в наличии!"

    def __str__(self) -> str:
        return f"Заказ: {self.name}, Количество: {self.quantity}, Итоговая стоимость: {self.total_price}"

    def get_products(self) -> list:
        return self.products
