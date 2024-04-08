"""
В данном модуле будут описаны виджеты, используемые в графическом интерфейсе.
"""
from typing import Optional, Sequence

import PySide6.QtCore
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QTableWidget,
    QHeaderView, QApplication, QTableWidgetItem, QVBoxLayout, QTabWidget,
)

from bookkeeper import settings, utils
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class Application:
    """
    Класс, содержащий в себе объект приложения Qt и объект главного окна.
    """

    def __init__(self, argv: Sequence[str] | None = None) -> None:
        """
        argv - аргументы коммандной строки.
        """
        self.app = QApplication(argv)
        main_font = self.app.font()
        main_font.setPointSize(settings.PYSIDE6_MAIN_FONT_SIZE)
        self.app.setFont(main_font)
        self.main_window = MainWindow()

    def show_main_window(self) -> None:
        """
        Отображает главное окно
        """
        self.main_window.show()

    def exec(self) -> int:
        """
        Возвращает код возврата приложения Qt.
        Этот метод нужно выполнить для запуска приложения Qt.
        """
        return self.app.exec()


class MainWindow(QMainWindow):
    """
    Класс главного окна.
    Здесь настраивается размеры окна и его название,
    а так же создаётся главный вижет.
    Ни каких других виджетов, кроме главного,
    не создаётся в конструкторе этого класса напрямую

    Класс реализует паттерн синглтон.
    """
    signal_budgets_updated = PySide6.QtCore.Signal(list, list)
    signal_categories_updated = PySide6.QtCore.Signal(list)
    signal_expenses_updated = PySide6.QtCore.Signal(list, list)
    signal_budget_analysis_updated = PySide6.QtCore.Signal(list, list)

    __instance: 'MainWindow' = None

    def __new__(cls, parent: Optional[QWidget] = None):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__()
        geometry = settings.PYSIDE6_MAIN_WINDOW_GEOMETRY
        *_, width, height = geometry
        self.setGeometry(*geometry)
        self.setWindowTitle(settings.PYSIDE6_MAIN_WINDOW_TITLE)
        self.main_widget = MainWidget()
        self.setCentralWidget(self.main_widget)
        self.setFixedSize(width, height)

    @classmethod
    def instance(cls) -> 'MainWindow':
        return cls.__instance


class MainWidget(QWidget):
    """
    Класс главного виджета.
    Здесь создаётся раскладка (layout) и все вижеты (надписи, таблицы, кнопки и т. д.).
    """
    LAYOUT_COLUMN_STRETCHES = [1, 6, 1]
    LAYOUT_ROW_STRETCHES = [
        1,
        7,
        1,
        5,
        1,
        1,
        1,
    ]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget(self)
        self.setLayout(self._layout)
        tab_tuples = [
            (TabExpanses(self), "Последние расходы"),
            (TabCategories(self), "Категории расходов"),
            (TabBudgets(self), "Бюджеты"),
            (TabBudgetAnalysis(self), "Анализ бюджета"),
        ]
        for tab_widget, tab_title in tab_tuples:
            self.tab_widget.addTab(tab_widget, tab_title)

        self._layout.addWidget(self.tab_widget)


class TabExpanses(QWidget):
    """
    Вкладка для отображнения и управления записями о расходах.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.table_expenses = QTableWidget(10, 5)
        self.table_expenses.setHorizontalHeaderLabels(
            ['№', 'Дата', 'Сумма', 'Категория', 'Комметарий'])
        header = self.table_expenses.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            1, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            2, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            3, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            4, QHeaderView.Stretch)  # type: ignore[attr-defined]
        self.table_expenses.verticalHeader().setVisible(False)
        self._layout.addWidget(self.table_expenses)
        self.setLayout(self._layout)
        main_window = MainWindow.instance()
        main_window.signal_expenses_updated.connect(self.update_table_expenses)

    def update_table_expenses(self, expenses: list[Expense], categories: list[Category]):
        """
        expenses - список расходов, которые нужно отбразить в таблице.
        categories - список категорий. При этом нужно чтобы каждому расходу
            соответствовала категория из categories.
        """
        self.table_expenses.setRowCount(len(expenses))
        for i, expense in enumerate(expenses):
            self.table_expenses.setItem(
                i, 0, QTableWidgetItem(str(expense.pk)))
            self.table_expenses.setItem(
                i, 1, QTableWidgetItem(
                    utils.humanize_datetime(expense.expense_date)))
            self.table_expenses.setItem(
                i, 2, QTableWidgetItem(str(expense.amount)))
            self.table_expenses.setItem(
                i, 3, QTableWidgetItem(
                    categories[expense.category - 1].name.capitalize()))
            self.table_expenses.setItem(
                i, 4, QTableWidgetItem(str(expense.comment)))


class TabCategories(QWidget):
    """
    Вкладка для отображнения и управления записями о категориях расходов.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)


