# -*- coding: utf-8 -*-
from ...modCommon.config.custom_container_config import FLY_ANIMATION_DURATION


class FlyImage(object):
    def __init__(self, path):
        self.path = path
        self.to_pos = []
        self.from_pos = []
        self.current_pos = []
        self.delta_x = 0
        self.delta_y = 0
        self.using = False

    def init_pos(self, from_pos, to_pos):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.current_pos = list(from_pos)
        self.using = True
        self.delta_x = (self.to_pos[0] - self.from_pos[0]) * 1.0 / FLY_ANIMATION_DURATION
        self.delta_y = (self.to_pos[1] - self.from_pos[1]) * 1.0 / FLY_ANIMATION_DURATION

    def update_current_pos(self):
        self.current_pos[0] += self.delta_x
        self.current_pos[1] += self.delta_y
        return tuple(self.current_pos)

    def is_using(self):
        return self.using

    def release(self):
        self.using = False

    def get_path(self):
        return self.path
