import pytest
from src.classes import Product, Category


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
    assert category.products[0] == product
    assert category_empty.name == "Empty"
    assert category_empty.description == "None"
    assert category_empty.products == []


def test_category_count_increments():
    Category("Cat1", "desc", [])
    Category("Cat2", "desc", [])
    assert Category.category_count == 2


def test_product_count_increments(product):
    Category("Смартфоны", "desc", [product, product])
    assert Category.product_count == 2