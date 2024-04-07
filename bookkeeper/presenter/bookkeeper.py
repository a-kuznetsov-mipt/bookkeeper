from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.view.abstract_view import AbstractView


class BookkeeperPresenter:
    """
    Класс презентера.
    Связующее звено между репозиторием и представлением.
    """
    def __init__(
            self,
            repository_budgets: AbstractRepository[Budget],
            repository_categories: AbstractRepository[Category],
            repository_expenses: AbstractRepository[Expense],
            view: AbstractView,
    ) -> None:
        self.repository_budgets = repository_budgets
        self.repository_categories = repository_categories
        self.repository_expenses = repository_expenses
        self.view = view
        self.view.show_initial_condition(
            self.repository_budgets.get_all(),
            self.repository_categories.get_all(),
            self.repository_expenses.get_all(),
        )

    def run(self) -> None:
        """
        Метод для запуска работы презентера.
        Фактически, запускает приложение.
        """
        self.view.run()
