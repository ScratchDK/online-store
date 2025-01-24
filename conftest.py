import pytest

from src.inventory import Product, Category, Smartphone, LawnGrass


@pytest.fixture
def first_product():
    return Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )


@pytest.fixture
def second_product():
    return Product("Iphone 15", "512GB, Gray space", 210000.0, 8)


@pytest.fixture
def third_product():
    return Product("Google Pixel 8", "128GB, Розовый цвет, 50MP камера", 65000.0, 20)


@pytest.fixture
def first_smartphone():
    return Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0,
        5, 95.5, "S23 Ultra", 256, "Серый"
    )


@pytest.fixture
def second_smartphone():
    return Smartphone(
        "Iphone 15", "512GB, Gray space", 210000.0,
        8, 98.2, "15", 512, "Gray space"
    )


@pytest.fixture
def first_grass():
    return LawnGrass(
        "Газонная трава", "Элитная трава для газона", 500.0,
        20, "Россия", "7 дней", "Зеленый"
    )


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
