import pytest

from src.inventory import Product, Category


@pytest.fixture
def first_product():
    return Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )


@pytest.fixture
def second_product():
    return Product("Iphone 15", "512GB, Gray space", 210000.0, 8)


@pytest.fixture
def category():
    return Category("Смартфоны",
                    "Смартфоны, как средство не только коммуникации,"
                    " но и получения дополнительных функций для удобства жизни",
                    [
                        Product(
                            "Samsung Galaxy S23 Ultra",
                            "256GB, Серый цвет, 200MP камера",
                            180000.0, 5
                        ),
                        Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
                    ])
