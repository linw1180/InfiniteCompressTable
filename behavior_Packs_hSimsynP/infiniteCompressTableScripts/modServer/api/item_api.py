# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def get_chest_block_container_size(player_id, pos, dimension=-1):
    """
    获取箱子容量大小
    
    1.20 调整 新增dimension参数，默认为-1，传入非负值时不依赖player_id，可获取对应维度的常加载区块内箱子容量

    :param player_id: str或None 玩家id/None
    :param pos: tuple(int,int,int) 箱子位置
    :param dimension: int 箱子所在维度，默认为-1，传入非负值时不依赖player_id，player_id可传入None，可获取对应维度的常加载区块内箱子容量
    :return: int 箱子大小,错误值-1
    """
    if dimension > -1:
        chest_block_comp = serverApi.GetEngineCompFactory().CreateChestBlock(level_id)
        return chest_block_comp.GetChestBoxSize(None, pos, dimension)

    chest_block_comp = serverApi.GetEngineCompFactory().CreateChestBlock(player_id)
    return chest_block_comp.GetChestBoxSize(player_id, pos)


def set_chest_block_item_num(player_id, pos, slot_pos, num, dimension=-1):
    """
    设置箱子槽位物品数目

    1.20 调整 增加参数dimension，默认为-1，传入非负值时不依赖player_id，可在对应维度的常加载区块设置箱子内物品数量

    :param player_id: str或None 玩家id/None
    :param pos: tuple(int,int,int) 箱子位置
    :param slot_pos: int 箱子槽位
    :param num: int 物品数目
    :param dimension: int 方块所在维度，默认值为-1，传入非负值时不依赖player_id，player_id可传入None，可在对应维度的常加载区块设置方块
    :return: bool 设置结果
    """
    if dimension > -1:
        chest_block_comp = serverApi.GetEngineCompFactory().CreateChestBlock(level_id)
        return chest_block_comp.SetChestBoxItemNum(None, pos, slot_pos, num, dimension)

    chest_block_comp = serverApi.GetEngineCompFactory().CreateChestBlock(player_id)
    return chest_block_comp.SetChestBoxItemNum(player_id, pos, slot_pos, num)


def exchange_chest_block_item(player_id, pos, slot_pos1, slot_pos2):
    """
    交换箱子里物品的槽位

    1.18 新增 新增交换箱子物品接口

    :param player_id: str 玩家id
    :param pos: tuple(int,int,int) 箱子位置
    :param slot_pos1: int 箱子槽位1
    :param slot_pos2: int 箱子槽位2
    :return: bool 设置成功返回True，失败返回False
    """
    chest_block_comp = serverApi.GetEngineCompFactory().CreateChestBlock(player_id)
    return chest_block_comp.SetChestBoxItemExchange(player_id, pos, slot_pos1, slot_pos2)


def add_banned_item(item_info):
    """
    增加禁用物品

    也可以通过填写配置文件config/banned_items.json进行启动禁用
    
    :param item_info: str 物品标识符，格式[namespace:name:auxvalue]，auxvalue默认为0，auxvalue为*时候匹配任意auxvalue值。例如：minecraft:egg:*
    :return: bool 是否增加成功
    """
    item_banned_comp = serverApi.GetEngineCompFactory().CreateItemBanned(level_id)
    return item_banned_comp.AddBannedItem(item_info)


def remove_banned_item(item_info):
    """
    移除禁用物品
    
    :param item_info: str 物品标识符，格式[namespace:name:auxvalue]，auxvalue默认为0，auxvalue为*时候匹配任意auxvalue值。
    :return: bool 是否移除成功
    """
    item_banned_comp = serverApi.GetEngineCompFactory().CreateItemBanned(level_id)
    return item_banned_comp.RemoveBannedItem(item_info)


