# -*- coding: utf-8 -*-

"""
extraClientApi文件中的一些有用的API接口函数
"""
import warnings

import mod.client.extraClientApi as clientApi


# region AI
def get_nav_path(pos, **kwargs):
    # type: (tuple, dict) -> int or list
    """
    获取本地玩家到目标点的寻路路径，开发者可以通过该接口定制自定义的导航系统。

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/02-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-ModAPI/1-ExtraAPI%E6%8E%A5%E5%8F%A3/2-%E5%AE%A2%E6%88%B7%E7%AB%AFExtraAPI%E6%8E%A5%E5%8F%A3.html#getnavpath

    :param pos: tuple(float,float,float) 目标点的坐标
    :param kwargs: 根据相应参数名传入相应key:value字典
        maxTrimNode: int 对搜索路径进行平滑时的最大尝试格数。设置的太大会影响寻路性能。默认值16
        maxIteration: int A星寻路的最大迭代次数。默认值800
        isSwimmer: bool 目标点是否在水中。默认为False
    :return: int或list(tuple(float,float,float))
        返回1: 参数错误
        返回2: 玩家所在chunk未加载完毕
        返回3: 终点为实心方块，无法寻路
        返回list[tuple(float,float,float),]: 寻到路径从起点到终点的坐标点列表。注意该list可能为空，表示本地玩家离地太远，或者被堵住无法行动。
    """
    return clientApi.GetNavPath(pos, **kwargs)


def start_nav_to(pos, sfx_path, **kwargs):
    # type: (tuple, str, dict) -> int
    """
    我们提供了一个基于上述接口的导航系统实现，做法是在路径上生成序列帧以引导玩家通向目标点，并且当玩家偏离路径会重新进行导航。

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/02-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-ModAPI/1-ExtraAPI%E6%8E%A5%E5%8F%A3/2-%E5%AE%A2%E6%88%B7%E7%AB%AFExtraAPI%E6%8E%A5%E5%8F%A3.html#startnavto

    1.20 调整 优化寻路序列帧表现，新增了几个控制寻路序列帧表现的参数

    :param pos: tuple(float,float,float) 目标点的坐标
    :param sfx_path: str 构成导航路径的序列帧素材路径。样式可以参考指向上的箭头
    :param kwargs:
        callback function 玩家抵达终点时会调用的**回调函数**。该函数需要接受一个bool参数。
        sfxIntl float 相邻两个序列帧之间的间隔。默认值2
        sfxMaxNum int 同时存在的序列帧的最大个数。默认值16
        sfxScale tuple(float,float) 序列帧的宽度及高度的缩放。默认为（0.5，0.5）
        maxIteration int A星寻路的最大迭代次数。默认值800
        isSwimmer bool 目标点是否在水中。默认为False
        fps int 序列帧帧率，默认为20，不建议超过30
        playIntl int 一轮中相邻序列帧开始播放的间隔，默认为8帧，不得小于0，否则将使用默认值
        duration int 单个序列帧持续播放帧数，默认为60帧，不小于10，否则将使用默认值
        oneTurnDuration int 两轮序列帧之间的播放间隔(帧)，默认值为90帧，至少为duration的1.5倍，否则将以1.5 * duration进行计算
    :return: int
        返回0：导航正常开始
        返回-1：本地玩家离地太远，或者被堵住无法行动
        返回1：参数错误
        返回2：玩家所在chunk未加载完毕
        返回3：终点为实心方块，无法寻路
    """
    return clientApi.StartNavTo(pos, sfx_path, **kwargs)


def stop_nav():
    """
    终止当前的导航
    """
    clientApi.StopNav()


# endregion


# region IP
def get_ip():
    # type: () -> str
    """
    获取本地玩家的ip地址

    :return: str 本地玩家的ip地址
    """
    return clientApi.GetIP()


# endregion


