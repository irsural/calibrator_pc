import ui_to_py
ui_to_py.convert_ui("./ui", "./ui/py")

from mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)

    translator = QtCore.QTranslator(app)
    path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("/".join([path, "qtbase_ru.qm"]))
    app.installTranslator(translator)

    w = MainWindow()
    sys.exit(app.exec_())
