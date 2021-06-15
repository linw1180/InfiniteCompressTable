# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()


def get_block(pos):
    """
    获取某一位置的block

    已经加载的地形才设置、获取方块信息

    :param pos: tuple(float,float,float) 方块位置
    :return: tuple(str,int) 参数1:方块的名称，参数2:方块的附加值AuxValue
    """
    block_info_comp = clientApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.GetBlock(pos)


def get_destroy_total_time(block_name, item_name=None):
    """
    获取使用物品破坏方块需要的时间

    1.22 新增 获取使用物品破坏方块需要的时间

    :param block_name: str 方块标识符，格式[namespace:name:auxvalue]，auxvalue默认为0
    :param item_name: str 物品标识符，格式[namespace:name:auxvalue]，auxvalue默认为0，默认为None（不使用物品）
    :return: int 高度
    """
    block_info_comp = clientApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.GetDestroyTotalTime(block_name, item_name)


def get_top_block_height(pos):
    """
    获取当前维度某一位置最高的非空气方块的高度

    :param pos: tuple(int,int) x轴与z轴位置
    :return: int 高度
    """
    block_info_comp = clientApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.GetTopBlockHeight(pos)


def change_block_textures(block_name, tile_name, texture_path):
    """
    替换方块贴图

    对纹理会动态变化的方块无效

    调用此接口后tileName不会发生变化，后续如果想恢复设置，依旧需要用这个tileName

    :param block_name: str 方块标识符，格式[namespace:name:auxvalue]，auxvalue默认为0; 只支持普通的没有特殊渲染逻辑的方形方块，否则可能会显示异常
    :param tile_name: str 原贴图在图集中对应的名字，对应terrain_texture.json中的配置
    :param texture_path: str 打算替换成的贴图的路径
    :return: bool 是否设置成功（因为采用延迟加载，此处返回成功不代表贴图路径正确，路径错误会导致渲染时贴图丢失显示异常）
    """
    block_info_comp = clientApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.ChangeBlockTextures(block_name, tile_name, texture_path)


def add_block_item_listen_for_use_event(block_name):
    """
    增加blockName方块对ClientBlockUseEvent事件的脚本层监听

    1.19 新增 增加原版方块对ClientBlockUseEvent事件的脚本层监听

    :param block_name: str 方块名称，格式：namespace:name:AuxValue，其中namespace:name:*匹配所有的方块数据值AuxValue
        如果不填AuxValue，则默认为0
    :return: bool 是否增加成功
    """
    block_use_event_white_list_comp = clientApi.GetEngineCompFactory().CreateBlockUseEventWhiteList(level_id)
    return block_use_event_white_list_comp.AddBlockItemListenForUseEvent(block_name)


def clear_all_block_item_listen_for_use_event():
    """
    清空所有已添加方块对ClientBlockUseEvent事件的脚本层监听

    1.19 新增 清空原版方块白名单列表对ClientBlockUseEvent事件的脚本层监听

    :return: bool 是否清空成功
    """
    block_use_event_white_list_comp = clientApi.GetEngineCompFactory().CreateBlockUseEventWhiteList(level_id)
    return block_use_event_white_list_comp.ClearAllListenForBlockUseEventItems()


def remove_block_item_listen_for_use_event(block_name):
    """
    移除blockName方块对ClientBlockUseEvent事件的脚本层监听

    1.19 新增 移除原版方块对ClientBlockUseEvent事件的脚本层监听

    :param block_name: str 方块名称，格式：namespace:name:AuxValue，其中namespace:name:*匹配所有的方块数据值AuxValue
    :return: bool 是否移除成功
    """
    block_use_event_white_list_comp = clientApi.GetEngineCompFactory().CreateBlockUseEventWhiteList(level_id)
    return block_use_event_white_list_comp.RemoveBlockItemListenForUseEvent(block_name)
