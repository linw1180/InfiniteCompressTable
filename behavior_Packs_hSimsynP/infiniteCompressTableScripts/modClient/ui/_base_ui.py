# -*- coding: utf-8 -*-

from mod.client.ui.screenNode import ScreenNode


class BaseUI(ScreenNode):
    def __init__(self, namespace, name, param):
        super(BaseUI, self).__init__(namespace, name, param)

    def show_ui(self):
        self.SetScreenVisible(True)

    def hide_ui(self):
        self.SetScreenVisible(False)

    def on_ui_create(self):
        pass

    def tick(self):
        pass

    def Create(self):
        self.on_ui_create()

    def Update(self):
        self.tick()
