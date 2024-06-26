"""
Основной скрипт проекта, который следует запускать,
чтобы работать с приложением через графический интерфейс.
"""
import sys
import traceback

import settings

if (base_dir_str := str(settings.BASE_DIR)) not in sys.path:
    sys.path.append(base_dir_str)
# Это костыль, чтобы не было ошибки ModuleNotFoundError.

from bookkeeper import utils
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.presenter.bookkeeper import BookkeeperPresenter
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.qtgui_view import QtGUIView


def main() -> None:
    """
    Главная функция приложения.
    """
    repository_budgets = MemoryRepository[Budget]()
    repository_categories = MemoryRepository[Category]()
    repository_expenses = MemoryRepository[Expense]()

    cats = '''
    продукты
        мясо
            сырое мясо
            мясные продукты
        сладости
    книги
    одежда
    '''.splitlines()

    Category.create_from_tree(utils.read_tree(cats), repository_categories)
    repository_expenses.add(Expense(category=1, amount=1714, comment='Гречка'))
    repository_expenses.add(Expense(category=4, amount=199914, comment='Пельмени'))

    repository_budgets.add(Budget(period='день', amount=100, category=6))
    repository_budgets.add(Budget(period='неделя', amount=700, category=6))
    repository_budgets.add(Budget(period='месяц', amount=3000, category=6))
    repository_budgets.add(Budget(period='день', amount=200, category=7))
    repository_budgets.add(Budget(period='неделя', amount=1400, category=7))
    repository_budgets.add(Budget(period='месяц', amount=6000, category=7))

    view = QtGUIView()
    bookkeeper_presenter = BookkeeperPresenter(
        repository_budgets,
        repository_categories,
        repository_expenses,
        view,
    )
    bookkeeper_presenter.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'Произошла ошибка ({exc}), обратитесь к разработчику:')
        print(''.join(traceback.format_exception(exc)))
