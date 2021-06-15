# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()
local_player = clientApi.GetLocalPlayerId()


def get_input_vector():
    """
    获取方向键（移动轮盘）的输入
    
    :return: tuple(float,float) 返回一个单位向量，向量第一项为向左的大小，第二项为向前的大小
    """
    motion_comp = clientApi.GetEngineCompFactory().CreateActorMotion(local_player)
    return motion_comp.GetInputVector()


def lock_input_vector(input_vector):
    """
    锁定本地玩家方向键（移动轮盘）的输入，可使本地玩家持续向指定方向前行，且不会再受玩家输入影响

    传入的向量会被转化为单位向量，因此传入(10, 0)与传入(0.1, 0)效果相同

    :param input_vector: tuple(float,float) 输入向量，第一项控制向左的大小，第二项控制向前的大小。传入(0, 0)时玩家将会被强制固定在原地，不允许移动。
    :return: bool 是否锁定成功，True:成功  False:失败
    """
    motion_comp = clientApi.GetEngineCompFactory().CreateActorMotion(local_player)
    return motion_comp.LockInputVector(input_vector)


def unlock_input_vector():
    """
    解锁本地玩家方向键（移动轮盘）的输入

    :return: bool 是否解锁成功，True:成功  False:失败
    """
    motion_comp = clientApi.GetEngineCompFactory().CreateActorMotion(local_player)
    return motion_comp.UnlockInputVector()


def set_motion(motion):
    """
    设置瞬时的移动方向向量，主要用于本地玩家

    # rot 和 世界坐标系关系
    #			^ x -90°
    # 			|
    # 180°/-180  ----------> z 0°
    # 			| 90°

    可以通过当前玩家的rot组件判断目前玩家面向的方向，可在开发模式下打开F3观察数值变化。

    :param motion: tuple(float,float,float) 世界坐标系下的向量，该方向为世界坐标系下的向量，以x,z,y三个轴的正方向为正值。
    :return: bool 设置是否成功
    """
    motion_comp = clientApi.GetEngineCompFactory().CreateActorMotion(local_player)
    return motion_comp.SetMotion(motion)


def get_motion(entity_id):
    """
    获取生物的瞬时移动方向向量

    :param entity_id: tuple(int,int,int) 瞬时移动方向向量，异常时返回None
    :return:
    """
    motion_comp = clientApi.GetEngineCompFactory().CreateActorMotion(entity_id)
    return motion_comp.GetMotion()


def begin_sprinting():
    """
    使本地玩家进入并保持向前冲刺状态

    :return:
    """
    motion_comp = clientApi.GetEngineCompFactory().CreateActorMotion(local_player)
    motion_comp.BeginSprinting()


def end_sprinting():
    """
    使本地玩家结束向前冲刺状态

    :return:
    """
    motion_comp = clientApi.GetEngineCompFactory().CreateActorMotion(local_player)
    motion_comp.EndSprinting()


def set_can_move(move):
    """
    设置是否响应移动

    与SetMoveLock的区别：调用SetCanMove会清除当前Input Vector，例如玩家一直按着前进键，调用SetCanMove(False)会立即停下来，调用SetMoveLock(True)则不会。

    :param move: bool True为可移动
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanMove(move)


def set_can_jump(jump):
    """
    设置是否响应跳跃（以及在水中浮起）

    :param jump: True为可跳跃
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanJump(jump)


def set_can_attack(attack):
    """
    设置是否响应攻击

    :param attack: bool True为可攻击
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanAttack(attack)


def set_can_walk_mode(walk_mode):
    """
    设置是否响应切换行走模式

    :param walk_mode: bool True为可切换
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    # 不响应切换行走模式
    return operation_comp.SetCanWalkMode(walk_mode)


def set_can_perspective(perspective):
    """
    设置是否响应切换视角

    :param perspective: bool True为可切换
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanPerspective(perspective)


def set_can_pause(pause):
    """
    设置是否响应暂停按钮

    :param pause: bool True为可打开暂停页面
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanPause(pause)


def set_can_chat(chat):
    """
    设置是否响应聊天按钮

    :param chat: bool True为可打开聊天页面
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanChat(chat)


def set_can_screen_shot(shot):
    """
    设置是否响应截图按钮

    :param shot: bool True为可截图
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanScreenShot(shot)


def set_can_open_inv(open_inv):
    """
    设置是否响应打开背包按钮

    :param open_inv: True为可打开背包
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanOpenInv(open_inv)


def set_can_drag(drag):
    """
    设置是否响应屏幕拖动

    :param drag: True为可拖动屏幕
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanDrag(drag)


def set_can_in_air(in_air):
    """
    设置是否响应上升下降按钮（飞在空中时右下角的三个按钮）

    :param in_air: bool True为可点击
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanInair(in_air)


def set_can_all(all_operation):
    """
    一次性设置除SetMoveLock之外的所有属性

    要在其他属性设置之前设置，不然在all之前设置的会被覆盖掉

    :param all_operation: bool True为全部响应
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetCanAll(all_operation)


