# -*- coding: utf-8 -*-

import warnings

import mod.server.extraServerApi as serverApi

from . import extra_server_api
from ...modCommon import ModName, ModServerSystemName


def get_platform():
    """
    获取脚本运行的平台

    1.18 新增 获取脚本运行的平台

    :return: int 0：Window；1：IOS；2：Android；-1：其他
    """
    return extra_server_api.get_system(ModName, ModServerSystemName).GetPlatform()


def broadcast_event(event_name, event_data):
    # type: (str, dict) -> None
    """
    本地广播事件，服务端system广播的事件仅服务端system能监听。

    :param event_name: str 事件名
    :param event_data: dict 事件参数
    :return:
    """
    extra_server_api.get_system(ModName, ModServerSystemName).BroadcastEvent(event_name, event_data)


def broadcast_to_all_client(event_name, event_data):
    # type: (str, dict) -> None
    """
    服务器广播事件到所有客户端

    :param event_name: str 事件名
    :param event_data: dict 事件参数
    :return:
    """
    extra_server_api.get_system(ModName, ModServerSystemName).BroadcastToAllClient(event_name, event_data)


def create_event_data():
    # type: () -> dict
    """
    创建自定义事件的数据，eventData用于发送事件。创建的eventData可以理解为一个dict，可以嵌套赋值dict,list和基本数据类型，但不支持tuple

    :return: dict 事件数据
    """
    warnings.warn("1.20 目前CreateEventData暂时没有特殊功能，可以使用{}代替", DeprecationWarning)
    return extra_server_api.get_system(ModName, ModServerSystemName).CreateEventData()


def define_event(event_name):
    # type: (str) -> None
    """
    定义自定义事件

    :param event_name: str 事件名
    :return:
    """
    extra_server_api.get_system(ModName, ModServerSystemName).DefineEvent(event_name)


def listen_for_event(namespace, system_name, event_name, instance, func, priority=0):
    """
    注册监听某个系统抛出的事件。若监听引擎事件时，namespace和systemName分别为GetEngineNamespace()和GetEngineSystemName()

    :param namespace: str 所监听事件的来源系统的namespace
    :param system_name: str 所监听事件的来源系统的systemName
    :param event_name: str 事件名
    :param instance: instance 回调函数所属的类的实例
    :param func: function 回调函数
    :param priority: int 这个回调函数的优先级。默认值为0，这个数值越大表示被执行的优先级越高，最高为10
    :return:
    """
    extra_server_api.get_system(ModName, ModServerSystemName
                                ).ListenForEvent(namespace, system_name, event_name, instance, func, priority)


def notify_to_client(target_id, event_name, event_data):
    # type: (str, str, dict) -> None
    """
    服务端端发送事件到客户器

    :param target_id: str 客户端对应的Id，一般就是玩家Id
    :param event_name: str 事件名
    :param event_data: dict 事件参数，一般用CreateEventData的返回值
    :return:
    """
    extra_server_api.get_system(ModName, ModServerSystemName).NotifyToClient(target_id, event_name, event_data)


def un_define_event(event_name):
    # type: (str) -> None
    """
    取消自定义事件

    :param event_name: str 事件名
    :return:
    """
    extra_server_api.get_system(ModName, ModServerSystemName).UnDefineEvent(event_name)


def un_listen_all_events():
    """
    反注册监听某个系统抛出的所有事件，即不再监听。

    :return:
    """
    extra_server_api.get_system(ModName, ModServerSystemName).UnListenAllEvents()


