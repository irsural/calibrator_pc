from typing import List
import os


def build_app(a_main_filename: str, a_app_name: str, a_icon_filename: str = "", a_noconsole=True,
              a_one_file=True, a_libs: List[str] = None):

    name = " -n {}".format(a_app_name)
    onefile = " --onefile" if a_one_file else ""
    noconsole = " --noconsole" if a_noconsole else ""
    icon = " --icon={}".format(a_icon_filename) if a_icon_filename else ""
    libs_ = "".join((' --add-data "{}";.'.format(lib) for lib in a_libs)) if a_libs is not None else ""

    os.system("pyinstaller{}{}{}{}{} {}".format(name, onefile, noconsole, icon, libs_, a_main_filename))


def build_qt_app(a_main_filename: str, a_app_name: str, a_icon_filename: str = "", a_noconsole=True,
                 a_one_file=True, a_libs: List[str] = None):

    tmp_filename = "{}.py".format(a_app_name)

    with open(a_main_filename, encoding='utf8') as main_py:
        with open(tmp_filename, "w", encoding='utf8') as compile_main:
            for line in main_py:
                if not ("ui_to_py" in line):
                    compile_main.write(line)

    build_app(tmp_filename, a_app_name, a_icon_filename, a_noconsole, a_one_file, a_libs)

    os.remove(tmp_filename)


if __name__ == "__main__":
    libs = [
        'C:\\Windows\\System32\\vcruntime140d.dll',
        'C:\\Windows\\System32\\ucrtbased.dll',
        'C:\\Users\\503\\Desktop\\Python projects\\calibrator_pc\\clb_driver_dll.dll',
    ]

    build_qt_app(a_main_filename="main.py",
                 a_app_name="calibrator_pc",
                 a_icon_filename="main_icon.ico",
                 a_noconsole=True,
                 a_one_file=True,
                 a_libs=libs)
