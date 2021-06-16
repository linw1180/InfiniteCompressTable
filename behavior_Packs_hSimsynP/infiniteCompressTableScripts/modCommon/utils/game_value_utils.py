# -*- coding: utf-8 -*-
import random


def get_probability_results(value):
    return random.random() < value


def get_max_rep_exp(rep_lv):
    return pow(int(rep_lv), 2) * 2 + 15


def get_rep_lv_grade(rep_lv):
    return int(rep_lv) / 10 if rep_lv < 50 else 4


def get_san_grade(san):
    return int(san) / 20 if san < 100 else 4


def random_pick(pick_list):
    """
    按概率抽取元素

    :param pick_list: tuple ((probability, element),...)
    :return:
    """
    x = random.uniform(0, 1)
    cumulative_probability = 0.0

    for probability, element in pick_list:
        cumulative_probability += probability
        if x < cumulative_probability:
            return element
