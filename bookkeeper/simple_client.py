"""
Простой тестовый скрипт для терминала
"""
import sys

import settings
if (base_dir_str := str(settings.BASE_DIR)) not in sys.path:
    sys.path.append(base_dir_str)
# Это костыль, чтобы не было ошибки ModuleNotFoundError.

from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.utils import read_tree

bud_repo = MemoryRepository[Budget]()
cat_repo = MemoryRepository[Category]()
exp_repo = MemoryRepository[Expense]()

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    elif cmd == 'бюджет':
        print(*bud_repo.get_all(), sep='\n')
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