# region UI
def check_can_bind_ui(entity_id):
    # type: (str) -> bool
    """
    检查实体是否可以绑定头顶UI，如何将UI与实体绑定详见[创建UI界面]

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/60-UI/4-UI%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.html#%E5%88%9B%E5%BB%BAui%E7%95%8C%E9%9D%A2

    不能绑定头顶UI通常是由于该实体已经死亡或该实体刚创建出来。刚创建的实体若无法绑定头顶UI，等待1-3帧后再次尝试绑定即可

    :param entity_id: str 实体id
    :return: bool 是否可以绑定头顶UI True:可以绑定 False:不能绑定
    """
    return clientApi.CheckCanBindUI(entity_id)


def create_ui(namespace, ui_key, create_params):
    # type: (str, str, dict) -> object
    """
    创建UI，详见[创建ui界面]

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/60-UI/4-UI%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.html#%E5%88%9B%E5%BB%BAui%E7%95%8C%E9%9D%A2

    :param namespace: str 命名空间，建议为mod名字
    :param ui_key: str UI唯一标识
    :param create_params: dict 创建UI的参数，会传到UI类的_init_函数中
        isHud: int 是否为Hud界面，1：是，0：否
        mini_map_root_path: str 小地图控件根路径
    :return: ScreenNode UI节点
    """
    return clientApi.CreateUI(namespace, ui_key, create_params)


def get_touch_pos():
    # type: () -> tuple
    """
    获取点击的屏幕坐标

    :return: tuple(float,float) 屏幕坐标
    """
    return clientApi.GetTouchPos()


def get_ui(namespace, ui_key):
    # type: (str, str) -> object
    """
    获取UI节点

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/60-UI/4-UI%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.html#%E8%8E%B7%E5%8F%96ui%E7%95%8C%E9%9D%A2

    :param namespace: str 命名空间，建议为mod名字
    :param ui_key: str UI唯一标识
    :return: ScreenNode UI节点
    """
    return clientApi.GetUI(namespace, ui_key)


def hide_air_supply_gui(is_hide=True):
    # type: (bool) -> bool
    """
    隐藏玩家氧气值界面

    1.19 新增 隐藏hud界面的氧气条显示

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return: bool 设置是否成功
    """
    return clientApi.HideAirSupplyGUI(is_hide)


def hide_armor_gui(is_hide=True):
    # type: (bool) -> bool
    """
    隐藏hud界面的护甲值显示

    1.20 新增 隐藏hud界面的护甲值显示

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return: bool 设置是否成功
    """
    return clientApi.HideArmorGui(is_hide)


def hide_change_person_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏切换人称的按钮。隐藏后点击相应位置不会响应

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideChangePersonGui(is_hide)


def hide_exp_gui(is_hide=True):
    # type: (bool) -> None
    """
    非创造者模式下隐藏经验条显示

    1.19 新增 新增隐藏经验条接口

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideExpGui(is_hide)


def hide_health_gui(is_hide=True):
    # type: (bool) -> bool
    """
    隐藏hud界面的血量显示

    1.18 新增 隐藏hud界面的血量显示

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return: bool 设置是否成功
    """
    return clientApi.HideHealthGui(is_hide)


def hide_horse_health_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏hud界面的坐骑的血量显示

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return: bool 设置是否成功
    """
    clientApi.HideHorseHealthGui(is_hide)


def hide_hud_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏HUD游戏界面的游戏原生UI。与原版F1按钮效果一致，只隐藏显示，但点击跳跃键等位置依然会响应

    :param is_hide: bool True为隐藏原生HUD，False为恢复显示
    :return:
    """
    clientApi.HideHudGUI(is_hide)


def hide_hunger_gui(is_hide=True):
    # type: (bool) -> bool
    """
    隐藏hud界面的饥饿值显示

    1.18 新增 隐藏hud界面的饥饿值显示

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return: bool 设置是否成功
    """
    return clientApi.HideHungerGui(is_hide)


def hide_interact_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏交互按钮。隐藏后点击相应位置不会响应

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideInteractGui(is_hide)


def hide_jump_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏游戏中右下角的跳跃按钮。隐藏后点击相应位置不会响应

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideJumpGui(is_hide)


def hide_move_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏游戏中左下角的移动按钮。隐藏后点击相应位置不会响应

    1.19 新增 新增隐藏移动按钮

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideMoveGui(is_hide)


def hide_netease_store_gui(is_hide):
    # type: (bool) -> None
    """
    隐藏游戏中的网易商店按钮。隐藏后点击相应位置不会响应

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideNeteaseStoreGui(is_hide)


