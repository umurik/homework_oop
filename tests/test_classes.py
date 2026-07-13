from unittest.mock import patch

import pytest

from src.classes import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def product():
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый", 180000.0, 5)


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
    assert captured.out == "Цена не должна быть нулевой или отрицательной\n"


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
    product_dict = {"description": "some_description",
                    "price": 10, "quantity": 12}
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
