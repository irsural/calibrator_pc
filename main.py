from irspy.qt import ui_to_py
ui_to_py.convert_ui("./ui", "./ui/py")
ui_to_py.convert_resources("./resources", ".")


def main():
    import sys
    
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QApplication
    
    from mainwindow import MainWindow

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    translator = QtCore.QTranslator(app)
    path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("/".join([path, "qtbase_ru.qm"]))
    app.installTranslator(translator)

    w = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        import traceback
        main()
    except Exception as err:
        print(traceback.format_exc())
