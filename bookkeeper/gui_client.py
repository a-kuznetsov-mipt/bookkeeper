"""
Основной скрипт проекта, который следует запускать,
чтобы работать с приложением через графический интерфейс.
"""
import sys
from typing import Sequence

from PySide6.QtWidgets import QApplication

from bookkeeper import settings
from bookkeeper.qtgui.gui import MainWindow


class Application(QApplication):
    """
    Класс приложения.
    В нём происходит создание главного окна приложения.
    Так же в нём устанавливается размер шрифта для всего приложения,
    т. к. размер шрифта - один из наиболее важных параметров,
    влияющих опыт взаимодействия.
    """
    def __init__(self, argv: Sequence[str] = None) -> None:
        super().__init__(argv)
        main_font = self.font()
        main_font.setPointSize(settings.PYSIDE6_MAIN_FONT_SIZE)
        self.setFont(main_font)
        self.main_window = MainWindow()
        self.main_window.show()


def main() -> None:
    app = Application(sys.argv)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