def clear_banned_items():
    """
    清空禁用物品

    :return: bool 是否清空成功
    """
    item_banned_comp = serverApi.GetEngineCompFactory().CreateItemBanned(level_id)
    return item_banned_comp.ClearBannedItems()


def spawn_item_to_level(item_dict, dimension, pos):
    """
    生成物品掉落物，如果需要获取物品的entityId，可以调用服务端系统接口CreateEngineItemEntity

    :param item_dict: dict [物品信息字典]
    :param dimension: int 设置dimension
    :param pos: tuple(float,float,float) 生成位置
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.SpawnItemToLevel(item_dict, dimension, pos)


def spawn_item_to_player_carried(item_dict, player_id):
    """
    生成物品到玩家右手
    
    :param item_dict: dict [物品信息字典]
    :param player_id: str 玩家id
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SpawnItemToPlayerCarried(item_dict, player_id)


def spawn_item_to_player_offhand(item_dict, player_id):
    """
    生成物品到玩家左手

    :param item_dict: dict [物品信息字典]
    :param player_id: str 玩家id
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SpawnItemToPlayerOffHand(item_dict, player_id)


def clear_player_offhand(player_id):
    """
    清除玩家左手物品

    1.19 新增 清除玩家左手物品

    :param player_id: str 玩家id
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.ClearPlayerOffHand(player_id)


def spawn_item_to_player_inv(item_dict, player_id, slot_pos=-1):
    """
    生成物品到玩家背包

    当slotPos不设置时，当设置的数量超过单个槽位堆叠的上限时，会将多余的物品设置到另外的空闲槽位.如果生成的物品与背包中有的槽位的物品种类一致，该接口也会将物品增加到这些槽位中。

    注意：如果背包中剩余的物品数目和增加的物品数目之和大于64，则会生成物品数目到64，但是接口返回失败。

    :param item_dict: dict [物品信息字典]
    :param player_id: str 玩家id
    :param slot_pos: int 背包槽位(可选)
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SpawnItemToPlayerInv(item_dict, player_id, slot_pos)


def spawn_item_to_chest_block(item_dict, player_id, slot_pos, block_pos, dimension=-1):
    """
    生成物品到箱子

    1.20 调整 增加参数dimension，默认为-1，传入非负值时不依赖player_id，可生成物品到对应维度的常加载区块内的箱子

    :param item_dict: dict [物品信息字典]
    :param player_id: str或None 玩家id/None
    :param slot_pos: int 箱子槽位
    :param block_pos: tuple(int,int,int) 箱子位置
    :param dimension: int 方块所在维度，默认值为-1，传入非负值时不依赖player_id，player_id可传入None，可生成物品到对应维度的常加载区块内的箱子
    :return: bool 设置结果
    """
    if dimension > -1:
        item_comp = serverApi.GetEngineCompFactory().CreateItem(level_id)
        return item_comp.SpawnItemToChestBlock(item_dict, None, slot_pos, block_pos, dimension)

    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SpawnItemToChestBlock(item_dict, player_id, slot_pos, block_pos)


def spawn_item_to_player_armor(item_dict, player_id, slot_pos):
    """
    生成物品到玩家装备位

    1.18 新增 添加物品到玩家装备位

    :param item_dict: dict [物品信息字典]
    :param player_id: str 玩家id
    :param slot_pos: int ArmorSlotType，装备位置，具体请看宏定义GetMinecraftEnum().ArmorSlotType.*
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SpawnItemToArmor(item_dict, player_id, slot_pos)