class TabBudgets(QWidget):
    """
    Вкладка для отображнения и управления записями о бюджетах
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.table_budgets = QTableWidget(3, 4)
        self.table_budgets.setHorizontalHeaderLabels(
            ['№', 'Срок', 'Катория', 'Сумма'])
        header = self.table_budgets.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            1, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            2, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            3, QHeaderView.Stretch)  # type: ignore[attr-defined]
        self.table_budgets.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # type: ignore[attr-defined]
        self.table_budgets.verticalHeader().setVisible(False)
        self._layout.addWidget(self.table_budgets)
        main_window = MainWindow.instance()
        main_window.signal_budgets_updated.connect(
            self.update_table_budgets)

    def update_table_budgets(
            self, budgets: list[Budget], categories: list[Category]):
        """
        budgets - список бюджетов
        categories - список категорий расходов
        """
        self.table_budgets.setRowCount(len(budgets))
        for i, budget in enumerate(budgets):
            budgets_sum: int
            expenses_sum: int
            self.table_budgets.setItem(
                i, 0, QTableWidgetItem(str(budget.pk)))
            self.table_budgets.setItem(
                i, 1, QTableWidgetItem(budget.period))
            self.table_budgets.setItem(
                i, 2, QTableWidgetItem(categories[budget.category - 1].name))
            self.table_budgets.setItem(
                i, 3, QTableWidgetItem(str(budget.amount)))


class TabBudgetAnalysis(QWidget):
    """
    Вкладка для анализа бюджета.

    Представление данных в этой вкладке - задача ПРЕДСТАВЛЕНИЯ.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        self.table_budget_analysis = QTableWidget(3, 2)
        self.table_budget_analysis.setHorizontalHeaderLabels(['Сумма', 'Бюджет'])
        self.table_budget_analysis.setVerticalHeaderLabels(['День', 'Неделя', 'Месяц'])
        self.table_budget_analysis.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # type: ignore[attr-defined]
        self.table_budget_analysis.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # type: ignore[attr-defined]
        self._layout.addWidget(self.table_budget_analysis)
        main_window = MainWindow.instance()
        main_window.signal_budget_analysis_updated.connect(
            self.update_table_budget_analysis)

    def update_table_budget_analysis(
            self, budgets_sums: list[int], expenses_sums: list[int]):
        """
        Представление данных в этой таблице - задача ПРЕДСТАВЛЕНИЯ.

        budgets - список бюджетов
        expenses_sums - список сумм расходов
            каждая сумма должна соответствовать своему бюджету
            (т. е. посчитана за тот же период)
        """
        (budgets_sum_dayly,
         budgets_sum_weeky,
         budgets_sum_monthly, *_) = budgets_sums  # *_ - на всякий случай, чтобы не упало.

        (expenses_sum_dayly,
         expenses_sum_weekly,
         expenses_sum_monthly, *_) = expenses_sums

        expenses_and_budget_sums = [
            [expenses_sum_dayly, budgets_sum_dayly],
            [expenses_sum_weekly, budgets_sum_weeky],
            [expenses_sum_monthly, budgets_sum_monthly],
        ]

        for i, (expenses_sum, budgets_sum) in enumerate(expenses_and_budget_sums):
            budgets_sum: int
            expenses_sum: int
            self.table_budget_analysis.setItem(
                i, 0, QTableWidgetItem(str(expenses_sum)))
            self.table_budget_analysis.setItem(
                i, 1, QTableWidgetItem(str(budgets_sum)))
