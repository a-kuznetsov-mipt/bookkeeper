import datetime

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

    TIMEDELTA_ZERO = datetime.timedelta(0)
    TIMEDELTA_DAY = datetime.timedelta(days=1)
    TIMEDELTA_WEEK = datetime.timedelta(days=7)
    TIMEDELTA_MONTH = datetime.timedelta(days=30)

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
        self.view.update_data_in_view(
            self.repository_budgets.get_all(),
            self.repository_categories.get_all(),
            self.repository_expenses.get_all(),
            self._calculate_current_budget_sums(),
            self._calculate_current_expenses_sums()
        )
        self.view.add_handler_budget_create(self._create_budget)
        self.view.add_handler_budget_update(self._update_budget)
        self.view.add_handler_budget_delete(self._delete_budget)
        self.view.add_handler_category_create(self._create_category)
        self.view.add_handler_category_update(self._update_category)
        self.view.add_handler_category_delete(self._delete_category)
        self.view.add_handler_expense_create(self._create_expense)
        self.view.add_handler_expense_update(self._update_expense)
        self.view.add_handler_expense_delete(self._delete_expense)

    def run(self) -> None:
        """
        Метод для запуска работы презентера.
        Фактически, запускает приложение.
        """
        self.view.run()

    def _calculate_current_budget_sums(self) -> list[int]:
        """
        Возвращает суммы бюджетов по категориям за день, месяц, неделю.
        """
        budgets = self.repository_budgets.get_all()
        budgets_sum_dayly = sum([budget.amount
                                 for budget in budgets
                                 if budget.period == 'день'])
        budgets_sum_weeky = sum([budget.amount
                                 for budget in budgets
                                 if budget.period == 'неделя'])
        budgets_sum_monthly = sum([budget.amount
                                   for budget in budgets
                                   if budget.period == 'месяц'])
        return [
            budgets_sum_dayly,
            budgets_sum_weeky,
            budgets_sum_monthly,
        ]

    def _calculate_current_expenses_sums(self) -> list[int]:
        """
        Возвращает суммы расходов по категориям за день, месяц, неделю.
        """
        expenses = self.repository_expenses.get_all()
        expenses_sum_dayly = 0
        expenses_sum_weeky = 0
        expenses_sum_monthly = 0
        now = datetime.datetime.now()
        for expense in expenses:
            now_to_expense_datetime_timedelta = now - expense.expense_date
            if now_to_expense_datetime_timedelta > self.TIMEDELTA_ZERO:
                if now_to_expense_datetime_timedelta < self.TIMEDELTA_DAY:
                    expenses_sum_dayly += expense.amount
                if now_to_expense_datetime_timedelta < self.TIMEDELTA_WEEK:
                    expenses_sum_weeky += expense.amount
                if now_to_expense_datetime_timedelta < self.TIMEDELTA_MONTH:
                    expenses_sum_monthly += expense.amount
        return [
            expenses_sum_dayly,
            expenses_sum_weeky,
            expenses_sum_monthly,
        ]

    def _update_data_in_view_wrapped(self):
        """
        Обёртка вокруг self.view.update_data_in_view...,
        чтобы каждый раз не писать одно и то же
        """
        self.view.update_data_in_view(
            self.repository_budgets.get_all(),
            self.repository_categories.get_all(),
            self.repository_expenses.get_all(),
            self._calculate_current_budget_sums(),
            self._calculate_current_expenses_sums()
        )

    def _create_expense(self, expense: Expense) -> None:
        """
        Создаёт запись о расходе.
        """
        self.repository_expenses.add(expense)
        self._update_data_in_view_wrapped()

    def _update_expense(self, expense: Expense) -> None:
        """
        Обноваляет запись о расходе.
        """
        self.repository_expenses.update(expense)
        self._update_data_in_view_wrapped()

    def _delete_expense(self, pk: int) -> None:
        """
        Удаляет запись о расходе по ПК.
        """
        self.repository_expenses.delete(pk)
        self._update_data_in_view_wrapped()

    def _create_category(self, category: Category) -> None:
        """
        Создаёт запись о категории.
        """
        self.repository_categories.add(category)
        self._update_data_in_view_wrapped()

    def _update_category(self, category: Category) -> None:
        """
        Обновляет запись о категории.
        """
        self.repository_categories.update(category)
        self._update_data_in_view_wrapped()

    def _delete_category(self, pk: int) -> None:
        """
        Удаляет запись о категории по ПК.
        """
        self.repository_categories.delete(pk)
        self._update_data_in_view_wrapped()

    def _create_budget(self, budget: Budget) -> None:
        """
        Создаёт запись о бюджете.
        """
        self.repository_budgets.add(budget)
        self._update_data_in_view_wrapped()

    def _update_budget(self, budget: Budget) -> None:
        """
        Обновляет запись о бюджете.
        """
        self.repository_budgets.update(budget)
        self._update_data_in_view_wrapped()

    def _delete_budget(self, pk: int) -> None:
        """
        Удаляет запись о бюджете по ПК.
        """
        self.repository_budgets.delete(pk)
        self._update_data_in_view_wrapped()