def hide_name_tag(is_hide):
    # type: (bool) -> None
    """
    隐藏场景内所有名字显示，包括玩家名字，生物的自定义名称，物品展示框与命令方块的悬浮文本等

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideNameTag(is_hide)


def hide_slot_bar_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏游戏中底部中间的物品栏界面

    1.19 调整 增加HideSlotBarGui使用说明。隐藏后点击相应位置不会响应
    
    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return: 
    """
    clientApi.HideSlotBarGui(is_hide)


def hide_sneak_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏游戏中左下角方向键的中心处潜行按钮。隐藏后点击相应位置不会响应

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideSneakGui(is_hide)


def hide_swim_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏游戏中的浮潜按钮。隐藏后点击相应位置不会响应

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideSwimGui(is_hide)


def hide_walk_gui(is_hide=True):
    # type: (bool) -> None
    """
    隐藏游戏中右上角的移动类型按钮。隐藏后点击相应位置不会响应

    :param is_hide: bool 是否隐藏，True为隐藏，False为显示
    :return:
    """
    clientApi.HideWalkGui(is_hide)


def open_netease_store_gui(category_name, item_name):
    # type: (str, str) -> None
    """
    打开游戏中的网易商店购买商品界面

    :param category_name: str 商品分类名称
    :param item_name: str 商品名称
    :return:
    """
    clientApi.OpenNeteaseStoreGui(category_name, item_name)


def pop_screen():
    # type: () -> bool
    """
    使用堆栈管理的方式关闭UI

    该接口关闭由PushScreen创建的界面

    1.20 新增 使用堆栈管理的方式关闭UI

    :return: bool 是否关闭成功
    """
    return clientApi.PopScreen()


def push_screen(namespace, ui_name):
    # type: (str, str) -> object
    """
    使用堆栈管理的方式创建UI

    使用PopScreen使用可以关闭该接口创建的界面
    由于UI不会在PushScreen被调用后立即创建完成，请不要在Init函数中对控件进行操作，创建完成后会调用screenNode的Create函数

    1.20 新增 使用堆栈管理的方式创建UI

    :param namespace: str 命名空间，建议为mod名字
    :param ui_name: str UI唯一标识
    :return: ScreenNode UI节点，创建失败时返回None
    """
    return clientApi.PushScreen(namespace, ui_name)


def register_ui(name_space, ui_key, cls_path, ui_name_space):
    # type: (str, str, str, str) -> bool
    """
    注册UI，创建UI前，需要先注册UI。同一UI只需要注册一次即可。

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/60-UI/4-UI%E8%AF%B4%E6%98%8E%E6%96%87%E6%A1%A3.html#%E6%B3%A8%E5%86%8Cui%E7%95%8C%E9%9D%A2

    :param name_space: str 命名空间，建议为mod名字
    :param ui_key: str UI唯一标识
    :param cls_path: str UI类路径
    :param ui_name_space: str UI.json的命名空间
    :return: bool 是否注册成功
    """
    return clientApi.RegisterUI(name_space, ui_key, cls_path, ui_name_space)


def set_cross_hair(visible=True):
    # type: (bool) -> None
    """
    设置屏幕中心的十字是否显示

    :param visible: bool 是否隐藏，True为显示，False为隐藏
    :return:
    """
    clientApi.SetCrossHair(visible)


def set_hud_chat_stack_position(pos):
    # type: (tuple) -> None
    """
    设置HUD界面左上小聊天窗口位置

    :param pos: tuple 该界面的目标坐标，第一项为横轴，第二项为纵轴，(0,0)点在Hud界面左上角，玩家形象下方
    :return:
    """
    clientApi.SetHudChatStackPosition(pos)


def set_hud_chat_stack_visible(visible=False):
    # type: (bool) -> None
    """
    设置屏幕中心的十字是否显示

    :param visible: bool 是否隐藏，True为显示，False为隐藏
    :return:
    """
    clientApi.SetHudChatStackVisible(visible)