def un_listen_for_event(namespace, system_name, event_name, instance, func, priority=0):
    """
    反注册监听某个系统抛出的事件，即不再监听。若是引擎事件，则namespace和systemName分别为GetEngineNamespace()和GetEngineSystemName()。与ListenForEvent对应。

    :param namespace: str 所监听事件的来源系统的namespace
    :param system_name: str 所监听事件的来源系统的systemName
    :param event_name: str 事件名
    :param instance: instance 回调函数所属的类的实例
    :param func: function 回调函数
    :param priority: int 这个回调函数的优先级。默认值为0，这个数值越大表示被执行的优先级越高
    :return:
    """
    extra_server_api.get_system(ModName, ModServerSystemName
                                ).UnListenForEvent(namespace, system_name, event_name, instance, func, priority)


def create_engine_entity_by_type_str(engine_type_str, pos, rot, dimension=0, is_npc=False):
    """
    利用字符串创建引擎实体，主要用于微软自定义物体，具体参见创建实体部分内容
    
    :param engine_type_str: str 例如 'minecraft:husk'
    :param pos: tuple(float,float,float) 生成坐标
    :param rot: tuple(float,float) 生物面向
    :param dimension: int 生成的维度，默认值为0（0为主世界，1为地狱，2为末地）
    :param is_npc: bool 是否为npc，默认值为False。npc不会移动、转向、存盘。
    :return: str或None 实体Id或者None
    """
    return extra_server_api.get_system(ModName, ModServerSystemName
                                       ).CreateEngineEntityByTypeStr(engine_type_str, pos, rot, dimension, is_npc)


def create_engine_item_entity(item_dict, dimension_id=0, pos=(0, 0, 0)):
    """
    用于创建物品实体，功能与item组件的SpawnItemToLevel接口作用类似，该接口返回物品的entityId，具体参见item组件

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/02-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-ModAPI/0-%E5%90%8D%E8%AF%8D%E8%A7%A3%E9%87%8A.html#%E7%89%A9%E5%93%81%E4%BF%A1%E6%81%AF%E5%AD%97%E5%85%B8

    :param item_dict: dict [物品信息字典]
        itemName: str 必须设置，物品的identifier，即"命名空间:物品名"
        count: int 必须设置，物品数量。设置为0时为空物品
        auxValue: int 必须设置，物品附加值
        showInHand: bool 可选，是否显示在手上，默认为True
        enchantData: list(tuple(EnchantType, int)) 可选，附魔数据，tuple中EnchantType为附魔类型，int为附魔等级
        customTips: str 可选，物品的自定义tips
        extraId: str 可选，物品自定义标识符。可以用于保存数据， 区分物品
        userData: dict 可选，物品userData，用于灾厄旗帜、旗帜等物品，请勿随意设置该值
        durability: int 可选，物品耐久度，不存在耐久概念的物品默认值为零
    :param dimension_id: int 设置dimension，默认为主世界
    :param pos: tuple(float,float,float) 生成坐标
    :return: str或None 实体Id或者None
    """
    return extra_server_api.get_system(ModName, ModServerSystemName
                                       ).CreateEngineItemEntity(item_dict, dimension_id, pos)


def destroy_entity(entity_id):
    # type: (str) -> bool
    """
    实体销毁接口

    :param entity_id: str 销毁的实体ID
    :return: bool 是否销毁成功
    """
    return extra_server_api.get_system(ModName, ModServerSystemName).DestroyEntity(entity_id)


def create_component(entity_id, namespace, name):
    """
    给实体创建组件，与GetComponent类似，如果已经创建会自动直接Get

    :param entity_id: str 该组件属主的实体id
    :param namespace: str 组件的命名空间，registerComponent的namespace
    :param name: str 组件的名字
    :return: instance 组件实例
    """
    return serverApi.CreateComponent(entity_id, namespace, name)


def get_component(entity_id, namespace, name):
    """
    获取实体的组件。一般用来判断某个组件是否创建过，其他情况请使用CreateComponent

    :param entity_id: str 该组件属主的实体id
    :param namespace: str 组件的命名空间，registerComponent的namespace
    :param name: str 组件的名字
    :return: instance 组件实例
    """
    return serverApi.GetComponent(entity_id, namespace, name)
