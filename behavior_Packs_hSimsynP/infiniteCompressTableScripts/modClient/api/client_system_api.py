# -*- coding: utf-8 -*-

import warnings

import mod.client.extraClientApi as clientApi

from . import extra_client_api
from ...modCommon import ModName, ModClientSystemName


def get_platform():
    """
    获取脚本运行的平台

    1.18 新增 获取脚本运行的平台

    :return: int 0：Window；1：IOS；2：Android；-1：其他
    """
    return extra_client_api.get_system(ModName, ModClientSystemName).GetPlatform()


def broadcast_event(event_name, event_data):
    # type: (str, dict) -> None
    """
    本地广播事件，客户端system广播的事件仅客户端system能监听。

    :param event_name: str 事件名
    :param event_data: dict 事件参数
    :return:
    """
    warnings.warn("1.20 BroadcastEvent目前暂时无法使用，需要通过服务端BroadcastToAllClient广播", DeprecationWarning)
    extra_client_api.get_system(ModName, ModClientSystemName).BroadcastEvent(event_name, event_data)


def create_event_data():
    # type: () -> dict
    """
    创建自定义事件的数据，eventData用于发送事件。创建的eventData可以理解为一个dict，可以嵌套赋值dict,list和基本数据类型，但不支持tuple

    :return: dict 事件数据
    """
    warnings.warn("1.20 目前CreateEventData暂时没有特殊功能，可以使用{}代替", DeprecationWarning)
    return extra_client_api.get_system(ModName, ModClientSystemName).CreateEventData()


def define_event(event_name):
    # type: (str) -> None
    """
    定义自定义事件

    :param event_name: str 事件名
    :return:
    """
    extra_client_api.get_system(ModName, ModClientSystemName).DefineEvent(event_name)


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
    extra_client_api.get_system(ModName, ModClientSystemName
                                ).ListenForEvent(namespace, system_name, event_name, instance, func, priority)


def notify_to_server(event_name, event_data):
    # type: (str, dict) -> None
    """
    客户端发送事件到服务器

    :param event_name: str 事件名
    :param event_data: dict 事件参数，一般用CreateEventData的返回值
    :return:
    """
    extra_client_api.get_system(ModName, ModClientSystemName).NotifyToServer(event_name, event_data)


def un_define_event(event_name):
    # type: (str) -> None
    """
    取消自定义事件

    :param event_name: str 事件名
    :return:
    """
    extra_client_api.get_system(ModName, ModClientSystemName).UnDefineEvent(event_name)


def un_listen_all_events():
    """
    反注册监听某个系统抛出的所有事件，即不再监听。

    :return:
    """
    extra_client_api.get_system(ModName, ModClientSystemName).UnListenAllEvents()


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
    extra_client_api.get_system(ModName, ModClientSystemName
                                ).UnListenForEvent(namespace, system_name, event_name, instance, func, priority)


def destroy_entity(entity_id):
    # type: (str) -> bool
    """
    实体销毁接口

    :param entity_id: str 销毁的实体ID
    :return: bool 是否销毁成功
    """
    return extra_client_api.get_system(ModName, ModClientSystemName).DestroyEntity(entity_id)


def create_engine_effect(path, bind_entity, ani_name):
    # type: (str, str, str) -> int
    """
    用于创建模型挂接特效，具体参见创建特效部分内容。

    :param path: str 特效资源路径，需要加上后缀名（一般是json）
    :param bind_entity: str 绑定实体的Id
    :param ani_name: str 选择使用哪个模型动作的特效
    :return: int或None effectEntityId或者None
    """
    return extra_client_api.get_system(ModName, ModClientSystemName).CreateEngineEffect(path, bind_entity, ani_name)


def create_engine_particle(path, pos=(0, 0, 0)):
    # type: (str, tuple) -> int
    """
    用于创建粒子特效，具体参见创建特效部分内容

    :param path: str 特效资源路径，需要加上后缀名（一般是json）
    :param pos: tuple (float,float,float)创建位置坐标
    :return: int或None particleEntityId或者None
    """
    return extra_client_api.get_system(ModName, ModClientSystemName).CreateEngineParticle(path, pos)


def create_engine_sfx(path, pos=None, rot=None, scale=None):
    # type: (str, tuple, tuple, float) -> int
    """
    用于创建序列帧特效，具体参见创建特效部分内容

    :param path: str 特效资源路径，不用后缀名
    :param pos: tuple (float,float,float)创建位置，可选
    :param rot: tuple (float,float)角度，可选
    :param scale: float 缩放系数，可选
    :return: int或None frameEntityId或者None
    """
    return extra_client_api.get_system(ModName, ModClientSystemName).CreateEngineSfx(path, pos, rot, scale)


def create_engine_sfx_from_editor(path, pos=None, rot=None, scale=None):
    # type: (str, tuple, tuple, float) -> int
    """
    指使用资源包中effects/xxx.json，按照编辑器中编辑好的参数创建序列帧。支持环状序列帧

    :param path: str 特效资源路径，不用后缀名
    :param pos: tuple (float,float,float)创建位置，可选
    :param rot: tuple (float,float)角度，可选
    :param scale: float 缩放系数，可选
    :return: int或None frameEntityId或者None
    """
    return extra_client_api.get_system(ModName, ModClientSystemName).CreateEngineSfxFromEditor(path, pos, rot, scale)


def create_component(entity_id, namespace, name):
    """
    给实体创建组件，与GetComponent类似，如果已经创建会自动直接Get

    :param entity_id: str 该组件属主的实体id
    :param namespace: str 组件的命名空间，registerComponent的namespace
    :param name: str 组件的名字
    :return: instance 组件实例
    """
    return clientApi.CreateComponent(entity_id, namespace, name)


def get_component(entity_id, namespace, name):
    """
    获取实体的组件。一般用来判断某个组件是否创建过，其他情况请使用CreateComponent

    :param entity_id: str 该组件属主的实体id
    :param namespace: str 组件的命名空间，registerComponent的namespace
    :param name: str 组件的名字
    :return: instance 组件实例
    """
    return clientApi.GetComponent(entity_id, namespace, name)
