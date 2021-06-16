# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def add_chunk_pos_white_list(dimension, pos):
    """
    为某区块加载完成、准备卸载事件添加监听
    
    方块坐标(x, y, z)所在的区块坐标为(math.floor(x / 16), math.floor(z / 16))
    
    1.19 新增 为客户端区块加载完成、准备卸载事件添加监听
    
    :param dimension: int 区块所在维度
    :param pos: tuple(int,int) 指定区块的坐标
    :return: bool 是否添加成功
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.AddChunkPosWhiteList(dimension, pos)


def remove_chunk_pos_white_list(dimension, pos):
    """
    移除对某区块加载完成、准备卸载事件的监听

    方块坐标(x, y, z)所在的区块坐标为(math.floor(x / 16), math.floor(z / 16))

    1.19 新增 为客户端区块加载完成、准备卸载事件移除监听

    :param dimension: int 区块所在维度
    :param pos: tuple(int,int) 指定区块的坐标
    :return: bool 是否移除成功
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.RemoveChunkPosWhiteList(dimension, pos)


def get_chunk_pos_from_block_pos(block_pos):
    """
    通过方块坐标获得该方块所在区块坐标

    当传入的blockPos类型不是tuple或者长度不为3时，返回值为None

    1.20 新增 服务端通过方块坐标获得该方块所在区块坐标

    :param block_pos: tuple(int,int,int) 方块的坐标
    :return: None或tuple(int,int) 该方块所在区块的坐标
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.GetChunkPosFromBlockPos(block_pos)


def check_chunk_state(dimension, pos):
    """
    判断指定位置的chunk是否加载完成

    1.19 新增 为客户端区块加载完成、准备卸载事件添加监听

    :param dimension: int 区块所在维度
    :param pos: tuple(int,int) 指定区块的坐标
    :return: bool 加载是否完成
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.CheckChunkState(dimension, pos)


def add_ticking_area(key, dimension, min_pos, max_pos):
    """
    设置区块的常加载

    * 该方式创建的常加载区域不会tick，即实体，方块实体，随机刻都不会进行更新。若需要区域被tick，请使用原版[tickingarea指令](https://minecraft-zh.gamepedia.com/%E5%91%BD%E4%BB%A4/tickingarea)。
    * 将当前未加载的区块设置为常加载区块时，不会从存档加载生物。但如果是当前已加载的区块，则玩家远离时区块后，区块内的实体会一直保持加载。
    * 常加载区块内可以使用api创建实体、放置方块、放置结构、修改方块实体数据。但由于区块加载的特性，需要将操作位置的四周外延80格的区域都设置为常加载，例如需要在(0,5,0)的位置生成生物/放置方块，需要将(-80,0,-80)到(80,0,80)的区域设置为常加载。

    :param key: str 常加载区域的名称，key必须唯一，若添加区域时key已存在将添加失败。
    :param dimension: int 区块所在的维度
    :param min_pos: tuple(int,int,int) 加载区域的最小坐标
    :param max_pos: tuple(int,int,int) 加载区域的最大坐标
    :return: bool 设置是否成功
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.SetAddArea(key, dimension, min_pos, max_pos)


def remove_ticking_area(key):
    """
    删除一个常加载区域

    :param key: str 常加载区域的名称
    :return: bool 删除是否成功
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.DeleteArea(key)


def clear_all_ticking_area():
    """
    删除所有常加载区域

    :return: int 删除的区域数目，错误时为None
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.DeleteAllArea()


def get_all_ticking_area():
    """
    获取所有常加载区域名称列表

    :return: list(str) 名称列表list
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.GetAllAreaKeys()


def get_chunk_min_pos(chunk_pos):
    """
    获取某区块最小点的坐标

    当传入的chunkPos类型不是tuple或者长度不为2时，返回值为None

    1.20 新增 获取某区块最小点的坐标

    :param chunk_pos: tuple(int,int) 指定区块的坐标
    :return: None或tuple(int,int,int) 该区块最小点的坐标
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.GetChunkMinPos(chunk_pos)


def get_chunk_max_pos(chunk_pos):
    """
    获取某区块最大点的坐标

    当传入的chunkPos类型不是tuple或者长度不为2时，返回值为None

    1.20 新增 获取某区块最大点的坐标

    :param chunk_pos: tuple(int,int) 指定区块的坐标
    :return: None或tuple(int,int,int) 该区块最大点的坐标
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.GetChunkMaxPos(chunk_pos)


