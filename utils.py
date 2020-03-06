from linecache import checkcache, getline
from configparser import ConfigParser
from enum import IntEnum
from sys import exc_info
import math
import re

from odf import text as odf_text, teletype
from odf import table as odf_table
from odf.opendocument import load as odf_load
from zipfile import BadZipFile
import numpy as np


check_input_re = re.compile(
    r"(?P<number>^[-+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][-+]?\d+)?) *(?P<units>(?:мк|м|н)?[аАвВ]?) *$")

check_input_no_python_re = re.compile(r"^[-+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][-+]?\d+)? *(?:мк|м|н)?[аАвВ]?$")

find_number_re = re.compile(r"[-+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][-+]?\d+)?")

__units_to_factor = {
    "": 1,
    "в": 1,
    "а": 1,

    "м": 1e-3,
    "мв": 1e-3,
    "ма": 1e-3,

    "мк": 1e-6,
    "мкв": 1e-6,
    "мка": 1e-6,

    "н": 1e-9,
    "нв": 1e-9,
    "на": 1e-9,
}


class __UnitsPrefix(IntEnum):
    NANO = 0
    MICRO = 1
    MILLI = 2
    NO = 3


__enum_to_units = {
    __UnitsPrefix.NANO: "н",
    __UnitsPrefix.MICRO: "мк",
    __UnitsPrefix.MILLI: "м",
    __UnitsPrefix.NO: "",
}


def parse_input(a_input: str, a_reverse_check=False):
    if not a_input:
        return 0.
    input_re = check_input_re.match(a_input)
    if not input_re:
        raise ValueError(f"Wrong units input format: {a_input}")

    number = float(input_re.group('number').replace(",", "."))
    factor = __units_to_factor[input_re.group("units").lower()]
    result = round(number * factor, 9)

    # print(f"S->V. Input: {a_input}. Parsed: {number} {input_re.group('units').lower()}. Result: {result}")
    if a_reverse_check:
        if value_to_user_with_units("В", False)(result) != a_input:
            if value_to_user_with_units("А", False)(result) != a_input:
                str_no_units = value_to_user_with_units("", False)(result)
                if a_input != str_no_units:
                    print(f"S->V reverse check is failed: {a_input} != {str_no_units}")

    return result


def value_to_user_with_units(a_postfix: str, a_reverse_check=False):
    def value_to_user(a_value):
        prefix_type = __UnitsPrefix.NO

        abs_value = abs(a_value)
        if abs_value == 0:
            a_value = 0
            prefix_type = __UnitsPrefix.NO
        elif abs_value < 1e-9:
            a_value = 0
            prefix_type = __UnitsPrefix.NANO
        elif abs_value < 1e-6:
            a_value *= 1e9
            prefix_type = __UnitsPrefix.NANO
        elif abs_value < 1e-3:
            a_value *= 1e6
            prefix_type = __UnitsPrefix.MICRO
        elif abs_value < 1:
            a_value *= 1e3
            prefix_type = __UnitsPrefix.MILLI
        result = round(a_value, 9)
        result_str = float_to_string(result)
        result_with_units = f"{result_str} {__enum_to_units[prefix_type]}{a_postfix}"

        # print(f"V->S. Input: {a_value}. Output: {result_str}")
        if a_reverse_check:
            parsed = parse_input(result_with_units, False)
            if result != parsed:
                print(f"V->S reverse check is failed: {result} != {parsed}")

        return result_with_units
    return value_to_user


def float_to_string(a_number: float):
    return f"{a_number:.9f}".rstrip('0').rstrip('.').replace(".", ",")


def absolute_error(a_reference: float, a_value: float):
    return a_reference - a_value


def relative_error(a_reference: float, a_value: float, a_normalize: float):
    assert a_normalize != 0, "Normalize value must not be zero"
    return (a_reference - a_value) / a_normalize * 100


def variation(a_lval: float, a_rval: float):
    return abs(a_lval - a_rval)


