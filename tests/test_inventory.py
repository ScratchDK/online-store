from src.inventory import Category


def test_product_init(first_product, second_product) -> None:
    assert first_product.name == "Samsung Galaxy S23 Ultra"
    assert first_product.description == "256GB, Серый цвет, 200MP камера"
    assert first_product.price == 180000.0
    assert first_product.quantity == 5

    assert second_product.name == "Iphone 15"
    assert second_product.description == "512GB, Gray space"
    assert second_product.price == 210000.0
    assert second_product.quantity == 8


def test_category_init(category) -> None:
    assert category.name == "Смартфоны"
    assert category.description == (
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни"
    )
    assert len(category.products) == 2

    assert category.product_count == 2
    assert category.category_count == 1


def test_category_read_json() -> None:
    category_read_json = Category.read_from_json()

    assert category_read_json[0].name == "Смартфоны"
    assert category_read_json[0].description == (
        "Смартфоны, как средство не только коммуникации, "
        "но и получение дополнительных функций для удобства жизни"
    )
    assert len(category_read_json[0].products) == 3
    assert category_read_json[0].product_count == 3
    assert category_read_json[0].category_count == 2

    assert category_read_json[1].name == "Телевизоры"
    assert category_read_json[1].description == (
        "Современный телевизор, который позволяет наслаждаться просмотром, "
        "станет вашим другом и помощником"
    )
    assert len(category_read_json[1].products) == 1
    assert category_read_json[1].product_count == 1
    assert category_read_json[1].category_count == 2
