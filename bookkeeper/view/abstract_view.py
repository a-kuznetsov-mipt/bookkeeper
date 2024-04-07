from abc import ABC, abstractmethod

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class AbstractView(ABC):
    """
    Абстрактное представление.
    """
    def show_initial_condition(
            self,
            budgets: list[Budget],
            categories: list[Category],
            expenses: list[Expense],
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
    def show_expenses(self, expenses: list[Expense]) -> None:
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
    def show_budgets(self, budgets: list[Budget]) -> None:
        """
        Ввыводит данные о бюджетах в интерфейс пользователя.
        """
        ...