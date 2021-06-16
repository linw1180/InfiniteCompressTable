# -*- coding: utf-8 -*-
import copy

import mod.client.extraClientApi as clientApi

from ...modCommon import ModName
from ...modCommon.config.ui_config import UI_DEFS

_ui_manager = None


def get_ui_manager():
    global _ui_manager
    if not _ui_manager:
        _ui_manager = UIManager()
    return _ui_manager


class UIManager(object):
    """
    UI管理类
    负责UI类的创建、注册、获取与删除操作
    尝试解决UI冲突的问题

    注意：该类需要保持单例管理
    """

    def __init__(self):
        self.registered_ui_dict = {}
        self.screen_ui_dict = {}  # {ui_name:ui_node}
        self.entity_ui_dict = {}  # {ui_name:{entity_id:ui_node}}
        self.current_ui_list = []  # [(ui_data, args)]
        self.full_screen_lock = False

    def init_all_ui(self, args):
        self.clear()
        for ui_data in UI_DEFS.values():
            self.register_ui(ui_data)

    def register_ui(self, ui_data):
        ui_name = ui_data['ui_name']
        if not self.registered_ui_dict.get(ui_name):
            clientApi.RegisterUI(ModName, ui_name, ui_data["ui_class_path"], ui_data["ui_screen_def"])
            self.registered_ui_dict[ui_name] = True

    def create_ui_node(self, ui_data):
        ui_name = ui_data['ui_name']
        param_dict = ui_data.get("paramDict", {"isHud": 1})
        ui_node = clientApi.CreateUI(ModName, ui_name, param_dict)
        if not ui_node:
            return None
        if param_dict.get('bindEntityId'):
            self.entity_ui_dict.setdefault(ui_name, {})
            self.entity_ui_dict[ui_name][param_dict.get('bindEntityId')] = ui_node
        else:
            self.screen_ui_dict[ui_name] = ui_node
        return ui_node

    def get_or_create_ui_node(self, ui_data):
        ui_name = ui_data['ui_name']
        param_dict = ui_data.get("paramDict", {"isHud": 1})
        if param_dict.get('bindEntityId'):
            ui_node = self.entity_ui_dict.get(ui_name, {}).get(param_dict.get('bindEntityId'))
        else:
            ui_node = self.screen_ui_dict.get(ui_name)

        if ui_node:
            return ui_node
        return clientApi.GetUI(ModName, ui_name) or self.create_ui_node(ui_data)

    def get_ui_node(self, ui_data):
        ui_name = ui_data['ui_name']
        param_dict = ui_data.get("paramDict", {"isHud": 1})
        if param_dict.get('bindEntityId'):
            ui_node = self.entity_ui_dict.get(ui_name, {}).get(param_dict.get('bindEntityId'))
        else:
            ui_node = self.screen_ui_dict.get(ui_name)
        return ui_node

    def show_current_ui(self, ui_data, lock=False, **kwargs):
        """
        将UI对象加入self.current_ui_list
        如果该对象需要锁定
            隐藏之前的UI，显示当前UI，且将锁定状态置真
        如果不需要锁定，且当前未锁定
            显示当前UI

        :param ui_data:
        :param lock: 是否需要锁定UI显示，用于全屏显示UI等情况
        :return:
        """
        # print "========== show_current_ui ui_data ==========", ui_data
        # print "========== show_current_ui current ==========", self.current_ui_list
        # print "========== full_screen_lock:%s lock:%s ==========" % (self.full_screen_lock, lock)
        # 由于ui_data的paramDict属性会变动，需要进行deepcopy存储
        self.current_ui_list.append((copy.deepcopy(ui_data), kwargs))

        if self.full_screen_lock and not lock:
            return None

        if lock:
            for data, _ in self.current_ui_list:
                if data != ui_data:
                    ui_node = self.get_or_create_ui_node(data)
                    if ui_node:
                        ui_node.hide_ui()
                    else:
                        # 去除掉不存在的ui_node
                        self.current_ui_list.remove((data, _))

            self.full_screen_lock = True

        ui_node = self.get_or_create_ui_node(ui_data)
        if not ui_node:
            self.current_ui_list.remove((ui_data, kwargs))
            return None
        ui_node.show_ui(**kwargs) if kwargs else ui_node.show_ui()

        return ui_node

    def hide_current_ui(self, ui_data, is_del=False, unlock=False):
        """
        若锁定，且不解锁
            去除self.current_ui_list内对象
        若锁定，且解锁
            执行当前UI的hide_ui方法，去除self.current_ui_list内对象，显示其他UI
        若未锁定
            去除self.current_ui_list内对象，执行当前UI的hide_ui方法

        :param is_del: 是否删除该UI
        :param ui_data:
        :param unlock: 是否解除UI显示锁定
        :return:
        """
        ui_name = ui_data['ui_name']
        bind_id = ui_data.get("paramDict", {"isHud": 1}).get('bindEntityId')

        if bind_id:
            for index, value in enumerate(self.current_ui_list):
                if ui_name == value[0].get('ui_name') and bind_id == value[0].get("paramDict").get('bindEntityId'):
                    self.current_ui_list.pop(index)
                    break

        else:
            for index, value in enumerate(self.current_ui_list):
                if ui_name == value[0].get('ui_name'):
                    self.current_ui_list.pop(index)
                    break

        # print "========== hide_current_ui ui_data ==========", ui_data
        # print "========== hide_current_ui current ==========", self.current_ui_list
        # print "========== full_screen_lock:%s unlock:%s ==========" % (self.full_screen_lock, unlock)

        if self.full_screen_lock and not unlock:
            if is_del:
                if bind_id:
                    self.remove_entity_ui_node(ui_name, bind_id)
                else:
                    self.remove_ui_node(ui_name)
            return

        self.get_or_create_ui_node(ui_data).hide_ui()

        if is_del:
            if bind_id:
                self.remove_entity_ui_node(ui_name, bind_id)
            else:
                self.remove_ui_node(ui_name)

        if self.full_screen_lock and unlock:
            for data, args in self.current_ui_list:
                ui_node = self.get_or_create_ui_node(data)
                if ui_node:
                    ui_node.show_ui(**args) if args else ui_node.show_ui()
                else:
                    # 去除掉不存在的ui_node
                    self.current_ui_list.remove((data, args))

            self.full_screen_lock = False

    def remove_ui_node(self, ui_name):
        ui_node = clientApi.GetUI(ModName, ui_name)
        if ui_node:
            if ui_name in self.screen_ui_dict:
                del self.screen_ui_dict[ui_name]
            # 从上面获取的UI结点删除界面，会调用node的Destroy()方法。
            ui_node.SetRemove()
            return True
        return False

    def remove_entity_ui_node(self, ui_name, entity_id):
        ui_node = self.entity_ui_dict[ui_name].pop(entity_id)
        if ui_node:
            ui_node.SetRemove()
            return True
        return False

    @staticmethod
    def push_ui(ui_date, **kwargs):
        ui_name = ui_date['ui_name']
        ui_node = clientApi.PushScreen(ModName, ui_name)
        if ui_node:
            ui_node.show_ui(**kwargs)
            return ui_node
        return

    @staticmethod
    def pop_ui():
        clientApi.PopScreen()

    @staticmethod
    def get_ui_by_push(ui_date):
        ui_name = ui_date['ui_name']
        return clientApi.GetUI(ModName, ui_name)

    def clear(self):
        self.registered_ui_dict.clear()
        self.screen_ui_dict.clear()
        self.entity_ui_dict.clear()
        self.current_ui_list = []
        self.full_screen_lock = False
