import numpy as np
import math

def parse_input(a_input: str):
    if not a_input:
        return 0.
    return float(a_input)


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
