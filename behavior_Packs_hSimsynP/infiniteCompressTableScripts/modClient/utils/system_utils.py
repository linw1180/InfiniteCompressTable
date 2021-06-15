# -*- coding: utf-8 -*-
import logging

from ..api import client_system_api, extra_client_api
from ...modCommon import ModName, ModServerSystemName, ModClientSystemName

_client_mod_system = {}

logger = logging.getLogger('{}.Client'.format(ModName))


def get_client(name_space=ModName, system_name=ModClientSystemName):
    """
    获取客户端系统，全局一个单例。

    :return: ClientSystem 返回具体系统的实例，如果获取不到则返回 None
    """
    client = name_space + system_name
    if client not in _client_mod_system:
        _client_mod_system[client] = extra_client_api.get_system(name_space, system_name)
    return _client_mod_system[client]


def listen_engine_events(engine_event_info):
    """
    监听客户端引擎事件

    :param engine_event_info: list[event_name, instance, function] 客户端引擎事件
        event_name: str 事件名
        instance: instance 回调函数所属的类的实例
        func: function 回调函数
    :return:
    """
    for event_name, instance, function in engine_event_info:
        client_system_api.listen_for_event(extra_client_api.get_engine_namespace(),
                                           extra_client_api.get_engine_system_name(),
                                           event_name, instance, function)


def un_listen_engine_events(engine_event_info):
    """
    反注册监听客户端引擎事件

    :param engine_event_info: list[event_name, instance, function] 客户端引擎事件
        event_name: str 事件名
        instance: instance 回调函数所属的类的实例
        func: function 回调函数
    :return:
    """
    for event_name, instance, function in engine_event_info:
        client_system_api.un_listen_for_event(extra_client_api.get_engine_namespace(),
                                              extra_client_api.get_engine_system_name(),
                                              event_name, instance, function)


def listen_server_events(server_event_info):
    """
    监听服务端自定义事件

    :param server_event_info: list[event_name, instance, function] 服务端自定义事件
        event_name: str 事件名
        instance: instance 回调函数所属的类的实例
        func: function 回调函数
    :return:
    """
    for event_name, instance, function in server_event_info:
        client_system_api.listen_for_event(ModName, ModServerSystemName, event_name, instance, function)


def un_listen_server_events(server_event_info):
    """
    反注册监听服务端自定义事件

    :param server_event_info: list[event_name, instance, function] 服务端自定义事件
        event_name: str 事件名
        instance: instance 回调函数所属的类的实例
        func: function 回调函数
    :return:
    """
    for event_name, instance, function in server_event_info:
        client_system_api.un_listen_for_event(ModName, ModServerSystemName, event_name, instance, function)


def listen_client_events(client_event_info):
    """
    监听客户端自定义事件

    :param client_event_info: list[event_name, instance, function] 客户端自定义事件
        event_name: str 事件名
        instance: instance 回调函数所属的类的实例
        func: function 回调函数
    :return:
    """
    for event_name, instance, function in client_event_info:
        client_system_api.listen_for_event(ModName, ModClientSystemName, event_name, instance, function)
