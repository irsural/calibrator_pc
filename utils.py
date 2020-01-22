import numpy as np
import math
import re
import enum


# __check_input_re = re.compile(r"^[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)? *(?:мк|м|н)?[аАвВ]?$")

__check_input_re = re.compile(
    r"(?P<number>^[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?) *(?P<units>(?:мк|м|н)?[аАвВ]?$)")

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


class __UnitsPrefix(enum.IntEnum):
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
    input_re = __check_input_re.match(a_input)
    if not input_re:
        raise ValueError(f"Wrong units input format: {a_input}")

    number = float(input_re.group('number'))
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
        result_str = remove_tail_zeroes(f"{result:.9f}")
        result_with_units = f"{result_str} {__enum_to_units[prefix_type]}{a_postfix}"

        # print(f"V->S. Input: {a_value}. Output: {result_str}")
        if a_reverse_check:
            parsed = parse_input(result_with_units, False)
            if result != parsed:
                print(f"V->S reverse check is failed: {result} != {parsed}")

        return result_with_units
    return value_to_user


def remove_tail_zeroes(a_string_num: str):
    return a_string_num.rstrip('0').rstrip('.')


def deviation(a_lval: float, a_rval: float):
    if a_lval == 0 or a_rval == 0:
        return 0
    return (a_lval - a_rval) / a_lval * 100


def auto_calc_points(a_start: float, a_stop: float, a_step:float):
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


def relative_step_change(a_value, a_step):
    absolute_step = abs(a_value * a_step)
    exp = int(math.floor(math.log10(absolute_step)))

    absolute_step /= pow(10., exp)
    get_new_step = lambda x, y: x if absolute_step < math.sqrt(x * y) else y

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
    sign = 1 if a_step >= 0 else -1
    a_value += new_step * sign

    finish_value = math.ceil(a_value / new_step) * new_step if sign > 0 \
        else math.floor(a_value / new_step) * new_step

    return finish_value


def increase_on_percent(a_value, a_percent):
    return a_value + a_value * a_percent / 100


def reduce_on_percent(a_value, a_percent):
    return a_value - a_value * a_percent / 100
