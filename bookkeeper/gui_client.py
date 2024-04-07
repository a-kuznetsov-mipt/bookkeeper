"""
Основной скрипт проекта, который следует запускать,
чтобы работать с приложением через графический интерфейс.
"""
import sys

import settings

if (base_dir_str := str(settings.BASE_DIR)) not in sys.path:
    sys.path.append(base_dir_str)
# Это костыль, чтобы не было ошибки ModuleNotFoundError.

from bookkeeper.view.qtgui.gui import Application


def main() -> None:
    """
    Главная функция приложения.
    """
    app = Application(sys.argv)
    app.show_main_window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
