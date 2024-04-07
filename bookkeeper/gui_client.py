"""
Основной скрипт проекта, который следует запускать,
чтобы работать с приложением через графический интерфейс.
"""
import sys

import settings
if (base_dir_str := str(settings.BASE_DIR)) not in sys.path:
    sys.path.append(base_dir_str)
# Это костыль, чтобы не было ошибки ModuleNotFoundError.

from typing import Sequence

from PySide6.QtWidgets import QApplication

from bookkeeper import settings
from bookkeeper.view.qtgui.gui import MainWindow


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
        self.main_window.show()

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


def main() -> None:
    """
    Главная функция приложения.
    """
    app = Application(sys.argv)
    app.show_main_window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
