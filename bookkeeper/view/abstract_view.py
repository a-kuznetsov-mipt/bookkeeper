from abc import ABC, abstractmethod
from typing import Callable

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class AbstractView(ABC):
    """
    Абстрактное представление.
    """
    def update_data_in_view(
            self,
            budgets: list[Budget],
            categories: list[Category],
            expenses: list[Expense],
            budgets_sums: list[int],
            expenses_sums: list[int],
    ) -> None:
        """
        Выводит данные из репозиториев в начале работы программы.
        Какие именно данные выводить и воводить ли вообще
        - вопрос конкретной реализации (конкретного дизайна UI).
        """
        ...

    @abstractmethod
    def run(self) -> None:
        """
        Метод запускает представление для взаимодействия с пользователем.
        """

    @abstractmethod
    def show_expenses(self, expenses: list[Expense], categories: list[Category]) -> None:
        """
        Ввыводит данные о расходах в интерфейс пользователя.
        """
        ...

    @abstractmethod
    def show_categories(self, categories: list[Category]) -> None:
        """
        Ввыводит данные о категориях в интерфейс пользователя.
        """
        ...

    @abstractmethod
    def show_budgets(self, budgets: list[Budget], categories: list[Category]) -> None:
        """
        Ввыводит данные о бюджетах в интерфейс пользователя.
        """
        ...

    @abstractmethod
    def show_budget_analysis(self, budgets_sums: list[int], expenses_sums: list[int]) -> None:
        """
        Ввыводит данные об анализе бюджета в интерфейс пользователя.
        """
        ...

    def add_handler_expense_create(self, handler: Callable[[Expense], None]) -> None:
        """
        Добавляет обработчик запроса на создание записи о расходах.
        """
        ...

    def add_handler_expense_update(self, handler: Callable[[Expense], None]) -> None:
        """
        Добавляет обработчик запроса на изменение записи о расходах.
        """
        ...

    def add_handler_expense_delete(self, handler: Callable[[int], None]) -> None:
        """
        Добавляет обработчик запроса на удаление записи о расходах.
        """
        ...

    def add_handler_budget_create(self, handler: Callable[[Budget], None]) -> None:
        """
        Добавляет обработчик запроса на создание записи о бюджете.
        """
        ...

    def add_handler_budget_update(self, handler: Callable[[Budget], None]) -> None:
        """
        Добавляет обработчик запроса на изменение записи о бюджете.
        """
        ...

    def add_handler_budget_delete(self, handler: Callable[[int], None]) -> None:
        """
        Добавляет обработчик запроса на удаление записи о бюджете.
        """
        ...

    def add_handler_category_create(self, handler: Callable[[Category], None]) -> None:
        """
        Добавляет обработчик запроса на создание записи о категории расходов
        """
        ...

    def add_handler_category_update(self, handler: Callable[[Category], None]) -> None:
        """
        Добавляет обработчик запроса на изменение записи о категории расходов
        """
        ...

    def add_handler_category_delete(self, handler: Callable[[int], None]) -> None:
        """
        Добавляет обработчик запроса на удаление записи о категории расходов
        """
        ...
