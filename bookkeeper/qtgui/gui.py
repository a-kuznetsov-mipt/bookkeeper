"""
В данном модуле будут описаны виджеты, используемые в графическом интерфейсе.
"""

from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QGridLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QHeaderView,
)

from bookkeeper import settings


class MainWindow(QMainWindow):
    """
    Класс главного окна.
    Здесь настраивается размеры окна и его название,
    а так же создаётся главный вижет.
    Ни каких других виджетов, кроме главного,
    не создаётся в конструкторе этого класса напрямую
    """
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        geometry = settings.PYSIDE6_MAIN_WINDOW_GEOMETRY
        *_, width, height = geometry
        self.setGeometry(*geometry)
        self.setWindowTitle(settings.PYSIDE6_MAIN_WINDOW_TITLE)
        self.setCentralWidget(MainWidget())
        self.setFixedSize(width, height)


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
        table_last_expenses = QTableWidget(10, 4)
        table_last_expenses.setHorizontalHeaderLabels(
            ['Дата', 'Сумма', 'Категория', 'Комметарий'])
        header = table_last_expenses.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            1, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            2, QHeaderView.ResizeToContents)  # type: ignore[attr-defined]
        header.setSectionResizeMode(
            3, QHeaderView.Stretch)  # type: ignore[attr-defined]
        table_last_expenses.verticalHeader().setVisible(False)
        self._layout.addWidget(table_last_expenses, 1, 0, 1, 3)
        self._layout.addWidget(QLabel('Бюджет'), 2, 0, 1, 3)
        table_budget = QTableWidget(3, 2)
        table_budget.setHorizontalHeaderLabels(['Сумма', 'Бюджет'])
        table_budget.setVerticalHeaderLabels(['День', 'Неделя', 'Месяц'])
        table_budget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # type: ignore[attr-defined]
        table_budget.verticalHeader().setSectionResizeMode(
            QHeaderView.Stretch)  # type: ignore[attr-defined]
        self._layout.addWidget(table_budget, 3, 0, 1, 3)
        self._layout.addWidget(QLabel('Сумма'), 4, 0, 1, 1)
        self._layout.addWidget(QLabel('Категория'), 5, 0, 1, 1)
        self._layout.addWidget(QLineEdit(), 4, 1, 1, 1)
        self._layout.addWidget(QComboBox(), 5, 1, 1, 1)
        self._layout.addWidget(QPushButton('Добавить'), 6, 1, 1, 1)
        self._layout.addWidget(QPushButton('Редактировать'), 5, 2, 1, 1)
