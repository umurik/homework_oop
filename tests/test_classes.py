from unittest.mock import patch

import pytest

from src.classes import (Category, CategoryException, LawnGrass, Order,
                         Product, Smartphone)


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def product():
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый", 180000.0, 5)


@pytest.fixture
def phone():
    return Smartphone(
        "new_phone", "new_description", 1501, 12, 4444, "S24", 256, "яблочный"
    )


@pytest.fixture
def grass1():
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


def test_product_fields(product):
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.quantity == 5
    assert product.description == "256GB, Серый"
    assert product.price == 180000.0


def test_category_fields(product):
    category = Category("Смартфоны", "описание", [product])
    category_empty = Category("Empty", "None", [])
    assert category.name == "Смартфоны"
    assert category.description == "описание"
    assert (
        category.products == "Samsung Galaxy S23 Ultra, "
        "180000.0 руб. Остаток: 5 шт.\n"
    )
    assert category_empty.name == "Empty"
    assert category_empty.description == "None"
    assert category_empty.products == ""


def test_category_count_increments():
    Category("Cat1", "desc", [])
    Category("Cat2", "desc", [])
    assert Category.category_count == 2


def test_product_count_increments(product):
    Category("Смартфоны", "desc", [product, product])
    assert Category.product_count == 2


def test_setter_price_minus_product(capsys):
    product = Product("name", "description", -22, 1)
    product.price = -11
    captured = capsys.readouterr()
    assert (
        captured.out == "Product('name', 'description', '-22', '1')\n"
        "Цена не должна быть нулевой или отрицательной\n"
    )


def test_setter_decreasing_product(capsys):
    product = Product("name", "description", 12, 1)
    with (
        patch("builtins.input", return_value="Y") as mock_input,
        patch("builtins.print") as mock_print,
    ):
        product.price = 11
        mock_print.assert_called_once_with("Вы устанавливаете цену ниже, чем была")
        mock_input.assert_called_once_with("Продолжить?(Y/n)")
        assert product.price == 11
    product = Product("name", "description", 190, 1)
    with (
        patch("builtins.input", return_value="n") as mock_input,
        patch("builtins.print") as mock_print,
    ):
        product.price = 11
        mock_print.assert_called_once_with("Вы устанавливаете цену ниже, чем была")
        mock_input.assert_called_once_with("Продолжить?(Y/n)")
        assert product.price == 190


def test_new_product_product(product):
    product_dict = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый",
        "price": 18666000.0,
        "quantity": 5,
    }
    list_product = [product]
    prod1 = Product.new_product(product_dict, list_product)
    new_prod = Product.new_product(product_dict)
    assert prod1.price == product_dict["price"]
    assert prod1.name == product_dict["name"]
    assert prod1.description == product_dict["description"]
    assert prod1.quantity == product_dict["quantity"] + 5
    assert product_dict["name"] == new_prod.name
    assert product_dict["description"] == new_prod.description
    assert product_dict["price"] == new_prod.price
    assert product_dict["quantity"] == new_prod.quantity


def test_new_product_errors_product():
    product_dict = {"description": "some_description", "price": 10, "quantity": 12}
    with pytest.raises(KeyError) as exc_info:
        Product.new_product(product_dict)
    assert "Ключ name отсутствует в словаре" in str(exc_info.value)
    product_dict["name"] = "some_name"
    with pytest.raises(ValueError) as exc_info:
        product_dict["price"] = -12
        Product.new_product(product_dict)
    assert "Цена не может быть отрицательной" in str(exc_info.value)
    with pytest.raises(ValueError) as exc_info:
        product_dict["price"] = 1222
        product_dict["quantity"] = -1
        Product.new_product(product_dict)
    assert "Количество не может быть отрицательным" in str(exc_info.value)


def test_add_product(product):
    total = product + product
    assert total == 1800000


def test_str_product(product):
    assert str(product) == (
        "Samsung Galaxy S23 Ultra, " "180000.0 руб. Остаток: 5 шт.\n"
    )


def test_str_category(product):
    cat = Category("name", "description", [product, product])
    assert str(cat) == "name, количество продуктов: 10 шт."


def test_smartphones(phone):
    assert "new_phone" == phone.name
    assert "new_description" == phone.description
    assert 1501 == phone.price
    assert 12 == phone.quantity
    assert 4444 == phone.efficiency
    assert "S24" == phone.model
    assert 256 == phone.memory
    assert "яблочный" == phone.color


def test_lawngrass(grass1):
    assert "Газонная трава" == grass1.name
    assert "Элитная трава для газона" == grass1.description
    assert 500.0 == grass1.price
    assert 20 == grass1.quantity
    assert "Россия" == grass1.country
    assert "7 дней" == grass1.germination_period
    assert "Зеленый" == grass1.color


def test_add_bad_product(phone, grass1):
    with pytest.raises(TypeError) as exc_info:
        new_bad_thing = phone + grass1
    assert "Невозможно сложить разные продукты!" == str(exc_info.value)


def test_order(product):
    new_order = Order(product, 123)
    assert product == new_order.product
    assert 123 == new_order.quantity
    assert 22140000 == new_order.amount
    assert 22140000 == new_order.summ()
    assert "Samsung Galaxy S23 Ultra, Цена: 180000.0, Сумма: 22140000" == str(new_order)


def test_exceptions():
    with pytest.raises(CategoryException) as exc_info:
        me = Product("na", "w", "122", 12)
        me.quantity = 0
        Category("имя", "ьы", products=[me])
    assert "Невозможно добавить товар с нулевым количеством!" == str(exc_info.value)

    with pytest.raises(CategoryException) as exc_info:
        me = Product("na", "w", "122", 12)
        me.quantity = 0
        Order(me, 122)
    assert "Невозможно добавить товар с нулевым количеством!" == str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        Product("smn", "description", 12212, 0)
    assert "Товар с нулевым количеством не может быть добавлен!" == str(exc_info.value)


def test_middle_price():
    product1 = Product("m", "a", 12, 12)
    cat1 = Category("n", "as", [product1])
    assert 12 == cat1.middle_price()
    cat2 = Category("n", "as", [])
    assert 0 == cat2.middle_price()
