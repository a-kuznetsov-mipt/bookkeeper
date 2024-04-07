"""
Основной скрипт проекта, который следует запускать,
чтобы работать с приложением через графический интерфейс.
"""
import sys

from PySide6.QtWidgets import QApplication

from bookkeeper import settings
from bookkeeper.qtgui.gui import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    main_font = app.font()
    main_font.setPointSize(settings.PYSIDE6_MAIN_FONT_SIZE)
    app.setFont(main_font)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
