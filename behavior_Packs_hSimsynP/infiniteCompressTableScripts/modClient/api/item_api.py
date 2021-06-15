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

    http://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E7%89%A9%E5%93%81/GetItemBasicInfo.html#%E5%AE%A2%E6%88%B7%E7%AB%AF%E6%8E%A5%E5%8F%A3

    1.22 调整 新增itemCategory,itemType,itemTierLevel字段

    1.21 调整 新增idAux字段，用于ui物品控件的绑定

    1.20 调整 返回信息新增挖掘相关属性tierDict

    :param item_name: str item的identifier
    :param aux_value: int 物品的附加值aux_value
    :return: dict 基础信息字典，如果物品不存在，返回值为None
        itemName: str 本地化的物品名字
        maxStackSize: int 物品最大堆叠数目
        maxDurability: int 物品最大耐久值
        idAux: int 用于给UI的inventory_item_renderer类型控件绑定#item_id_aux字段，详见
        tierDict: dict 自定义方块定义的挖掘相关的属性 netease:tier,没有设置时返回None
        itemCategory: str 创造栏分类
        itemType: str 物品类型
        itemTierLevel: int 工具等级
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


def get_recipes_by_input(input_identifier, tag, aux, max_result_num):
    """
    通过输入物品查询配方

    在获取酿造台配方时，不匹配tag标签与aux值，药水的identifier需要输入全称，例如：minecraft:potion_type:long_turtle_master，否则无法获取正确的配方。

    需要遍历较多数据，不建议频繁调用

    :param input_identifier: str 输入物品的标识符
    :param tag: str 对应配方json中的tags字段里面的值
    :param aux: int 输出物品的附加值, 不传参的话默认为0
    :param max_result_num: int 最大输出条目数，若大于等于0时，结果超过maxResultNum，则只返回maxResultNum条。默认-1，表示返回全部
    :return: list(dict)	返回符合条件的配方列表
    """
    recipe_comp = clientApi.GetEngineCompFactory().CreateRecipe(level_id)
    return recipe_comp.GetRecipesByInput(input_identifier, tag, aux, max_result_num)


def get_recipes_by_result(result_identifier, tag, aux=0):
    """
    通过输出物品查询配方所需要的输入材料

    若配方为酿造台配方时，由于原版实现没有存储相应信息，不匹配tag标签与aux值

    1.20 新增 通过输出物品查询配方所需要的输入材料

    :param result_identifier: str 输出物品的标识符
    :param tag: str 对应配方json中的tags字段里面的值
    :param aux: int 输出物品的附加值, 不传参的话默认为0
    :return: list(dict) 返回符合条件的配方列表
    """
    recipe_comp = clientApi.GetEngineCompFactory().CreateRecipe(level_id)
    return recipe_comp.GetRecipesByResult(result_identifier, tag, aux)


def change_item_texture(identifier, texture_path):
    """
    替换物品的贴图，修改后所有用到该贴图的物品都会被改变，后续创建的此类物品也会被改变。

    会同时修改物品在UI界面上的显示，手持时候的显示与场景掉落的显示。

    :param identifier: str 物品标识符，格式[namespace:name:auxvalue]，auxvalue默认为0
    :param texture_path: str 打算替换成的贴图的路径
    :return: bool 是否设置成功（因为采用延迟加载，此处返回成功不代表贴图路径正确，路径错误会导致渲染时贴图丢失显示异常）
    """
    item_comp = clientApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.ChangeItemTexture(identifier, texture_path)
