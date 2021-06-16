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


def get_top_block_height(pos):
    """
    获取当前维度某一位置最高的非空气方块的高度

    :param pos: tuple(int,int) x轴与z轴位置
    :return: int 高度
    """
    block_info_comp = clientApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.GetTopBlockHeight(pos)


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
