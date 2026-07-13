from __future__ import annotations

class Product:
    """Класс для продуктов.

    Класс предназначен для хранения и обработки информации о продукте.

    Attributes:
        name (str): Имя продукта.
        description (str): Описание продукта.
        price (float): Цена продукта.
        quantity (int): Количество продукта на складе.
    """
    name: str
    description: str
    __price: float
    quantity: int

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ):
        """Инициализация продукта

        Args:
            name (str): Имя продукта.
            description (str): Описание продукта.
            price (float): Цена продукта.
            quantity (int): Количество продукта на складе.
        """

        self.name = name
        self.description = description

        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        """float: Возвращает текущую цену продукта."""
        return self.__price

    @price.setter
    def price(self, price):
        """Устанавливает новую цену продукта.

        Если новая цена ниже текущей, запрашивает подтверждение пользователя в консоли.
        Не позволяет установить нулевую или отрицательную цену.

        Args:
            price (float): Новая цена продукта.
        """
        if price <= 0:
            print('Цена не должна быть нулевой или отрицательной')
            return
        if price < self.__price:
            while True:
                print('Вы устанавливаете цену ниже, чем была')
                user_input = str(input('Продолжить?(Y/n)')).upper()
                if user_input == 'N':
                    return
                if user_input in ('Y', ''):
                    break
        self.__price = price
    @classmethod
    def new_product(cls, product_data: dict, products_list: list[Product] | None = None):
        """Добавляет новый продукт.

        Создает новый экземпляр класса в случае, если product_list пуст, иначе обновляет информацию о цене, описании и количестве.

        Args:
            product_data (dict): Словарь с полями 'name', 'description', 'price', 'quantity'
            products_list (list[Product]): Список с существующими экземплярами класса.

        Returns:
            Product: Экземпляр продукта.

        Raises:
            KeyError: Если Name отсутствует.
            ValueError: Если price или quantity меньше 0.
        """
        if 'name' not in product_data:
            raise KeyError("Ключ name отсутствует в словаре")
        name = product_data.get('name')
        description = product_data.get('description', '')
        price = product_data.get('price', 0)
        quantity = product_data.get('quantity', 0)
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        for product in products_list or []:
            if product.name == name:
                product.price = max(product.price, price)
                product.quantity += quantity
                product.description = description
                return product
        return cls(name, description, price, quantity)



class Category:
    name: str
    description: str
    __products: list = None
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)
    @property
    def products(self):
        return ''.join(f'{product.name}, '
                       f'{product.price} руб. '
                       f'Остаток: {product.quantity} шт.\n' for product in self.__products)
    def add_product(self, product):
        Category.product_count += 1
        self.__products.append(product)