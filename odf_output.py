from collections import defaultdict
from typing import List

from odf import text as odf_text, teletype
from odf import table as odf_table
from odf.opendocument import load as odf_load
from zipfile import BadZipFile

import irspy.clb.calibrator_constants as clb
from db_measures import Measure
import utils


class TableToDraw:
    """
    Структура для хранения выходных параметров одного Measure.Case
    """
    def __init__(self, a_case: Measure.Case):
        self.value_to_user = utils.value_to_user_with_units(clb.signal_type_to_units[a_case.signal_type])

        self.limit = self.value_to_user(a_case.limit)
        self.signal_type = clb.signal_type_to_text[a_case.signal_type]
        self.error_limit = self.value_to_user(utils.absolute_error_limit(a_normalize_value=a_case.limit,
                                                                         a_error_percent=a_case.device_class))
        self.points = defaultdict(list)

    def add_point(self, a_frequency: float, a_points_data: list):
        self.points[a_frequency].append(a_points_data)

    def __str__(self):
        return "\n".join([self.limit, self.signal_type, self.error_limit, str(self.points)])


def replace_text_in_odt(a_src_file: str, a_dst_file: str, a_marks_map: list, a_tables_to_draw: List[TableToDraw]):
    try:
        odt_file = odf_load(a_src_file)

        # Итерация по заголовкам
        __replace_text_in_odf_element(odt_file, odf_text.H, a_marks_map)

        # Итерация по остальному тексту и полям таблиц
        __replace_text_in_odf_element(odt_file, odf_text.P, a_marks_map)

        __fill_odf_table(odt_file, a_tables_to_draw)

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


def __fill_odf_table(a_file, a_tables_to_draw: List[TableToDraw]):
    for table in a_file.getElementsByType(odf_table.Table):
        for table_row in table.getElementsByType(odf_table.TableRow):
            if teletype.extractText(table_row) == "%insert_table__":

                cell_style = table_row.getElementsByType(odf_table.TableCell)[0].getAttribute("stylename")
                text_style = table_row.getElementsByType(odf_text.P)[0].getAttribute("stylename")
                row_length_in_cells = __get_table_columns_count(table)

                # Удаляем флаговую строку
                table_row.parentNode.removeChild(table_row)

                for table_to_draw in a_tables_to_draw:
                    table_header = ["Тип сигнала: " + table_to_draw.signal_type,
                                    "Предел измерения: " + table_to_draw.limit,
                                    "Допустимая погрешность: " + table_to_draw.error_limit]

                    __add_row_with_texts_to_table(table, None, cell_style, table_header, row_length_in_cells)

                    for frequency in table_to_draw.points.keys():
                        if int(frequency) != 0:
                            __add_row_with_text_to_table(table, None, cell_style,
                                                         ' '.join(["Частота:", str(frequency), "Гц"]),
                                                         row_length_in_cells)

                        for points in table_to_draw.points[frequency]:
                            points_row = __add_row_to_table(table)
                            for point in points:
                                __add_cell_to_row(points_row, cell_style, text_style, str(point))

                            for empty_cell in range(row_length_in_cells - len(points)):
                                # Чтобы пустые ячейки не мерджились в одну
                                __add_cell_to_row(points_row, cell_style, text_style, "")

                # Без этого дерево нодов сломается
                a_file.rebuild_caches(table_row.parentNode)
                break


def __add_text_to_element(a_element, a_text_style, a_text: str):
    text = odf_text.P(text=a_text)
    if a_text_style is not None:
        text.setAttribute("stylename", a_text_style)
    a_element.addElement(text)
    return a_element


def __add_row_with_text_to_table(table, text_style, cell_style, text, row_length_in_cells):
    table_row = __add_row_to_table(table)
    __add_cell_to_row(table_row, cell_style, text_style, text, row_length_in_cells)


def __add_row_with_texts_to_table(table, text_style, cell_style, texts: list, row_length_in_cells):
    """
    В __add_row_with_text_to_table нельзя вставлять переводы строки, в этой функции можно
    """
    table_row = __add_row_to_table(table)

    value_cell = odf_table.TableCell(valuetype="string")
    value_cell.setAttribute("stylename", cell_style)
    value_cell.setAttribute("numbercolumnsspanned", row_length_in_cells)
    table_row.addElement(value_cell)

    for t in texts:
        __add_text_to_element(value_cell, text_style, t)


def __get_table_columns_count(table):
    row_length_in_cells = 0
    for el in table.getElementsByType(odf_table.TableColumn):
        repeated = el.getAttribute("numbercolumnsrepeated")
        if repeated is None:
            row_length_in_cells += 1
        else:
            row_length_in_cells += int(repeated)
    return row_length_in_cells


def __add_row_to_table(table):
    table_row = odf_table.TableRow()
    table.addElement(table_row)
    return table_row


def __add_cell_to_row(row, cell_style, text_style, text: str, spanned_columns=None):
    value_cell = odf_table.TableCell(valuetype="string")
    value_cell.setAttribute("stylename", cell_style)

    if spanned_columns is not None:
        value_cell.setAttribute("numbercolumnsspanned", spanned_columns)

    row.addElement(value_cell)

    __add_text_to_element(value_cell, text_style, text)
