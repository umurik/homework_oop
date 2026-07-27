from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProduct(ABC):
    name: str
    quantity: int
    __price: float

    @abstractmethod
    def __init__(self, name, price, quantity):
        self.name = name
        self.__price = price
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен!")
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. " f"Остаток: {self.quantity} шт.\n"

    @property
    def price(self):
        """float: Возвращает текущую цену продукта."""
        return self.__price

    @price.setter
    def price(self, price):
        """Устанавливает новую цену продукта.

        Если новая цена ниже текущей,
         запрашивает подтверждение пользователя в консоли.
        Не позволяет установить нулевую или отрицательную цену.

        Args:
            price (float): Новая цена продукта.
        """
        if price <= 0:
            print("Цена не должна быть нулевой или отрицательной")
            return
        if price < self.__price:
            while True:
                print("Вы устанавливаете цену ниже, чем была")
                user_input = str(input("Продолжить?(Y/n)")).upper()
                if user_input == "N":
                    return
                if user_input in ("Y", ""):
                    break
        self.__price = price


class InfoMixin:
    def __init__(self):
        print(
            f"{self.__class__.__name__}('{self.name}', '{self.description}', '{self.price}', '{self.quantity}')"
        )


class Product(BaseProduct, InfoMixin):
    """Класс для продуктов.

    Класс предназначен для хранения и обработки информации о продукте.

    Attributes:
        name (str): Имя продукта.
        description (str): Описание продукта.
        price (float): Цена продукта.
        quantity (int): Количество продукта на складе.
        color (str): Цвет продукта(необязателен).
    """

    description: str
    color: str | None

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        color: str | None = None,
    ):
        """Инициализация продукта

        Args:
            name (str): Имя продукта.
            description (str): Описание продукта.
            price (float): Цена продукта.
            quantity (int): Количество продукта на складе.
            color (str | None): Цвет продукта.
        """

        super().__init__(name, price, quantity)
        self.description = description
        self.color = color
        InfoMixin.__init__(self)

    def __add__(self, addend):
        if type(self) is not type(addend):
            raise TypeError("Невозможно сложить разные продукты!")
        total = (self.price * self.quantity) + (addend.price * addend.quantity)
        if total % 1 == 0:
            return int(total)
        return total

    @classmethod
    def new_product(
        cls, product_data: dict, products_list: list[Product] | None = None
    ):
        """Добавляет новый продукт.

        Создает новый экземпляр класса в случае, если product_list пуст,
        иначе обновляет информацию о цене, описании и количестве.

        Args:
            product_data (dict): Словарь с полями 'name',
            'description', 'price', 'quantity'
            products_list (list[Product]):
            Список с существующими экземплярами класса.

        Returns:
            Product: Экземпляр продукта.

        Raises:
            KeyError: Если Name отсутствует.
            ValueError: Если price или quantity меньше 0.
        """
        if "name" not in product_data:
            raise KeyError("Ключ name отсутствует в словаре")
        name = product_data.get("name")
        description = product_data.get("description", "")
        price = product_data.get("price", 0)
        quantity = product_data.get("quantity", 0)
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


class Smartphone(Product):
    efficiency: float
    model: str
    memory: int

    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity, color)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory


class LawnGrass(Product):
    country: str
    germination_period: str

    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity, color)
        self.country = country
        self.germination_period = germination_period


class BaseCategory(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def summ(self):
        pass


class CategoryException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = (
            args[0] if args else "Невозможно добавить товар с нулевым количеством!"
        )

    def __str__(self):
        return self.message


class Category(BaseCategory):
    name: str
    description: str
    __products: list[Product] | None = None
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        self.check_for_errors(products)
        self.name = name
        self.__products = products
        self.description = description
        Category.category_count += 1
        Category.product_count += len(products)

    def check_for_errors(self, products):
        try:
            for product in products:
                if product.quantity <= 0:
                    raise CategoryException
        except CategoryException:
            print(CategoryException())
            print("Процесс прерван.")
            raise
        else:
            print("Товар успешно добавлен.")
        finally:
            print("Обработка добавления товара завершена.")

    @property
    def products(self):
        return "".join(str(product) for product in self.__products)

    def __str__(self):
        total = 0
        for product in self.__products:
            total += product.quantity
        return f"{self.name}, количество продуктов: {total} шт."

    def middle_price(self):
        try:
            total_price = sum(product.price for product in self.__products) / len(
                self.__products
            )
        except ZeroDivisionError:
            return 0
        return round(total_price, 4)

    def summ(self):
        total = 0
        for product in self.__products:
            total += product.price * product.quantity
        return total

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Объект не является классом Product")
        try:
            if product.quantity <= 0:
                raise CategoryException
        except CategoryException:
            print(CategoryException())
            print("Процесс прерван.")
            raise
        else:
            print("Товар успешно добавлен.")
        finally:
            print("Обработка добавления товара завершена.")

        Category.product_count += 1
        self.__products.append(product)


class Order(BaseCategory):
    quantity: int
    amount: float
    product: Product

    def __init__(self, product, quantity):
        try:
            if quantity <= 0 or product.quantity <= 0:
                raise CategoryException
            self.quantity = quantity
            self.product = product
        except CategoryException:
            print(str(CategoryException()))
            print("Процесс прерван.")
            raise
        else:
            print("Товар успешно добавлен!")
        finally:
            print("Обработка добавления товара завершена.")

    @property
    def amount(self):
        return self.summ()

    def summ(self):
        amount = self.quantity * self.product.price
        if amount % 1 == 0:
            return int(amount)
        return amount

    def __str__(self):
        return f"{self.product.name}, Цена: {self.product.price}, Сумма: {self.summ()}"