def set_move_lock(move_lock):
    """
    设置是否锁住移动。实际上为是否响应十字键与遥感的操作。

    与SetCanMove的区别：调用SetCanMove会清除当前Input Vector，例如玩家一直按着前进键，调用SetCanMove(False)会立即停下来，调用SetMoveLock(True)则不会。

    :param move_lock: bool True为锁住
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetMoveLock(move_lock)


def set_can_operation(operation, state):
    """
    TODO

    :param operation:
    :param state:
    :return:
    """
    return {
        'move': set_can_move(state),
        'jump': set_can_jump(state),
        'attack': set_can_attack(state),
        'walk_mode': set_can_walk_mode(state),
        'perspective': set_can_perspective(state),
        'pause': set_can_pause(state),
        'chat': set_can_chat(state),
        'screen_shot': set_can_screen_shot(state),
        'open_inv': set_can_open_inv(state),
        'drag': set_can_drag(state),
        'in_air': set_can_in_air(state),
        'all': set_can_all(state),
        'move_lock': set_move_lock(state),
    }.get(operation, False)


def set_hold_time_threshold(time):
    """
    设置长按判定时间，即按着屏幕多长时间会触发长按操作

    :param time: int 时间，单位毫秒。默认为400
    :return: bool 设置是否成功
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.SetHoldTimeThreshold(time)


def get_hold_time_threshold_in_ms():
    """
    获取长按判定时间，即按着屏幕多长时间会触发长按操作

    :return: int 时间，单位毫秒。默认为400
    """
    operation_comp = clientApi.GetEngineCompFactory().CreateOperation(level_id)
    return operation_comp.GetHoldTimeThresholdInMs()


def set_device_vibrate(milli_seconds):
    """
    设置设备震动

    * 设置时间区间为[1,5000]毫秒，如果milliSeconds参数大于该区间将会被设置为5000毫秒，小于则设为1毫秒
    * 调用时距离上次震动结束的时间不能短于2秒，如果短于2秒本次设置将会失败
    * 设置震动失败（函数返回False）的可能原因：距离上次震动结束还未超过2秒、当前已经处于震动状态、设备不支持震动等
    * 即使函数返回值为True，也有可能因为未正确判断设备是否支持震动、设备权限上禁止震动等原因未能真正震动
    * 在目前版本中还不支持对IOS设备进行震动

    :param milli_seconds: int 震动时间（单位：毫秒）
    :return: bool 设置是否成功
    """
    device_comp = clientApi.GetEngineCompFactory().CreateDevice(local_player)
    return device_comp.SetDeviceVibrate(milli_seconds)


def get_perspective(entity_id):
    """
    获取当前的视角模式

    :param entity_id:
    :return: int 0：第一人称视角；1：第三人称视角；2：前视第三人称视角
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(entity_id)
    return view_comp.GetPerspective()


def set_perspective(entity_id, perspective):
    """
    设置视角模式

    :param entity_id:
    :param perspective: int 0：第一人称视角；1：第三人称视角；2：前视第三人称视角
    :return: bool 设置是否成功
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(entity_id)
    return view_comp.SetPerspective(perspective)


def lock_perspective(entity_id, perspective):
    """
    锁定玩家的视角模式

    :param entity_id:
    :param perspective: int 0：第一人称视角；1：第三人称视角；2：前视第三人称视角 其他值：解除锁定
    :return: bool 是否锁定成功
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(entity_id)
    return view_comp.LockPerspective(perspective)


def get_ui_profile():
    """
    获取"UI 档案"模式

    :return: 0表示经典模式，1表示Pocket模式
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(level_id)
    return view_comp.GetUIProfile()


def set_ui_profile(profile_type):
    """
    设置"UI 档案"模式

    :param profile_type: int 0表示经典模式，1表示Pocket模式
    :return: 0表示经典模式，1表示Pocket模式
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(level_id)
    return view_comp.SetUIProfile(profile_type)


def get_toggle_option(option_id):
    """
    获得某个开关设置值的接口

    :param option_id: str [OptionId]枚举
    :return: -1：类型不支持；0：开关关闭； 1: 开关打开；
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(level_id)
    return view_comp.GetToggleOption(option_id)


def set_toggle_option(option_id, on):
    """
    修改开关型设置的接口

    :param option_id: str [OptionId]枚举
    :param on: bool 是否打开开关，True为开，False为关
    :return: -1：类型不支持；0：开关关闭； 1: 开关打开；
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(level_id)
    return view_comp.SetToggleOption(option_id, on)


def highlight_box_selection(is_highlight):
    """
    镜头移动时高亮当前视角中心所指的方块

    功能实现上面其实是 设置->视频->轮廓设置 的一层代码封装，但不会影响到原本轮廓设置的值，如果设置为高亮，效果与关闭轮廓设置时相同，如果设置为非高亮，效果则取决于当前是否设置了轮廓设置，如果设置了，则不高亮。
    
    重启后设置失效

    :param is_highlight: bool 是否高亮，True为高亮，False为不高亮，默认为不高亮
    :return: -1：类型不支持；0：开关关闭； 1: 开关打开；
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(level_id)
    return view_comp.HighlightBoxSelection(is_highlight)


def set_split_control_can_change(can_change):
    """
    设置是否允许使用准星瞄准按钮

    :param can_change: bool 是否允许
    :return: bool 设置是否成功
    """
    view_comp = clientApi.GetEngineCompFactory().CreatePlayerView(level_id)
    return view_comp.SetSplitControlCanChange(can_change)
