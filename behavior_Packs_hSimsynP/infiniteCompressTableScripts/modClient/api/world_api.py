# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()
local_player = clientApi.GetLocalPlayerId()


def add_chunk_pos_white_list(dimension, pos):
    """
    为某区块加载完成、准备卸载事件添加监听
    
    方块坐标(x, y, z)所在的区块坐标为(math.floor(x / 16), math.floor(z / 16))
    
    :param dimension: int 区块所在维度
    :param pos: tuple(int,int) 指定区块的坐标
    :return: bool 是否添加成功
    """
    chunk_comp = clientApi.GetEngineCompFactory().CreateChunkSource(local_player)
    return chunk_comp.AddChunkPosWhiteList(dimension, pos)


def remove_chunk_pos_white_list(dimension, pos):
    """
    移除对某区块加载完成、准备卸载事件的监听

    方块坐标(x, y, z)所在的区块坐标为(math.floor(x / 16), math.floor(z / 16))

    :param dimension: int 区块所在维度
    :param pos: tuple(int,int) 指定区块的坐标
    :return: bool 是否移除成功
    """
    chunk_comp = clientApi.GetEngineCompFactory().CreateChunkSource(local_player)
    return chunk_comp.RemoveChunkPosWhiteList(dimension, pos)


def get_chunk_pos_from_block_pos(block_pos):
    """
    通过方块坐标获得该方块所在区块坐标

    当传入的blockPos类型不是tuple或者长度不为3时，返回值为None

    :param block_pos: tuple(int,int,int) 方块的坐标
    :return: None或tuple(int,int) 该方块所在区块的坐标
    """
    chunk_comp = clientApi.GetEngineCompFactory().CreateChunkSource(local_player)
    return chunk_comp.GetChunkPosFromBlockPos(block_pos)


def show_health_bar(show=True):
    """
    设置是否显示血条
    
    :param show: bool True为显示。开启后可用health组件单独设置某个实体的血条颜色及是否显示
    :return: bool 设置是否成功
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.ShowHealthBar(show)


def set_name_deep_test(deep_test=True):
    """
    设置名字是否透视
    
    :param deep_test: bool True为不透视。默认情况下为透视
    :return: bool 设置是否成功
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetNameDeeptest(deep_test)


def get_screen_size():
    """
    获取游戏分辨率

    :return: tuple(float,float) 宽高（像素）
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetScreenSize()


def set_render_local_player(render=False):
    """
    设置本地玩家是否渲染

    :param render: bool True为渲染
    :return: bool 设置是否成功
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetRenderLocalPlayer(render)


def add_pick_blacklist(entity_id):
    """
    添加使用camera组件选取实体时的黑名单，即该实体不会被选取到

    :param entity_id: str 实体id
    :return: bool 设置是否成功
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.AddPickBlacklist(entity_id)


def clear_pick_blacklist():
    """
    清除使用camera组件选取实体的黑名单

    :return: bool 设置是否成功
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.ClearPickBlacklist()


def get_current_dimension():
    """
    获取客户端当前维度

    :return: int 维度id。客户端未登录完成或正在切维度时返回-1
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetCurrentDimension()


def get_entity_in_area(pos_a, pos_b, entity_id=None, except_entity=False):
    """
    返回区域内的实体，可获取到区域范围内已加载的实体列表

    1.20 调整 支持传入entityId为None，此时exceptEntity无作用，可获取到区域范围内已加载的实体列表

    :param pos_a: tuple(int,int,int) 起点
    :param pos_b: tuple(int,int,int) 终点，终点应大于起点
    :param entity_id: str或None 实体Id
    :param except_entity: bool 返回结果中是否除去entityId, 默认为False，传入entityId为None时exceptEntity无作用
    :return: list(str) 区域范围内已加载的entityId列表
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetEntityInArea(entity_id, pos_a, pos_b, except_entity)


def has_entity(entity_id):
    """
    判断 entity 是否存在

    :param entity_id: str 实体id
    :return: int 0表示不存在，1表示存在
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.HasEntity(entity_id)


def is_entity_alive(entity_id):
    """
    判断生物实体是否存活或非生物实体是否存在

    注意，如果检测的实体所在的区块被卸载，则该接口返回False。因此，需要注意实体所在的区块是否被加载。

    :param entity_id: str 实体id
    :return: bool false表示生物实体已死亡或非生物实体已销毁，true表示生物实体存活或非生物实体存在
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.IsEntityAlive(entity_id)