def auto_calc_points(a_start: float, a_stop: float, a_step: float):
    if a_start == a_stop or a_step == 0:
        return []
    if a_stop < a_start:
        a_step *= -1

    points = np.arange(a_start, a_stop, a_step)
    points = np.append(a_stop, points)
    sorted_list = (-np.sort(-points)).tolist()
    rounded_list = [round(elem, 9) for elem in sorted_list]
    return rounded_list


def bound(a_value, a_min, a_max):
    return max(min(a_value, a_max), a_min)


def relative_step_change(a_value: float, a_step: float, a_min_step: float, a_normalize_value=None):
    value_sign = 1 if a_step >= 0 else -1
    if a_value == 0:
        return a_min_step * value_sign

    if not a_normalize_value:
        a_normalize_value = a_value

    absolute_step = abs(a_normalize_value * a_step)
    exp = int(math.floor(math.log10(absolute_step)))

    absolute_step /= pow(10., exp)

    def get_new_step(x, y):
        return x if absolute_step < math.sqrt(x * y) else y

    if absolute_step <= 2:
        new_step = 1 if absolute_step < math.sqrt(1 * 2) else 2
        test_step = get_new_step(1, 2)
    elif absolute_step < 5:
        new_step = 2 if absolute_step < math.sqrt(2 * 5) else 5
        test_step = get_new_step(2, 5)
    else:
        new_step = 5 if absolute_step < math.sqrt(5 * 10) else 10
        test_step = get_new_step(5, 10)

    assert new_step == test_step, f"new: {new_step}, test: {test_step}. dont work"

    new_step *= pow(10., exp)
    new_step: float = max(new_step, a_min_step)
    a_value += new_step * value_sign

    # Если это преобразование убрать, то шаг будет равномерным на любой амплитуде
    finish_value = math.ceil(a_value / new_step) * new_step if value_sign > 0 \
        else math.floor(a_value / new_step) * new_step

    return finish_value


def increase_by_percent(a_value, a_percent, a_normalize_value=None):
    normalize = a_normalize_value if a_normalize_value else a_value
    return a_value + abs(normalize) * a_percent / 100


def decrease_by_percent(a_value, a_percent, a_normalize_value=None):
    normalize = a_normalize_value if a_normalize_value else a_value
    return a_value - abs(normalize) * a_percent / 100


def save_settings(a_path: str, a_config: ConfigParser):
    with open(a_path, 'w') as config_file:
        a_config.write(config_file)


def calc_smooth_approach(a_from, a_to, a_count, a_dt, sigma=0.01):
    """
    Вычисляет экспоненциальное изменение величины во времени от a_from до a_to с ассимптотическим подходом к a_to
    :param a_from: Стартовое значение
    :param a_to: Конечное значение
    :param a_count: Количество точек между a_from и a_to
    :param a_dt: Дискрет времени, с которым должна изменяться величина
    :param sigma: Кэффициент плавного подхода. Чем меньше, там плавнее будет подход к a_to и тем резче будет
                  скачок в начале
    :return: Список точек, размером a_count
    """
    dt_stop = a_dt * a_count
    dt_stop_s = dt_stop / 1000
    a_k = -1 / dt_stop_s * math.log(sigma)

    delta = abs(a_from - a_to)
    slope = delta / (1 - math.e ** (-a_k * dt_stop_s))

    points = []
    for t in range(a_dt, dt_stop + a_dt, a_dt):

        point = a_from + slope * (1 - math.e**(-a_k * t / 1000)) if a_from < a_to else \
            a_from + slope * (math.e ** (-a_k * t / 1000) - 1)

        points.append(round(point, 9))

    return points


def exception_handler(a_exception):
    e_type, e_obj, e_tb = exc_info()
    frame = e_tb.tb_frame
    lineno = e_tb.tb_lineno
    filename = frame.f_code.co_filename
    checkcache(filename)
    line = getline(filename, lineno, frame.f_globals)
    print(f"Exception{type(a_exception)} in {filename}\n"
          f"Line {lineno}: '{line.strip()}'\n"
          f"Message: {a_exception}")


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
