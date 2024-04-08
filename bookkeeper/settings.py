"""
Файл настроек приложения bookkeeper.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]  # Корневая папка проекта.

SQLITE_DB_FILE_PATH = BASE_DIR / 'bookkeeper' / 'db.sqlite3'  # Путь до базы данных.

PYSIDE6_MAIN_WINDOW_GEOMETRY = 200, 100, 900, 790  # Размеры главного окна приложения.
PYSIDE6_MAIN_WINDOW_TITLE = 'The Bookkeeper App'  # Заголовок главного окна приложения.
PYSIDE6_MAIN_FONT_SIZE = 14  # Размер шрифта всего приложения.
