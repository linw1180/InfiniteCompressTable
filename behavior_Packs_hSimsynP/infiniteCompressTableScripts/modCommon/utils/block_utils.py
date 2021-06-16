# -*- coding: utf-8 -*-


def get_block_aux_from_rot(rot):
    if -135 <= rot[1] < -45:
        return 1
    elif -45 <= rot[1] < 45:
        return 2
    elif 45 <= rot[1] < 135:
        return 3
    else:
        return 0