def set_response(response=False):
    # type: (bool) -> None
    """
    设置原生UI是否响应

    :param response: bool 点击UI时是否屏蔽下层敲击方块/攻击实体
    :return:
    """
    clientApi.SetResponse(response)


# endregion


# region 通用
def get_dir_from_rot(rot):
    # type: (tuple) -> tuple
    """
    通过旋转角度获取朝向

    :param rot: tuple(float,float) 俯仰角度及绕竖直方向的角度，单位是角度
    :return: tuple(float,float,float) 玩家朝向的单位向量
    """
    return clientApi.GetDirFromRot(rot)


def get_engine_namespace():
    # type: () -> str
    """
    获取引擎事件的命名空间。监听引擎事件时，namespace传该接口返回的namespace

    :return: str 引擎的命名空间
    """
    return clientApi.GetEngineNamespace()


def get_engine_system_name():
    # type: () -> str
    """
    获取引擎系统名。监听引擎事件时，systemName传该接口返回的systemName

    :return: str 引擎的systemName
    """
    return clientApi.GetEngineSystemName()


def get_level_id():
    # type: () -> str
    """
    获取levelId。某些组件需要levelId创建，可以用此接口获取levelId。其中level即为当前地图的游戏。

    :return: str 当前地图的levelId
    """
    return clientApi.GetLevelId()


def get_local_player_id():
    # type: () -> str
    """
    获取本地玩家的id

    :return: str 客户端玩家Id
    """
    return clientApi.GetLocalPlayerId()


def get_minecraft_enum():
    # type: () -> object
    """
    用于获取[Minecraft枚举值文档]中的枚举值

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/99-%E5%8F%82%E8%80%83%E8%B5%84%E6%96%99/0-Minecraft%E6%9E%9A%E4%B8%BE%E5%80%BC%E6%96%87%E6%A1%A3.html

    import common.minecraftEnum as enum

    return enum

    :return: minecraftEnum 枚举集合类
    """
    warnings.warn("冗余接口，可以直接通过import相应的枚举类实现获取枚举值", DeprecationWarning)
    return clientApi.GetMinecraftEnum()


def start_multi_profile():
    # type: () -> bool
    """
    开始启动服务端与客户端双端脚本性能分析，启动后调用[StopMultiProfile(path)]即可在路径path生成函数性能火焰图。

    双端采集时数据误差较大，建议优先使用[StartProfile()]单端版本，此接口只支持PC端

    1.18 新增 开始启动服务端与客户端双端脚本性能分析

    :return: bool 执行结果
    """
    return clientApi.StartMultiProfile()


def start_profile():
    # type: () -> bool
    """
    开始启动客户端脚本性能分析，启动后调用[StopProfile(path)]即可在路径path生成函数性能火焰图，此接口只支持PC端。

    生成的火焰图可以用浏览器打开，推荐chrome浏览器。

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/02-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-ModAPI/1-ExtraAPI%E6%8E%A5%E5%8F%A3/2-%E5%AE%A2%E6%88%B7%E7%AB%AFExtraAPI%E6%8E%A5%E5%8F%A3.html#startprofile

    1.18 新增 开始启动客户端脚本性能分析

    :return: bool 执行结果
    """
    return clientApi.StartProfile()


def stop_multi_profile(file_name=None):
    # type: (str) -> bool
    """
    停止双端脚本性能分析并生成火焰图，与[StartMultiProfile()]配合使用，此接口只支持PC端

    1.18 新增 停止双端脚本性能分析并生成火焰图

    :param file_name: str 具体路径，相对于PC开发包的路径，默认为"flamegraph.svg"，位于PC开发包目录下，自定义路径请确保文件后缀名为".svg"
    :return: bool 执行结果
    """
    return clientApi.StopMultiProfile(file_name)