def get_player_item(player_id, slot_type, slot_pos=0, get_user_data=False):
    """
    获取玩家物品，支持获取背包，盔甲栏，副手以及主手物品
    
    :param player_id: str 玩家id
    :param slot_type: int [ItemPosType]枚举
    :param slot_pos: int 槽位，获取INVENTORY及ARMOR时需要设置，其他情况写0即可
    :param get_user_data: bool 是否获取userData，默认为False
    :return: dict [物品信息字典]，没有物品则返回None
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.GetPlayerItem(slot_type, slot_pos, get_user_data)


def change_player_item_tips_and_extra_id(player_id, slot_type, slot_pos=0, custom_tips="", extra_id=""):
    """
    修改玩家物品的自定义tips和自定义标识符

    :param player_id: str 玩家id
    :param slot_type: int [ItemPosType]枚举
    :param slot_pos: int 箱子槽位
    :param custom_tips: str 物品的自定义tips
    :param extra_id: str 物品的自定义标识符
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.ChangePlayerItemTipsAndExtraId(slot_type, slot_pos, custom_tips, extra_id)


def add_enchant_to_player_inv_item(player_id, slot_pos, enchant_type, level):
    """
    给物品栏的物品添加附魔信息
    
    :param player_id: 
    :param slot_pos: int 物品栏槽位
    :param enchant_type: int 附魔类型，可以查看枚举值文档
    :param level: int 附魔等级
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.AddEnchantToInvItem(slot_pos, enchant_type, level)


def get_player_inv_item_enchant(player_id, slot_pos):
    """
    获取物品栏的物品附魔信息

    :param player_id:
    :param slot_pos: int 物品栏槽位
    :return: list(tuple(int,int)) list中每个tuple由附魔类型([EnchantType]枚举)和附魔等级组成。没有附魔则为空list
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.GetInvItemEnchant(slot_pos)


def set_player_inv_item_num(player_id, slot_pos, num):
    """
    设置玩家背包物品数目

    :param player_id:
    :param slot_pos: int 物品栏槽位
    :param num: int 物品数目
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SetInvItemNum(slot_pos, num)


def exchange_player_inv_item(player_id, pos1, pos2):
    """
    交换玩家背包物品

    :param player_id:
    :param pos1: int 物品位置
    :param pos2: int 物品位置
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SetInvItemExchange(pos1, pos2)


def set_player_inv_item_durability(player_id, slot_pos, durability):
    """
    设置背包物品的耐久值

    设置的耐久值超过物品的最大耐久值时，使用最大耐久值；最小耐久值为0。当slot值为-1时，设置左手物品的耐久值

    :param player_id:
    :param slot_pos: int 物品槽位
    :param durability: int 耐久值
    :return: bool 设置结果
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SetInvItemDurability(slot_pos, durability)


def get_player_inv_item_durability(player_id, slot_pos):
    """
    获取背包物品的耐久值

    如果物品不存在，返回值为None。当slot值为-1时，获取左手物品的耐久值

    :param player_id:
    :param slot_pos: int 物品槽位
    :return: int 物品的耐久值
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.GetInvItemDurability(slot_pos)


def set_equipment_durability(entity_id, slot_pos, durability):
    """
    设置装备槽位中盔甲的耐久值

    设置的耐久值超过物品的最大耐久值时，使用最大耐久值；最小耐久值为0

    1.19 调整 新增支持设置生物装备槽位中盔甲的耐久值
    :param entity_id:
    :param slot_pos: int [ArmorSlotType]枚举
    :param durability: int 耐久值
    :return:
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(entity_id)
    return item_comp.SetEquItemDurability(slot_pos, durability)


def get_equipment_durability(entity_id, slot_pos):
    """
    获取装备槽位中盔甲的耐久值

    :param entity_id:
    :param slot_pos: int [ArmorSlotType]枚举
    :return: int 盔甲的耐久值，如果物品不存在，返回值为None
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(entity_id)
    return item_comp.GetEquItemDurability(slot_pos)


