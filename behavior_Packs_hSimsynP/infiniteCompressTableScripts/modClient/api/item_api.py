# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()


def get_offhand_item(entity_id, get_user_data=False):
    """
    获取左手物品的信息

    :param entity_id:
    :param get_user_data: bool 是否获取物品的userData，默认为False
    :return: dict [物品信息字典]，没有物品则返回None
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(entity_id)
    return item_comp.GetOffhandItem(get_user_data)


def get_carried_item(entity_id, get_user_data=False):
    """
    获取右手物品的信息

    :param entity_id:
    :param get_user_data: bool 是否获取物品的userData，默认为False
    :return: dict [物品信息字典]，没有物品则返回None
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(entity_id)
    return item_comp.GetCarriedItem(get_user_data)


def get_slot_id(entity_id):
    """
    获取当前手持的快捷栏的槽id

    :param entity_id:
    :return: int 0到8
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(entity_id)
    return item_comp.GetSlotId()


def get_item_basic_info(item_name, aux_value=0):
    """
    获取物品的基础信息

    1.20 调整 返回信息新增挖掘相关属性tierDict

    :param item_name: str item的identifier
    :param aux_value: int 物品的附加值aux_value
    :return: dict 基础信息字典，如果物品不存在，返回值为None
        itemName: str 本地化的物品名字
        maxStackSize: int 物品最大堆叠数目
        maxDurability: int 物品最大耐久值
        tierDict: dict 自定义方块定义的挖掘相关的属性 netease:tier,没有设置时返回None
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.GetItemBasicInfo(item_name, aux_value)


def get_item_formatted_hover_text(item_name, aux_value=0, show_category=False, user_data=None):
    """
    获取物品的格式化hover文本，如：§f灾厄旗帜§r

    1.18 新增 获取物品格式化hover文本

    :param item_name: str item的identifier
    :param aux_value: int 物品的附加值auxValue，默认为不指定auxValue（0）
    :param show_category: bool 是否包括item的类别信息，默认False
    :param user_data: dict 物品userData，默认为None
    :return: str 物品的格式化hover文本
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.GetItemFormattedHoverText(item_name, aux_value, show_category, user_data)


def get_item_hover_name(item_name, aux_value=0, user_data=None):
    """
    获取物品的hover名称，如：灾厄旗帜§r

    1.18 新增 获取物品的Hover名称

    :param item_name: str item的identifier
    :param aux_value: int 物品的附加值auxValue，默认为不指定auxValue（0）
    :param user_data: dict 物品userData，默认为None
    :return: str 物品hover名称
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.GetItemHoverName(item_name, aux_value, user_data)


def get_item_effect_name(item_name, aux_value=0, user_data=None):
    """
    获取物品的状态描述，如：§7保护 0§r

    1.18 新增 获取物品的状态描述

    :param item_name: str item的identifier
    :param aux_value: int 物品的附加值auxValue，默认为不指定auxValue（0）
    :param user_data: dict 物品userData，默认为None
    :return: str 物品的状态描述
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.GetItemEffectName(item_name, aux_value, user_data)


def get_user_data_in_event(event_name):
    """
    使物品相关客户端事件的[物品信息字典]参数带有userData。在mod初始化时调用即可

    1.20 新增 可以用物品相关客户端事件的参数中获取userData

    :param event_name: str 引擎事件名
    :return: bool 是否成功
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.GetUserDataInEvent(event_name)