def stop_profile(file_name=None):
    # type: (str) -> bool
    """
    停止客户端端脚本性能分析并生成火焰图，与[StartProfile()]配合使用，此接口只支持PC端

    1.18 新增 停止客户端端脚本性能分析并生成火焰图

    :param file_name: str 具体路径，相对于PC开发包的路径，默认为"flamegraph.svg"，位于PC开发包目录下，自定义路径请确保文件后缀名为".svg"
    :return: bool 执行结果
    """
    return clientApi.StopProfile(file_name)


def get_mini_map_screen_node_cls():
    # type: () -> object
    """
    获取小地图ScreenNode基类

    1.20 新增 获取小地图ScreenNode基类

    :return: type(MiniMapBaseScreen) 小地图ScreenNode基类
    """
    return clientApi.GetMiniMapScreenNodeCls()


def get_mod_config_json():
    # type: () -> dict
    """
    以字典形式返回指定路径的json格式配置文件的内容，文件必须放置在资源包的/modconfigs目录下

    FIXME 1.23 目前接口文档错误，暂时缺少相关参数

    :return: dict 配置内容的字典，当读取文件失败时返回空字典
    """
    warnings.warn("目前接口文档错误，暂时缺少相关参数", FutureWarning)
    return clientApi.GetModConfigJson()


# endregion


# region 材质
def reload_all_materials():
    # type: () -> bool
    """
    重新加载所有材质文件

    :return: bool 是否成功
    """
    return clientApi.ReloadAllMaterials()


def reload_all_shaders():
    # type: () -> bool
    """
    重新加载所有Shader文件

    若修改到材质，建议使用ReloadAllMaterials方法。

    :return: bool 是否成功
    """
    return clientApi.ReloadAllShaders()


def reload_one_shader(shader_name):
    # type: (str) -> bool
    """
    重新加载某个Shader文件

    若同时修改了多个Shader，建议使用ReloadAllShaders方法。

    :param shader_name: str shader名称
    :return: bool 是否成功
    """
    return clientApi.ReloadOneShader(shader_name)


# endregion


# region 系统
def get_client_system_cls():
    # type: () -> object
    """
    用于获取客户端system基类。实现新的system时，需要继承该接口返回的类

    :return: type(ClientSystem) 客户端系统类
    """
    return clientApi.GetClientSystemCls()


def get_system(name_space, system_name):
    """
    用于获取其他系统实例

    :param name_space: str 系统注册的命名空间，一般为mod名字
    :param system_name: str 要获取的系统名称
    :return: ClientSystem 返回具体系统的实例，如果获取不到则返回 None
    """
    return clientApi.GetSystem(name_space, system_name)


def register_system(name_space, system_name, cls_path):
    # type: (str, str, str) -> object
    """
    用于将系统注册到引擎中，引擎会保存系统的实例，并在退出时引擎会回收。

    系统可以执行我们引擎赋予的基本逻辑，例如监听事件、执行Tick函数、与服务端进行通讯等。

    :param name_space: str 命名空间，建议为mod名字
    :param system_name: str 系统名称，自定义名称，可以使用英文、拼音和下划线，建议尽量个性化
    :param cls_path: str 组件类路径，路径从脚本的第一层开始算起
    :return: ClientSystem 返回具体系统的实例
    """
    return clientApi.RegisterSystem(name_space, system_name, cls_path)


# endregion


# region 组件
def get_component_cls():
    # type: () -> object
    """
    用于获取客户端component基类。实现新的component时，需要继承该接口返回的类

    :return: type(BaseComponent) 组件基类
    """
    return clientApi.GetComponentCls()


def get_engine_comp_factory():
    # type: () -> object
    """
    获取引擎组件的工厂，通过工厂可以创建客户端的引擎组件

    1.20 新增 获取组件的工厂，客户端引擎组件通过该工厂创建

    :return: EngineCompFactoryClient 客户端引擎组件工厂
    """
    return clientApi.GetEngineCompFactory()


def register_component(name_space, name, cls_path):
    # type: (str, str, str) -> object
    """
    用于将组件注册到引擎中

    :param name_space: str 命名空间，建议为mod名字
    :param name: str 组件名称
    :param cls_path: str 组件类路径，路径从脚本的第一层开始算起
    :return: bool 注册成功与否
    """
    return clientApi.RegisterComponent(name_space, name, cls_path)
# endregion