def check_words_valid(words):
    """
    检查语句是否合法，即不包含敏感词

    :param words: str 语句
    :return: bool True:语句合法 False:语句非法
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.CheckWordsValid(words)


def check_name_valid(name):
    """
    检查昵称是否合法，即不包含敏感词

    :param name: str 昵称
    :return: bool True:昵称合法 False:昵称非法
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.CheckNameValid(name)


def get_screen_view_info():
    """
    获取游戏视角信息。分辨率为1313，618时，画布是376，250的2倍，所以viewport得到的是1313 + (2-(1313%2))，y值类似

    可参考《我的世界》界面适配方法
        http://mc.163.com/mcstudio/mc-dev/MCDocs/1-MC%20Studio%E5%BC%80%E5%8F%91%E5%B7%A5%E5%85%B7/6-%E7%95%8C%E9%9D%A2%E7%BC%96%E8%BE%91%E5%99%A8%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.html#%E3%80%8A%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C%E3%80%8B%E7%95%8C%E9%9D%A2%E9%80%82%E9%85%8D%E6%96%B9%E6%B3%95

    :return: tuple(float,float,float,float) 依次为宽、高、x偏移、y偏移
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetScreenViewInfo()


def set_popup_notice(message, subtitle):
    """
    在本地玩家的物品栏上方弹出popup类型通知，位置位于tip类型消息下方

    :param message: str 消息内容,可以在消息前增加extraClientApi.GenerateColor("RED")字符来设置颜色，具体参考样例
    :param subtitle: str 消息子标题内容,效果同message，也可设置颜色，位置位于message上方
    :return: bool 设置是否成功
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(local_player)
    return game_comp.SetPopupNotice(message, subtitle)


def set_tip_message(message):
    """
    在本地玩家的物品栏上方弹出tip类型通知，位置位于popup类型通知上方

    :param message: str 消息内容,可以在消息前增加extraClientApi.GenerateColor("RED")字符来设置颜色，具体参考样例
    :return: bool 设置是否成功
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(local_player)
    return game_comp.SetTipMessage(message)


def add_timer(delay, func, *args, **kwargs):
    """
    添加客户端触发的定时器，非重复

    :param delay: float 延迟时间，单位秒
    :param func: function 定时器触发函数
    :param args: any 变长参数，可以不设置
    :param kwargs: any 字典变长参数，可以不设置
    :return: CallLater 返回单次触发的定时器实例
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.AddTimer(delay, func, *args, **kwargs)


def add_repeated_timer(delay, func, *args, **kwargs):
    """
    添加客户端触发的定时器，重复执行

    :param delay: float 延迟时间，单位秒
    :param func: function 定时器触发函数
    :param args: any 变长参数，可以不设置
    :param kwargs: any 字典变长参数，可以不设置
    :return: CallLater 返回触发的定时器实例
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.AddRepeatedTimer(delay, func, *args, **kwargs)


def cancel_timer(timer):
    """
    取消定时器

    :param timer: CallLater AddOnceTimer和AddRepeatedTimer时返回的定时器实例
    :return:
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.CancelTimer(timer)


def simulate_touch_with_mouse(touch):
    """
    模拟使用鼠标控制UI（PC F11快捷键）

    :param touch: bool True:进入鼠标模式，False:退出鼠标模式
    :return: bool 模拟结果
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SimulateTouchWithMouse(touch)


def get_chinese(lang_str):
    """
    获取langStr对应的中文，可参考PC开发包中resource_pack/texts/zh_CN.lang

    :param lang_str: str 传入的langStr
    :return: str langStr对应的中文，若找不到对应的中文，则会返回langStr本身
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetChinese(lang_str)


def set_actor_collision(entity_id, collision):
    """
    设置实体是否可碰撞

    :param entity_id:
    :param collision: bool True:可碰撞  False:不可碰撞
    :return: bool True表示设置成功
    """
    collision_comp = clientApi.GetEngineCompFactory().CreateActorCollidable(entity_id)
    return collision_comp.SetActorCollidable(1 if collision else 0)
