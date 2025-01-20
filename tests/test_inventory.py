from unittest.mock import patch

import pytest

from src.inventory import Category, IterationCategory, LawnGrass, Product, Smartphone


def test_product_init(first_product: Product, second_product: Product) -> None:
    assert first_product.name == "Samsung Galaxy S23 Ultra"
    assert first_product.description == "256GB, Серый цвет, 200MP камера"
    assert first_product.price == 180000.0
    assert first_product.quantity == 5

    assert second_product.name == "Iphone 15"
    assert second_product.description == "512GB, Gray space"
    assert second_product.price == 210000.0
    assert second_product.quantity == 8


def test_category_init(category: Category) -> None:
    assert category.name == "Смартфоны"
    assert category.description == (
        "Смартфоны, как средство не только коммуникации, " "но и получения дополнительных функций для удобства жизни"
    )
    assert category.products == (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n" "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
    )

    assert category.product_count == 2
    assert category.category_count == 1


def test_new_product(category: Category) -> None:
    new_product1 = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 11,
        }
    )

    new_product2 = Product.new_product(
        {"name": "Google Pixel 8", "description": "128GB, Розовый цвет, 50MP камера", "price": 65000.0, "quantity": 20}
    )
    assert new_product1.quantity == 16

    assert new_product2.name == "Google Pixel 8"
    assert new_product2.description == "128GB, Розовый цвет, 50MP камера"
    assert new_product2.price == 65000.0
    assert new_product2.quantity == 20


def test_category_read_json() -> None:
    category_read_json = Category.read_from_json()

    assert category_read_json[0].name == "Смартфоны"
    assert category_read_json[0].description == (
        "Смартфоны, как средство не только коммуникации, " "но и получение дополнительных функций для удобства жизни"
    )
    assert category_read_json[0].product_count == 3
    assert category_read_json[0].category_count == 2

    assert category_read_json[1].name == "Телевизоры"
    assert category_read_json[1].description == (
        "Современный телевизор, который позволяет наслаждаться просмотром, " "станет вашим другом и помощником"
    )
    assert category_read_json[1].product_count == 1
    assert category_read_json[1].category_count == 2


def test_add_category(category: Category, third_product: Product) -> None:
    category.add_product(third_product)
    assert category.products == (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
        "Google Pixel 8, 65000.0 руб. Остаток: 20 шт.\n"
    )
    assert category.product_count == 3

    try:
        category.add_product("Not a product")
    except TypeError as e:
        assert str(e) == "Вы пытаетесь добавить не продукт!!"


@pytest.mark.parametrize(
    "user_input, new_price, expected",
    [("Y", 50000.0, 50000.0), ("n", 50000.0, 65000.0), (["Да", "n"], 50000.0, 65000.0)],
)
def test_price_change(user_input: str, new_price: float, expected: float, third_product: Product) -> None:
    with patch("builtins.input", side_effect=user_input):
        third_product.price = new_price
        assert third_product.price == expected


def test_add_product(first_product: Product, second_product: Product, third_product: Product,
                     first_smartphone: Smartphone, second_smartphone: Smartphone, first_grass: LawnGrass) -> None:
    assert (first_product + second_product) == 2580000.0
    assert (first_product + third_product) == 2200000.0
    assert (second_product + third_product) == 2980000.0
    assert (first_smartphone + second_smartphone) == 2580000.0
    try:
        assert (first_smartphone + first_grass) == 910000.0
    except TypeError as e:
        assert str(e) == "Можно складывать только продукты одного класса!"


def test_str_product(first_product: Product, second_product: Product, third_product: Product) -> None:
    assert str(first_product) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
    assert str(second_product) == "Iphone 15, 210000.0 руб. Остаток: 8 шт."
    assert str(third_product) == "Google Pixel 8, 65000.0 руб. Остаток: 20 шт."


def test_str_category(category: Category) -> None:
    assert str(category) == "Смартфоны, количество продуктов: 13 шт."


def test_iteration_category(category: Category) -> None:
    iterator = IterationCategory(category)
    iter(iterator)  # Переобпределяем итер чтобы проверить что индекс сбросился на 0
    assert iterator.index == 0
    assert next(iterator).name == "Samsung Galaxy S23 Ultra"
    assert next(iterator).name == "Iphone 15"

    with pytest.raises(StopIteration):
        next(iterator)
