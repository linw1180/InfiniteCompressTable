# -*- coding: utf-8 -*-

"""
这里是一些服务端的基础API接口，完成基础的系统和组件的初始化，同时也能从这个module中获取到一些通用的枚举类和levelId等信息。
"""
import warnings

import mod.server.extraServerApi as serverApi


# region 实体
def add_entity_tick_event_white_list(identifier):
    """
    添加实体类型到EntityTickServerEvent事件的触发白名单。

    1.20 新增 添加实体tick事件白名单

    :param identifier: str 实体的类型名，原版的实体需要加上minecraft命名空间
    :return: bool 是否成功
    """
    return serverApi.AddEntityTickEventWhiteList(identifier)


# endregion


# region 通用
def get_dir_from_rot(rot):
    """
    通过旋转角度获取朝向

    :param rot: tuple(float,float) 俯仰角度及绕竖直方向的角度，单位是角度
    :return: tuple(float,float,float) 玩家朝向的单位向量
    """
    return serverApi.GetDirFromRot(rot)


def get_engine_actor():
    """
    获取所有实体

    1.23 调整 返回结果中去掉当前已经确定要移除的实体

    :return: dict 当前地图中的所有实体信息，key：实体id，value：entityDict
        entityDict: {
            dimensionId: int 维度id
            entityType: int 实体类型id，可参考EntityType
        }
    """
    return serverApi.GetEngineActor()


def get_engine_namespace():
    """
    获取引擎事件的命名空间。监听引擎事件时，namespace传该接口返回的namespace

    :return: str 引擎的命名空间
    """
    return serverApi.GetEngineNamespace()


def get_engine_system_name():
    """
    获取引擎系统名。监听引擎事件时，systemName传该接口返回的systemName

    :return: str 引擎的systemName
    """
    return serverApi.GetEngineSystemName()


def get_entity_limit():
    """
    获取当前level最大实体数量（上限值，非现有值）

    1.19 新增 获取当前level最大实体数量

    :return: int 当前level最大实体数量
    """
    return serverApi.GetEntityLimit()


def get_level_id():
    """
    获取levelId。某些组件需要levelId创建，可以用此接口获取levelId。其中level即为当前地图的游戏。

    :return: str 当前地图的levelId
    """
    return serverApi.GetLevelId()


def get_minecraft_enum():
    """
    用于获取[Minecraft枚举值文档]中的枚举值

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/99-%E5%8F%82%E8%80%83%E8%B5%84%E6%96%99/0-Minecraft%E6%9E%9A%E4%B8%BE%E5%80%BC%E6%96%87%E6%A1%A3.html

    import common.minecraftEnum as enum

    return enum

    :return: minecraftEnum 枚举集合类
    """
    warnings.warn("冗余接口，可以直接通过import相应的枚举类实现获取枚举值", DeprecationWarning)
    return serverApi.GetMinecraftEnum()


def get_player_list():
    """
    获取level中所有玩家的id列表

    1.19 新增 获取获取level中所有玩家的id列表

    :return: list(str) 返回玩家id列表
    """
    return serverApi.GetPlayerList()


def is_in_apollo():
    """
    返回当前游戏Mod是否运行在Apollo网络服

    :return: bool True是说明当前Mod运行于Apollo网络服环境，False时说明当前Mod运行于租赁服、联机大厅或者单机环境
    """
    return serverApi.IsInApollo()


def is_in_server():
    """
    获取当前游戏是否跑在服务器环境下

    :return: bool True:在服务器环境下 False:不在服务器环境下
    """
    return serverApi.IsInServer()


def set_entity_limit(num):
    """
    设置以玩家为中心，6个chunk范围内的最大实体数量，实体数量超过该值后将不再随机生成实体，不影响summon指令和sdk相关生成实体接口

    该上限与生物json文件中配置的种群密度共同作用，比如上限是200，但种群密度是10，那么该生物随机生成不会超过10个。此外生物上限还和适合生成的区块容
    量相关，设置上限过高的话可能因其他限制条件而不能达到该高度。

    1.19 新增 设置以玩家为中心，6个chunk范围内的最大实体数量

    :param num: int 以玩家为中心，6个chunk范围内的最大实体数量
    :return: bool 返回是否设置成功
    """
    return serverApi.SetEntityLimit(num)


def start_multi_profile():
    """
    开始启动服务端与客户端双端脚本性能分析，启动后调用[StopMultiProfile(path)]即可在路径path生成函数性能火焰图。双端采集时数据误差较大，建议

    优先使用[StartProfile()]单端版本，此接口只支持PC端

    1.18 新增 开始启动服务端与客户端双端脚本性能分析

    :return: bool 执行结果
    """
    return serverApi.StartMultiProfile()


def start_profile():
    """
    开始启动服务端脚本性能分析，启动后调用[StopProfile(path)]即可在路径path生成函数性能火焰图，此接口只支持PC端。

    生成的火焰图可以用浏览器打开，推荐chrome浏览器。

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/02-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-ModAPI/1-ExtraAPI%E6%8E%A5%E5%8F%A3/1-%E6%9C%8D%E5%8A%A1%E7%AB%AFExtraAPI%E6%8E%A5%E5%8F%A3.html#startprofile

    1.18 新增 开始启动服务端脚本性能分析

    :return: bool 执行结果
    """
    return serverApi.StartProfile()


