"""
В данном модуле будут описаны виджеты, используемые в графическом интерфейсе.
"""
from typing import Optional, Sequence

import PySide6.QtCore
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QGridLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QHeaderView, QApplication, QTableWidgetItem,
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
        self._layout = QGridLayout(self)
        self.setLayout(self._layout)
        for column, stretch in enumerate(self.LAYOUT_COLUMN_STRETCHES):
            self._layout.setColumnStretch(column, stretch)
        for row, stretch in enumerate(self.LAYOUT_ROW_STRETCHES):
            self._layout.setRowStretch(row, stretch)

        self._layout.addWidget(QLabel('Последние расходы'), 0, 0, 1, 3)
        self.table_expenses = QTableWidget(10, 4)
        self.table_expenses.setHorizontalHeaderLabels(
            ['Дата', 'Сумма', 'Категория', 'Комметарий'])
        header = self.table_expenses.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            1, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            2, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            3, QHeaderView.Stretch)  # type: ignore[attr-defined]
        self.table_expenses.verticalHeader().setVisible(False)
        self._layout.addWidget(self.table_expenses, 1, 0, 1, 3)
        self._layout.addWidget(QLabel('Бюджет'), 2, 0, 1, 3)
        self.table_budgets = QTableWidget(3, 2)
        self.table_budgets.setHorizontalHeaderLabels(['Сумма', 'Бюджет'])
        self.table_budgets.setVerticalHeaderLabels(['День', 'Неделя', 'Месяц'])
        self.table_budgets.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # type: ignore[attr-defined]
        self.table_budgets.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # type: ignore[attr-defined]
        self._layout.addWidget(self.table_budgets, 3, 0, 1, 3)
        self._layout.addWidget(QLabel('Сумма расходов'), 4, 0, 1, 1)
        self._layout.addWidget(QLabel('Категория'), 5, 0, 1, 1)
        self._layout.addWidget(QLineEdit(), 4, 1, 1, 1)
        self._layout.addWidget(QComboBox(), 5, 1, 1, 1)
        self._layout.addWidget(QPushButton('Добавить'), 6, 1, 1, 1)
        self._layout.addWidget(QPushButton('Редактировать'), 5, 2, 1, 1)
        main_window = MainWindow.instance()
        main_window.signal_expenses_updated.connect(self.update_table_expenses)
        main_window.signal_budgets_updated.connect(self.update_table_budgets)

    def update_table_expenses(self, expenses: list[Expense], categories: list[Category]):
        """
        expenses - список расходов, которые нужно отбразить в таблице.
        categories - список категорий. При этом нужно чтобы каждому расходу
            соответствовала категория из categories.
        """
        self.table_expenses.setRowCount(0)
        for i, expense in enumerate(expenses):
            expense: Expense
            self.table_expenses.setItem(
                i, 0, QTableWidgetItem(
                    utils.humanize_datetime(expense.expense_date)))
            self.table_expenses.setItem(
                i, 1, QTableWidgetItem(str(expense.amount)))
            self.table_expenses.setItem(
                i, 2, QTableWidgetItem(
                    categories[expense.category].name.capitalize()))
            self.table_expenses.setItem(
                i, 3, QTableWidgetItem(str(expense.comment)))

    def update_table_budgets(self, budgets: list[Budget], expenses_sums: list[int]):
        """
        budgets - список бюджетов
        expenses_sums - список сумм расходов
            каждая сумма должна соответствовать своему бюджету
            (т. е. посчитана за тот же период)
        """
        ...