def get_chunk_mob_num(dimension, chunk_pos):
    """
    获取某区块中的生物数量（不包括玩家，但包括盔甲架）

    :param dimension: int 区块所在维度
    :param chunk_pos: tuple(int,int) 指定区块的坐标
    :return: int 该区块中的生物数量，返回值为-1通常是由于该维度未加载、该区块未加载
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.GetChunkMobNum(dimension, chunk_pos)


def is_chunk_generated(dimension, chunk_pos):
    """
    获取某个区块是否生成过

    玩家探索过（以玩家为中心，模拟距离（在游戏的设置页面内）为半径内的区块），或者使用SetAddArea设置常加载区块附近的区块，都是生成过的区块。这些区块会保存到存档里，再次探索时会从存档读取，不会重新生成。

    1.20 新增 获取某个区块是否生成过。

    :param dimension: int 区块所在维度
    :param chunk_pos: tuple(int,int) 指定区块的坐标
    :return: bool 该区块是否生成过
    """
    chunk_source_comp = serverApi.GetEngineCompFactory().CreateChunkSource(level_id)
    return chunk_source_comp.IsChunkGenerated(dimension, chunk_pos)


def create_explosion(source_id, player_id, pos, radius, fire=False, breaks=False):
    """
    用于生成爆炸

    :param source_id: 爆炸伤害源的实体id
    :param player_id: 爆炸创造的实体id
    :param pos: tuple(float,float,float) 爆炸位置
    :param radius: int 爆炸威力，具体含义可参考[wiki](https://minecraft-zh.gamepedia.com/%E7%88%86%E7%82%B8)对爆炸的解释
    :param fire: bool 是否带火
    :param breaks: bool 是否破坏方块
    :return: bool 设置结果
    """
    explosion_comp = serverApi.GetEngineCompFactory().CreateExplosion(level_id)
    return explosion_comp.CreateExplosion(pos, radius, fire, breaks, source_id, player_id)


def add_netease_feature_white_list(structure_name):
    """
    添加结构对PlaceNeteaseStructureFeatureEvent事件的脚本层监听

    :param structure_name: str 结构的identifier，格式为folderName:structureName
    :return: bool 是否增加成功
    """
    feature_comp = serverApi.GetEngineCompFactory().CreateFeature(level_id)
    return feature_comp.AddNeteaseFeatureWhiteList(structure_name)


def remove_netease_feature_white_list(structure_name):
    """
    移除structureName对PlaceNeteaseStructureFeatureEvent事件的脚本层监听

    :param structure_name: str 结构的identifier，格式为folderName:structureName
    :return: bool 是否移除成功
    """
    feature_comp = serverApi.GetEngineCompFactory().CreateFeature(level_id)
    return feature_comp.AddNeteaseFeatureWhiteList(structure_name)


def clear_all_netease_feature_white_list():
    """
    清空所有已添加Netease Structure Feature对PlaceNeteaseStructureFeatureEvent事件的脚本层监听

    :return: bool 是否清空成功
    """
    feature_comp = serverApi.GetEngineCompFactory().CreateFeature(level_id)
    return feature_comp.ClearAllNeteaseFeatureWhiteList()


def locate_structure_feature(feature_type, dimension, pos):
    """
    与[/locate指令](https://minecraft-zh.gamepedia.com/%E5%91%BD%E4%BB%A4/locate)相似，用于定位原版的部分结构，如海底神殿、末地城等。

    定位失败通常是由于该维度不存在、该维度未加载、该维度中不存在该结构、该结构距离传入位置过远等

    该接口返回值为对应结构所在区块的坐标，与结构实际生成位置可能相距一定距离

    1.19 新增 定位原版的部分结构

    :param feature_type: int 原版的结构类型，[StructureFeatureType]枚举
    :param dimension: int 结构所在维度，要求该维度已加载
    :param pos: tuple(int,int,int) 以该位置为中心来查找最近的结构
    :return: tuple(float,float)或None 最近的结构所在区块位置(x坐标,z坐标)，y坐标不定，若定位失败则返回None
    """
    feature_comp = serverApi.GetEngineCompFactory().CreateFeature(level_id)
    return feature_comp.LocateStructureFeature(feature_type, dimension, pos)


def locate_netease_feature(feature_name, dimension, pos):
    """
    与[/locate指令](https://minecraft-zh.gamepedia.com/%E5%91%BD%E4%BB%A4/locate)相似，用于定位由[网易自定义特征]放置的结构

    **通过[PlaceStructure接口]、/placestructure指令或结构方块手动放置的结构无法被定位到。如有需要，建议开发者自行记录这些手动放置的结构位置**

    * 定位失败通常是由于该维度不存在、该维度未加载、该维度中不存在该结构、该结构距离传入位置过远（以该位置为中心，半径100个区块内无法找到）
    * 若在feature rules中"conditions"内的"minecraft:biome_filter"中填写了判断维度以外的过滤规则，将有概率无法定位到距离最近的特征。建议开发者在"distribution"的"iterations"中使用query.is_biome代替
    * 定位原理是根据放置条件寻找可能放置结构的位置，因此有可能会定位到在PlaceNeteaseStructureFeatureEvent事件中被取消生成的结构。开发者应注意甄别，尽量避免对可能在PlaceNeteaseStructureFeatureEvent事件中被取消放置的结构调用定位函数

    :param feature_name: str 结构名称，形式为namespace:featureName，如test:pumpkins
    :param dimension: int 结构所在维度，要求该维度已加载
    :param pos: tuple(int,int,int) 以该位置为中心来查找最近的结构
    :return: tuple(float,float,float)或None 最近的结构位置，定位失败则返回None
    """
    feature_comp = serverApi.GetEngineCompFactory().CreateFeature(level_id)
    return feature_comp.LocateNeteaseFeature(feature_name, dimension, pos)


def place_structure(player_id, pos, structure_name, dimension=-1):
    """
    放置结构

    放置时需要确保所放置的区块都已加载，否则会放置失败或者部分缺失

    该接口是同步执行的，请勿在一帧内放置大量结构，会造成游戏卡顿

    1.20 调整 增加参数dimensionId，默认为-1，传入非负值时不依赖playerId，可在对应维度的常加载区块放置结构

    :param player_id: str或None 放置该结构的玩家id/None
    :param pos: tuple(float,float,float) 放置结构的位置
    :param structure_name: str 结构名称
    :param dimension: int 希望放置结构的维度，默认为-1，传入非负值时不依赖playerId，playerId可传入None，可在对应维度的常加载区块放置结构
    :return: bool 是否放置成功，True为放置成功，False为放置失败
    """
    if dimension > -1:
        game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
        return game_comp.PlaceStructure(None, pos, structure_name, dimension)
    game_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return game_comp.PlaceStructure(player_id, pos, structure_name)


def add_timer(delay, func, *args, **kwargs):
    """
    添加服务端触发的定时器，非重复

    :param delay: float 延迟时间，单位秒
    :param func: function 定时器触发函数
    :param args: any 变长参数，可以不设置
    :param kwargs: any 字典变长参数，可以不设置
    :return: CallLater 返回单次触发的定时器实例
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.AddTimer(delay, func, *args, **kwargs)


def add_repeated_timer(delay, func, *args, **kwargs):
    """
    添加服务端触发的定时器，重复执行

    :param delay: float 延迟时间，单位秒
    :param func: function 定时器触发函数
    :param args: any 变长参数，可以不设置
    :param kwargs: any 字典变长参数，可以不设置
    :return: CallLater 返回触发的定时器实例
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.AddRepeatedTimer(delay, func, *args, **kwargs)


def cancel_timer(timer):
    """
    取消定时器

    :param timer: CallLater AddTimer和AddRepeatedTimer时返回的定时器实例
    :return:
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    game_comp.CancelTimer(timer)


def can_see_entity(from_id, target_id, **kwargs):
    """
    判断起始对象是否可看见目标对象,基于对象的Head位置判断

    :param from_id: str 起始对象ID
    :param target_id: str 目标对象ID
    :param kwargs: dict 相关参数
        viewRange: float 视野距离,默认值8.0
        onlySolid: bool 只判断固体方块遮挡,默认True; False则液体方块也会遮挡
        angleX: float 视野X轴角度,默认值180.0度
        angleY: float 视野Y轴角度,默认值180.0度
    :return: bool 是否可见
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(from_id)
    return game_comp.CanSee(from_id, target_id, **kwargs)


def check_name_valid(name):
    """
    检查昵称是否合法，即不包含敏感词

    :param name: str 昵称
    :return: bool True:昵称合法 False:昵称非法
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.CheckNameValid(name)


def check_words_valid(words):
    """
    检查语句是否合法，即不包含敏感词

    :param words: str 语句
    :return: True:语句合法 False:语句非法
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.CheckWordsValid(words)


def set_disable_vine_block_spread(disable=True):
    """
    设置是否允许藤曼蔓延生长

    :param disable: bool True:禁用 False:非禁用
    :return:
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    game_comp.DisableBineBlockSpread(disable)


def set_disable_liquid_flow(disable=True):
    """
    禁止/允许地图中的流体流动；备注：在禁止流体流动后方式的水/岩浆，重新允许流动之后立刻不会触发向四周流动的逻辑，直到再次触发流动判定为止（如周围的方块发生了变化）

    1.18 新增 禁止/允许地图中的流体流动

    :param disable: bool True为允许流体流动 False为禁止流体流动
    :return: success True为设置成功，False为设置失败
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.ForbidLiquidFlow(disable)


def set_disable_lightning_ignites_block(disable=True):
    """
    禁止/允许闪电点燃方块

    :param disable: bool True为允许闪电点燃方块 False为禁止闪电点燃方块
    :return: bool success True为设置成功，False为设置失败
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetCanBlockSetOnFireByLightning(not disable)


def set_disable_lightning_ignites_actor(disable=True):
    """
    禁止/允许闪电点燃实体

    :param disable: bool True为允许闪电点燃实体 False为禁止闪电点燃实体
    :return: bool success True为设置成功，False为设置失败
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetCanActorSetOnFireByLightning(not disable)


def set_disable_containers(disable=True):
    """
    设置是否屏蔽容器交互(不包括背包)，不包括纯客户端逻辑控制的容器：纱布机，切石机，制图台等

    :param disable: bool 是否屏蔽容器交互
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetDisableContainers(disable)


def set_disable_drop_item(disable=True):
    """
    设置禁止丢弃物品
    
    * 开启开关后，玩家死亡会所有物品消失；如需保证物品不掉落，可以配合/gamerule keepInventory true 使用
    * 创造模式下物品依然能丢弃。
    
    :param disable: bool 是否禁止丢弃物品
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetDisableDropItem(disable)


def set_disable_gravity_in_liquid(disable=True):
    """
    是否屏蔽所有实体在液体（水、岩浆）中的重力

    设置屏蔽实体在液体中的重力后，实体将不能上浮也不能下潜。
    **对玩家而言，当水/岩浆淹没腰部及以上时（约在水面/岩浆表面0.7格及以下），将无法上岸。**

    :param disable: bool True:屏蔽 False:取消屏蔽
    :return: bool 是否设置成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetDisableGravityInLiquid(disable)


def set_disable_hunger(disable=True):
    """
    设置是否屏蔽饥饿度

    如需隐藏饥饿度请使用extraClientApi的HideHungerGui

    :param disable: bool 是否屏蔽饥饿度
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetDisableHunger(disable)


def get_entities_around(entity_id, radius, filters=None):
    """
    获取区域内的entity列表

    :param entity_id: str 某个entityId
    :param radius: int 正方体区域半径
    :param filters: dict 过滤设置字典，可以不设置
    :return: list(str) 返回entityId的list
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(entity_id)
    return game_comp.GetEntitiesAround(entity_id, radius, filters)


def get_entities_around_by_type(entity_id, radius, entity_type):
    """
    获取区域内的某类型的entity列表

    :param entity_id: str 区域中心的entityId,如某个玩家的entityid
    :param radius: int 区域半径
    :param entity_type: int 实体类型参见枚举EntityType
    :return: list(str) 返回entityId的list
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetEntitiesAroundByType(entity_id, radius, entity_type)


def get_entities_in_square_area(entity_id, start_pos, end_pos, dimension=-1):
    """
    获取区域内的entity列表

    1.20 调整 新增dimensionId参数，默认为-1，传入非负值时不依赖entityId，可获取对应维度的常加载区块内的实体列表

    :param entity_id: str或None 某个entityId/None
    :param start_pos: tuple(int,int,int) 初始位置
    :param end_pos: tuple(int,int,int) 结束位置
    :param dimension: int 区域所在维度，默认值为-1，传入非负值时不依赖entityId，entityId可传入None，可获取对应维度的常加载区块内的实体列表
    :return: list(str) 返回entityId的list
    """
    if dimension > -1:
        game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
        return game_comp.GetEntitiesInSquareArea(None, start_pos, end_pos, dimension)
    game_comp = serverApi.GetEngineCompFactory().CreateGame(entity_id)
    return game_comp.GetEntitiesInSquareArea(entity_id, start_pos, end_pos)


def get_entity_identifier(entity_id):
    """
    获取实体entity的identifier标识名称

    :param entity_id: str 要获取的目标的entityId
    :return: str identifier标识符,例如:"minecraft:item"
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetEntityIdentifier(entity_id)


def get_item_entity_item_identifier(entity_id):
    """
    获取ItemEntity的Item的identifier标识名称

    :param entity_id: str 要获取的目标的entityId
    :return: str identifier标识符,例如:"minecraft:apple"
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetItemEntityItemIdentifier(entity_id)


def get_game_difficulty():
    """
    获取游戏难度

    :return: int GetMinecraftEnum().GameDiffculty.*:Peaceful，Easy，Normal，Hard分别为0~3
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetGameDiffculty()


def is_lock_difficulty():
    """
    获取当前世界的游戏难度是否被锁定

    :return: bool isLock True为已锁定，False为未锁定
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.IsLockDifficulty()


def set_game_difficulty_lock(lock=True):
    """
    锁定当前世界游戏难度（仅本次游戏有效），锁定后任何玩家在游戏内都无法通过指令或暂停菜单修改游戏难度

    :param lock: bool True:锁定 False:解锁
    :return: bool result是否操作成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.LockDifficulty(lock)


def set_game_difficulty(difficulty):
    """
    设置游戏难度

    若已经锁定了游戏难度，除非调用解锁游戏难度，否则将无法成功修改游戏难度

    1.18 新增 设置游戏难度

    :param difficulty: int GetMinecraftEnum().GameDiffculty.*:Peaceful，Easy，Normal，Hard分别为0~3
    :return: bool 是否设置成功，True为成功，False为失败
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetGameDifficulty(difficulty)


def get_game_rules_info_server():
    """
    获取游戏规则

    :return: dict 游戏规则字典
        create_info: dict
            'bonus_item': bool,
            'init_with_map': bool,
            'generator_type': int,
            'seed': str
        option_info: dict
            'pvp': bool,
            'show_coordinates': bool,
            'fire_spreads': bool,
            'tnt_explodes': bool,
            'mob_loot': bool,
            'natural_regeneration': bool,
            'tile_drops': bool,
            'experimental_gameplay': bool
        cheat_info: dict
            'enable': bool,
            'always_day': bool,
            'mob_griefing': bool,
            'keep_inventory': bool,
            'weather_cycle': bool,
            'mob_spawn': bool,
            'entities_drop_loot': bool,
            'daylight_cycle': bool,
            'command_blocks_enabled': bool,
            'random_tick_speed': int
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetGameRulesInfoServer()


def set_game_rules_info_server(game_rule_dict):
    """
    设置游戏规则。所有参数均可选

    其中游戏规则字典中每一项都为可选参数,但是设置option_info或者cheat_info其中一项子项后，必须加上option_info或者cheat_info

    :param game_rule_dict: dict 游戏规则字典
        'option_info':
            'pvp': bool, #玩家伤害
            'show_coordinates': bool, #显示坐标
            'fire_spreads': bool, #火焰蔓延
            'tnt_explodes': bool, #tnt爆炸
            'mob_loot': bool, #生物战利品
            'natural_regeneration': bool, #自然生命恢复
            'tile_drops': bool, #方块掉落
            'immediate_respawn':bool #作弊开启
        'cheat_info':
            'enable': bool, #是否开启作弊
            'always_day': bool, #终为白日
            'mob_griefing': bool, #生物破坏方块
            'keep_inventory': bool, #保留物品栏
            'weather_cycle': bool, #天气更替
            'mob_spawn': bool, #生物生成
            'entities_drop_loot': bool, #实体掉落
            'daylight_cycle': bool, #开启昼夜交替
            'command_blocks_enabled': bool, #启用方块命令
            'random_tick_speed': int,#随机方块tick速度
    :return: bool 是否设置成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetGameRulesInfoServer(game_rule_dict)


def get_game_type():
    """
    获取游戏类型

    :return: int GetMinecraftEnum().GameType.*:Survival，Creative，Adventure分别为0~2
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetGameType()


def set_default_game_type(game_type):
    """
    设置默认游戏模式

    :param game_type: int GetMinecraftEnum().GameType.*:Survival，Creative，Adventure分别为0~2
    :return: bool 是否设置成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetDefaultGameType(game_type)


def get_player_game_type(player_id):
    """
    获取指定玩家的游戏模式

    :param player_id: str 玩家id
    :return: int GameType类型
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetPlayerGameType(player_id)


def get_level_gravity():
    """
    获取重力因子

    :return: float 重力因子
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetLevelGravity()


def set_level_gravity(data):
    """
    设置重力因子

    生物可单独设置重力因子，当生物的重力因子非0时则该生物单独有自己的重力因子，具体参见实体重力组件

    :param data: float 重力因子
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.GetLevelGravity(data)


def kill_entity(entity_id):
    """
    杀死某个Entity

    :param entity_id: str 要杀死的目标的entityId
    :return: bool 是否杀死成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.KillEntity(entity_id)


def find_item_by_identifier(item_name):
    """
    判定指定identifier的物品是否存在

    1.18 新增 判定指定identifier的物品是否存在

    :param item_name: 判定指定identifier的物品是否存在
    :return: bool exist True为对应的物品存在，False为对应物品不存在
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.LookupItemByName(item_name)


def open_city_protect():
    """
    开启城市保护，包括禁止破坏方块，禁止对方块使用物品，禁止怪物攻击玩家，禁止玩家之间互相攻击，禁止日夜切换，禁止天气变化，禁止怪物群落刷新

    :return: bool success True为设置成功，False为设置失败
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.OpenCityProtect()


def pick_up_item_entity(player_id, item_entity_id):
    """
    某个Player拾取物品ItemEntity

    :param player_id: str 拾取者的playerEntityId
    :param item_entity_id: str 要拾取的物品itemEntityId
    :return: bool 是否拾取成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.PickUpItemEntity(player_id, item_entity_id)


def set_hurt_cd(cd_time):
    """
    设置伤害CD

    :param cd_time: int 单位帧数
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.SetHurtCD(cd_time)


def set_notify_msg(player_id, msg, color=None):
    """
    设置消息通知

    :param player_id:
    :param msg: str 消息内容
    :param color: str 使用GenerateColor接口获取的颜色，默认为白色
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(player_id)
    if color:
        return game_comp.SetNotifyMsg(msg, color)
    return game_comp.SetNotifyMsg(msg)


def set_popup_notice(player_id, message, subtitle):
    """
    在所有玩家物品栏上方弹出popup类型通知，位置位于tip类型消息下方

    :param player_id:
    :param message: str 消息内容,可以在消息前增加extraServerApi.GenerateColor("RED")字符来设置颜色，具体参考样例
    :param subtitle: str 消息子标题内容,效果同message，也可设置颜色，位置位于message上方
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(player_id)
    return game_comp.SetPopupNotice(message, subtitle)


def set_tip_message(player_id, message):
    """
    在所有玩家物品栏上方弹出tip类型通知，位置位于popup类型通知上方

    :param player_id:
    :param message: str 消息内容,可以在消息前增加extraServerApi.GenerateColor("RED")字符来设置颜色，具体参考样例
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(player_id)
    return game_comp.SetTipMessage(message)


def set_one_popup_notice(player_id, message, subtitle):
    """
    在具体某个玩家的物品栏上方弹出popup类型通知，位置位于tip类型消息下方，此功能更建议客户端使用game组件的对应接口SetPopupNotice

    :param player_id: str 具体玩家Id
    :param message: str 消息内容,可以在消息前增加extraServerApi.GenerateColor("RED")字符来设置颜色，具体参考样例
    :param subtitle: str 消息子标题内容,效果同message，也可设置颜色，位置位于message上方
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(player_id)
    return game_comp.SetOnePopupNotice(player_id, message, subtitle)


def set_one_tip_message(player_id, message):
    """
    在具体某个玩家的物品栏上方弹出tip类型通知，位置位于popup类型通知上方，此功能更建议在客户端使用game组件的对应接口SetTipMessage

    :param player_id: str 具体玩家Id
    :param message: str 消息内容,可以在消息前增加extraServerApi.GenerateColor("RED")字符来设置颜色，具体参考样例
    :return: bool 设置是否成功
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(player_id)
    return game_comp.SetOneTipMessage(player_id, message)


def upgrade_map_dimension_version(dimension, version):
    """
    提升指定地图维度的版本号，版本号不符的维度，地图存档信息将被废弃

    1.19 新增 提升指定地图维度的版本号，版本号不符的维度，地图存档信息将被废弃

    :param dimension: int 维度的数字ID，0代表主世界
    :param version: int 维度地图的版本号，取值范围为1-999
    :return: bool success True为设置成功，False为设置失败
    """
    game_comp = serverApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.UpgradeMapDimensionVersion(dimension, version)


def set_time(time):
    """
    设置当前世界时间

    :param time: int 时间，单位帧数，游戏一天24000帧，可以通过设置时间来改变天亮和天黑以及其他
    :return: bool 设置是否成功
    """
    time_comp = serverApi.GetEngineCompFactory().CreateTime(level_id)
    return time_comp.SetTime(time)


def get_time():
    """
    获取当前世界时间

    :return: int 当前时间，帧数
    """
    time_comp = serverApi.GetEngineCompFactory().CreateTime(level_id)
    return time_comp.GetTime()


def is_raining():
    """
    获取是否下雨

    :return: bool 是否下雨
    """
    weather_comp = serverApi.GetEngineCompFactory().CreateWeather(level_id)
    return weather_comp.IsRaining()


def set_raining(level, time):
    """
    设置是否下雨

    :param level: float 下雨强度
    :param time: int 下雨时间单位为帧
    :return: bool 设置是否成功
    """
    weather_comp = serverApi.GetEngineCompFactory().CreateWeather(level_id)
    return weather_comp.SetRaining(level, time)


def is_thunder():
    """
    获取是否打雷

    :return: bool 是否打雷
    """
    weather_comp = serverApi.GetEngineCompFactory().CreateWeather(level_id)
    return weather_comp.IsThunder()


def set_thunder(level, time):
    """
    设置是否打雷

    :param level: float 打雷强度
    :param time: int 打雷时间单位为帧
    :return: bool 设置是否成功
    """
    weather_comp = serverApi.GetEngineCompFactory().CreateWeather(level_id)
    return weather_comp.SetThunder(level, time)