def start_record_event():
    """
    开始启动服务端与客户端之间的脚本事件收发包统计，启动后调用[StopRecordEvent()]即可获取两个函数调用之间引擎收发包的统计信息

    1.19 新增 开始启动服务端与客户端之间的脚本事件收发包统计

    :return: bool 执行结果
    """
    return serverApi.StartRecordEvent()


def start_record_packet():
    """
    开始启动服务端与客户端之间的引擎收发包统计，启动后调用[StopRecordPacket()]即可获取两个函数调用之间引擎收发包的统计信息

    1.19 新增 开始启动服务端与客户端之间的引擎收发包统计

    :return: bool 执行结果
    """
    return serverApi.StartRecordPacket()


def stop_multi_profile(file_name=None):
    """
    停止双端脚本性能分析并生成火焰图，与[StartMultiProfile()]配合使用，此接口只支持PC端\

    1.18 新增 停止双端脚本性能分析并生成火焰图

    :param file_name: str 具体路径，相对于PC开发包的路径，默认为"flamegraph.svg"，位于PC开发包目录下，自定义路径请确保文件后缀名为".svg"
    :return: bool 执行结果
    """
    return serverApi.StopMultiProfile(file_name)


def stop_profile(file_name=None):
    """
    停止服务端脚本性能分析并生成火焰图，与[StartProfile()]配合使用，此接口只支持PC端

    1.18 新增 停止服务端脚本性能分析并生成火焰图

    :param file_name: str 具体路径，相对于PC开发包的路径，默认为"flamegraph.svg"，位于PC开发包目录下，自定义路径请确保文件后缀名为".svg"
    :return: bool 执行结果
    """
    return serverApi.StopProfile(file_name)


def stop_record_event():
    """
    停止服务端与客户端之间的脚本事件收发包统计并输出结果，与[StartRecordEvent()]配合使用，输出结果为字典，key为网络包名，value字典中记录收发信息，具体见示例

    1.19 新增 停止服务端与客户端之间的脚本事件收发包统计并输出结果

    :return: dict 收发包信息，假如没有调用过StartRecordEvent，则返回为None
    """
    return serverApi.StopRecordEvent()


def stop_record_packet():
    """
    停止服务端与客户端之间的引擎收发包统计并输出结果，与[StartRecordPacket()]配合使用，输出结果为字典，key为网络包名，value字典中记录收发信息，具体见示例
    
    1.19 新增 停止服务端与客户端之间的引擎收发包统计并输出结果
    
    :return: dict 收发包信息，假如没有调用过StartRecordPacket，则返回为None
    """
    return serverApi.StopRecordPacket()


# endregion


# region 系统
def get_server_system_cls():
    """
    用于获取服务器system基类。实现新的system时，需要继承该接口返回的类
    
    :return: type(ServerSystem) 服务端系统类
    """
    return serverApi.GetServerSystemCls()


def get_system(namespace, system_name):
    """
    获取已注册的系统
    
    :param namespace: str 命名空间，建议为mod名字
    :param system_name: str 系统名称，自定义名称，可以使用英文、拼音和下划线，建议尽量个性化
    :return: ServerSystem 返回具体系统的实例
    """
    return serverApi.GetSystem(namespace, system_name)


def register_system(namespace, system_name, cls_path):
    """
    用于将系统注册到引擎中，引擎会保存系统的实例，并在退出时引擎会回收。
    
    系统可以执行我们引擎赋予的基本逻辑，例如监听事件、执行Tick函数、与客户端进行通讯等。
    
    :param namespace: str 命名空间，建议为mod名字
    :param system_name: str 系统名称，自定义名称，可以使用英文、拼音和下划线，建议尽量个性化
    :param cls_path: str 组件类路径，路径从脚本的第一层开始算起
    :return: ServerSystem 返回具体系统的实例
    """
    return serverApi.RegisterSystem(namespace, system_name, cls_path)


# endregion


# region 组件
def get_component_cls():
    """
    用于获取服务器component基类。实现新的component时，需要继承该接口返回的类
    
    :return: type(BaseComponent) 组件基类
    """
    return serverApi.GetComponentCls()


def get_engine_comp_factory():
    """
    获取引擎组件的工厂，通过工厂可以创建服务端的引擎组件
    
    1.20 新增 获取组件的工厂，服务端引擎组件通过该工厂创建
    
    :return: EngineCompFactoryServer 服务端引擎组件工厂
    """
    return serverApi.GetEngineCompFactory()


def register_component(namespace, name, cls_path):
    """
    用于将组件注册到引擎中
    
    :param namespace: str 命名空间，建议为mod名字
    :param name: str 组件名称
    :param cls_path: str 组件类路径，路径从脚本的第一层开始算起
    :return: bool 注册成功与否
    """
    return serverApi.RegisterComponent(namespace, name, cls_path)
# endregion
