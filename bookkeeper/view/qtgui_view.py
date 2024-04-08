import sys

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.view.abstract_view import AbstractView
from bookkeeper.view.qtgui.gui import Application, MainWindow


class QtGUIView(AbstractView):
    """
    Реализует представление с помощью библиотеки PySide6.
    """
    def __init__(self):
        self.application = Application(sys.argv)
        self.main_window = MainWindow.instance()

    def update_data_in_view(
            self,
            budgets: list[Budget],
            categories: list[Category],
            expenses: list[Expense],
            budgets_sums: list[int],
            expenses_sums: list[int],
    ) -> None:
        self.show_expenses(expenses, categories)
        self.show_budgets(budgets, categories)
        self.show_budget_analysis(budgets_sums, expenses_sums)

    def run(self) -> None:
        self.application.show_main_window()
        self.application.exec()

    def show_expenses(self, expenses: list[Expense], categories: list[Category]) -> None:
        self.main_window.signal_expenses_updated.emit(expenses, categories)

    def show_categories(self, categories: list[Category]) -> None:
        self.main_window.signal_categories_updated.emit(categories)

    def show_budgets(self, budgets: list[Budget], categories: list[Category]) -> None:
        self.main_window.signal_budgets_updated.emit(budgets, categories)

    def show_budget_analysis(
            self, budgets_sums: list[int], expenses_sums: list[int]) -> None:
        self.main_window.signal_budget_analysis_updated.emit(budgets_sums, expenses_sums)


