"""
Основной скрипт проекта, который следует запускать,
чтобы работать с приложением через графический интерфейс.
"""
import sys
from typing import Sequence

from PySide6.QtWidgets import QApplication

from bookkeeper import settings
from bookkeeper.view.qtgui.gui import MainWindow


class Application:
    """
    Класс, содержащий в себе объект приложения Qt и объект главного окна.
    """

    def __init__(self, argv: Sequence[str] | None = None) -> None:
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
    app = Application(sys.argv)
    app.show_main_window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
