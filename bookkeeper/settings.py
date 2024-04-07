"""
Файл настроек приложения bookkeeper.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]  # Корневая папка проекта.

PYSIDE6_MAIN_WINDOW_GEOMETRY = 200, 100, 750, 790  # Размеры главного окна приложения.
PYSIDE6_MAIN_WINDOW_TITLE = 'The Bookkeeper App'  # Заголовок главного окна приложения.
PYSIDE6_MAIN_FONT_SIZE = 14  # Размер шрифта всего приложения.
