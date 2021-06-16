# -*- coding: utf-8 -*-

from ..api import extra_server_api, server_system_api
from ...modCommon import ModName, ModServerSystemName, ModClientSystemName

_server_mod_system = None


def get_mod_server_system():
    """
    获取服务端系统，全局一个单例。

    :return: ClientSystem 返回具体系统的实例，如果获取不到则返回 None
    """
    global _server_mod_system
    if not _server_mod_system:
        _server_mod_system = extra_server_api.get_system(ModName, ModServerSystemName)
    return _server_mod_system


DEFINE_EVENT_LIST = [

]


def define_events():
    # type: () -> None
    """
    定义客户端自定义事件

    :return:
    """
    for event_name in DEFINE_EVENT_LIST:
        server_system_api.define_event(event_name)


def un_define_events():
    # type: () -> None
    """
    取消自定义事件

    :return:
    """
    for event_name in DEFINE_EVENT_LIST:
        server_system_api.un_define_event(event_name)


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
        server_system_api.listen_for_event(extra_server_api.get_engine_namespace(),
                                           extra_server_api.get_engine_system_name(),
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
        server_system_api.listen_for_event(ModName, ModServerSystemName, event_name, instance, function)


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
        server_system_api.listen_for_event(ModName, ModClientSystemName, event_name, instance, function)
