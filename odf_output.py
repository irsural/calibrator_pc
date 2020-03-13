from collections import defaultdict

from odf import text as odf_text, teletype
from odf import table as odf_table
from odf.opendocument import load as odf_load
from zipfile import BadZipFile

import calibrator_constants as clb
from db_measures import Measure
import utils


class TableToDraw:
    """
    Структура для хранения выходных параметров одного Measure.Case
    """
    def __init__(self, a_case: Measure.Case):
        self.value_to_user = utils.value_to_user_with_units(clb.signal_type_to_units[a_case.signal_type])

        self.limit = self.value_to_user(a_case.limit)
        self.signal_type = clb.enum_to_signal_type[a_case.signal_type]
        self.error_limit = self.value_to_user(utils.absolute_error_limit(a_normalize_value=a_case.limit,
                                                                         a_error_percent=a_case.device_class))
        self.points = defaultdict(list)

    def add_point(self, a_frequency: float, a_points_data: list):
        self.points[a_frequency].append(a_points_data)

    def __str__(self):
        return "\n".join([self.limit, self.signal_type, self.error_limit, str(self.points)])


def replace_text_in_odt(a_src_file: str, a_dst_file: str, a_marks_map: list, a_points):
    try:
        odt_file = odf_load(a_src_file)

        # Итерация по заголовкам
        __replace_text_in_odf_element(odt_file, odf_text.H, a_marks_map)

        # Итерация по остальному тексту и полям таблиц
        __replace_text_in_odf_element(odt_file, odf_text.P, a_marks_map)

        __fill_odf_table(odt_file, a_points)

        odt_file.save(a_dst_file)
        return True
    except (BadZipFile, PermissionError):
        return False


def __replace_text_in_odf_element(a_file, a_element_foo, a_replace_map: list):
    replace_map = {}
    for element in a_file.getElementsByType(a_element_foo):
        text = teletype.extractText(element)
        for mark in a_replace_map:
            text = text.replace(mark[0], mark[1])

        new_odf_element = odf_text.P()
        new_odf_element.setAttribute("stylename", element.getAttribute("stylename"))

        for space_elements in element.getElementsByType(odf_text.S):
            # Без этого все пробельные символы в начале строк удалятся
            spaces = space_elements.getAttribute('c')
            if spaces is not None:
                new_space_element = odf_text.S()
                new_space_element.setAttribute('c', spaces)
                new_odf_element.appendChild(new_space_element)

        new_odf_element.addText(text)
        replace_map[element] = new_odf_element

    for old, new in replace_map.items():
        old.parentNode.insertBefore(new, old)
        old.parentNode.removeChild(old)
        # Без этого дерево нодов сломается
        a_file.rebuild_caches(new.parentNode)


def __fill_odf_table(a_file, a_points):
    for table in a_file.getElementsByType(odf_table.Table):
        for table_row in table.getElementsByType(odf_table.TableRow):
            if teletype.extractText(table_row) == "%insert_table__":

                cell_style = table_row.getElementsByType(odf_table.TableCell)[0].getAttribute("stylename")
                text_style = table_row.getElementsByType(odf_text.P)[0].getAttribute("stylename")

                # Удаляем флаговую строку
                table_row.parentNode.removeChild(table_row)

                for row in a_points:
                    table_row = odf_table.TableRow()
                    table.addElement(table_row)
                    for value in row:
                        value_cell = odf_table.TableCell(valuetype="float")
                        value_cell.setAttribute("stylename", cell_style)

                        table_row.addElement(value_cell)
                        cell_text = odf_text.P(text=str(value))
                        cell_text.setAttribute("stylename", text_style)
                        value_cell.addElement(cell_text)

                # Без этого дерево нодов сломается
                a_file.rebuild_caches(table_row.parentNode)
                break