def get_item_entity_data(item_entity_id, get_user_data=False):
    """
    获取掉落在世界的指定entity_id的物品信息
    
    :param item_entity_id: str itemEntity的entityId
    :param get_user_data: bool 是否获取userData，默认为False
    :return: dict 物品字典信息，如果物品不存在，返回值为None
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.GetDroppedItem(item_entity_id, get_user_data)


def get_equipment_enchant(entity_id, slot_pos):
    """
    获取装备槽位中盔甲的附魔

    1.19 调整 支持获取生物装备槽位中盔甲的附魔

    :param entity_id:
    :param slot_pos: int [ArmorSlotType]枚举
    :return: 如果物品不存在，或者没有附魔值，返回None。如果存在返回tuple数组，每个tuple由附魔类型([EnchantType]和附魔等级组成
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(entity_id)
    return item_comp.GetEquItemEnchant(slot_pos)


def get_item_basic_info(item_name, aux_value=0):
    """
    获取物品的基础信息

    1.20 调整 返回信息新增挖掘相关属性tierDict

    :param item_name: str item的identifier
    :param aux_value: int 物品的附加值auxValue
    :return: dict
        itemName: str 本地化的物品名字
        maxStackSize: int 物品最大堆叠数目
        maxDurability: int 物品最大耐久值
        tierDict: dict 自定义方块定义的挖掘相关的属性 netease:tier,没有设置时返回None
    如果物品不存在，返回值为None
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(level_id)
    return item_comp.GetItemBasicInfo(item_name, aux_value)


def get_player_all_items(player_id, pos_type, get_user_data=False):
    """
    获取玩家指定的槽位的批量物品信息

    :param player_id:
    :param pos_type: int [ItemPosType]枚举
    :param get_user_data: bool 是否获取userData，默认为False
    :return: list(dict) [物品信息字典]的数组，没有物品的位置为None
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.GetPlayerAllItems(pos_type, get_user_data)


def set_player_all_items(player_id, items_dict_map):
    """
    添加批量物品信息到指定槽位

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/02-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-ModAPI/4-%E7%BB%84%E4%BB%B6/2-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E7%BB%84%E4%BB%B6.html#setplayerallitems

    :param player_id:
    :param items_dict_map: dict 需要添加的物品的字典，字典的key是tuple([ItemPosType], slotPos)，value是需要添加的[物品信息字典]
    :return: dict 设置结果，字典的key是tuple(ItemPosType, slot)，value为bool代表该槽位设置是否成功
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SetPlayerAllItems(items_dict_map)


def get_entity_item(entity_id, pos_type, slot_pos=0, get_user_data=False):
    """
    获取生物物品，支持获取背包，盔甲栏，副手以及主手物品

    左右手及装备可以替代GetPlayerItem接口获取玩家的物品，**但背包不行**。获取生物背包目前支持驴、骡、羊驼以及其他带背包的自定义生物

    :param entity_id:
    :param pos_type: int [ItemPosType]枚举
    :param slot_pos: int 槽位，获取INVENTORY及ARMOR时需要设置，其他情况写0即可
    :param get_user_data: bool 是否获取userData，默认为False
    :return: dict 物品信息字典，没有物品则返回None
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(entity_id)
    return item_comp.GetEntityItem(pos_type, slot_pos, get_user_data)


def set_entity_item(entity_id, pos_type, item_dict, slot_pos=0):
    """
    设置生物物品，建议开发者根据生物特性来进行设置，部分生物设置装备后可能不显示但是死亡后仍然会掉落所设置的装备

    设置生物背包目前支持驴、骡、羊驼以及其他带背包的自定义生物。

    该接口与spawnTo系列接口相比多了槽位限制，只能设置对应槽位的装备、左手物品，并且右手不能设置装备。溺尸暂不支持设置自定义装备。

    :param entity_id:
    :param pos_type: int [ItemPosType]枚举
    :param item_dict: dict 生物身上不同位置的[物品信息字典]列表，如果传入None将清除当前位置的物品/装备
    :param slot_pos: int 容器槽位
        如果ItemPosType为左右手可不传
        如果ItemPosType为背包则对应背包槽位
        如果ItemPosType为armor则对应装备位置，具体请看宏定义GetMinecraftEnum().ArmorSlotType.*
    :return: bool 设置成功返回True
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(entity_id)
    return item_comp.SetEntityItem(pos_type, item_dict, slot_pos)


def get_item_custom_name(player_id, item_dict):
    """
    获取物品的自定义名称，与铁砧修改的名称一致

    :param player_id:
    :param item_dict: dict [物品信息字典]。如果是接口获取的item_dict，应该包含userData，即getUserData应该为True
    :return: str 自定义名称
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.GetCustomName(item_dict)


def set_item_custom_name(player_id, item_dict, name):
    """
    设置物品的自定义名称，与使用铁砧重命名一致

    :param player_id:
    :param item_dict: dict [物品信息字典]
    :param name: str 物品名称。支持unicode
    :return: bool 设置是否成功
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.SetCustomName(item_dict, name)


def get_item_user_data_in_server_event(event_name):
    """
    使物品相关 **服务端事件** 的[物品信息字典]参数带有userData。在mod初始化时调用即可

    :param event_name: str 引擎事件名
    :return: bool 是否成功
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(level_id)
    # 这样调用之后，PlayerEatFoodServerEvent事件的itemDict参数会带有userData字段
    return item_comp.GetUserDataInEvent(event_name)


def set_player_selected_slot(player_id, slot):
    """
    设置玩家当前选中快捷栏物品的index

    1.20 调整 由玩家分类移动到物品分类

    1.18 新增 设置玩家当前选中快捷栏物品的index

    :param player_id:
    :param slot: int 快捷栏物品的index，从0开始，最大为8
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.ChangeSelectSlot(slot)


def get_player_selected_slot(player_id):
    """
    获取玩家当前选中槽位

    :param player_id:
    :return: int 当前槽位，错误时返回-1
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.GetSelectSlotId()


def get_container_item(player_id, pos, slot_pos, dimension=-1, get_user_data=False):
    """
    获取容器物品

    容器的具体类型包括：箱子，陷阱箱，潜影盒，漏斗，木桶，投掷器，发射器

    此接口不支持末影箱。对应的末影箱接口请参考 **GetEnderChestItem**

    :param player_id:
    :param pos: tuple(int,int,int) 容器位置
    :param slot_pos: int 容器槽位
    :param dimension: int 方块所在维度，默认值为-1，传入非负值时不依赖player_id，CreateItem可传入level_id，否则CreateItem需传入player_id来获取玩家当前维度
    :param get_user_data: bool 是否获取userData，默认为False
    :return: dict [物品信息字典]，没有物品则返回None
    """
    if dimension > -1:
        item_comp = serverApi.GetEngineCompFactory().CreateItem(level_id)
        return item_comp.GetContainerItem(pos, slot_pos, dimension, get_user_data)

    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.GetContainerItem(pos, slot_pos, get_user_data)


def get_ender_chest_item(player_id, slot_pos, get_user_data=False):
    """
    获取末影箱物品

    :param player_id: str 玩家id
    :param slot_pos: int 容器槽位
    :param get_user_data: bool 是否获取userData，默认为False
    :return: dict [物品信息字典]，没有物品则返回None
    """
    item_comp = serverApi.GetEngineCompFactory().CreateItem(player_id)
    return item_comp.GetEnderChestItem(player_id, slot_pos, get_user_data)


def get_recipe_result(recipe_id):
    """
    根据配方id获取配方结果。仅支持合成配方

    :param recipe_id: str 配方id,对应配方json文件中的identifier字段
    :return: list [dict]
        itemName: str 物品名称id
        auxValue: int 物品附加值
        num: int 物品数目
    """
    recipe_comp = serverApi.GetEngineCompFactory().CreateRecipe(level_id)
    return recipe_comp.GetRecipeResult(recipe_id)


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
    recipe_comp = serverApi.GetEngineCompFactory().CreateRecipe(level_id)
    return recipe_comp.GetRecipesByResult(result_identifier, tag, aux)
