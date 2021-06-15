# -*- coding: utf-8 -*-

import warnings

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def register_block_patterns(pattern, defines, result_actor_name):
    """
    注册特殊方块组合

    :param pattern: list(str) 方块组合位置
    :param defines: dict 方块组合类型
    :param result_actor_name: str 合成结果
    :return: bool 设置结果
    """
    block_comp = serverApi.GetEngineCompFactory().CreateBlock(level_id)
    return block_comp.RegisterBlockPatterns(pattern, defines, result_actor_name)


def create_micro_block_res_str(identifier, start, end, color_map=None, is_merge=False, icon=''):
    """
    生成微缩方块资源Json字符串

    https://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91beta/03-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/10-%E5%BE%AE%E7%BC%A9%E6%96%B9%E5%9D%97.html#%E5%BE%AE%E7%BC%A9%E6%96%B9%E5%9D%97

    TODO 是否需要加上写入文件操作?

    :param identifier: str 微缩方块唯一标识
    :param start: tuple(int,int,int) 微缩起始坐标
    :param end: tuple(int,int,int) 微缩结束坐标
    :param color_map: dict 默认为None，微缩方块颜色对应表
    :param is_merge: bool 默认为False，是否合并同类型方块
    :param icon: str 默认为空字符串，微缩方块图标，需要定义在 terrain_texture.json 中
    :return: str 生成的微缩方块的资源字符串
    """
    block_comp = serverApi.GetEngineCompFactory().CreateBlock(level_id)
    return block_comp.CreateMicroBlockResStr(identifier, start, end, color_map, is_merge, icon)


def get_block_entity_data(dimension, pos):
    """
    用于获取可操作某个自定义方块实体数据的对象，操作方式与dict类似

    * GetBlockEntityData返回None通常是由于该方块所在区块未加载、正在退出游戏、该方块不是自定义方块或该自定义方块的json中并未配置netease:block_entity组件。
    * 在对GetBlockEntityData返回对象进行操作前，请先判断它是否为空，否则会导致'NoneType' object has no attribute '__getitem__'错误。
    * 支持python基本数据类型(int/float/string/bool/dict/list)，不支持tuple且dict的key必须为字符串
    * 存储list时，list内各项的数据类型应相同，否则将存储失败。如[True, False]可成功存储，[True, 1, 0.5]会存储失败
    * 虽然返回的对象操作与dict相似，但并不支持嵌套存储，只允许形如blockEntityData['key'] = value的直接赋值。如blockEntityData["value5"] ["v1"] = 9或blockEntityData["value6"].append(True)的操作将无法成功存储数据。
    * 存储整数时，若数值范围超过int所能表示的最大范围，将无法成功存储。建议将此类数值转为字符串进行存储。

    :param dimension: int 维度
    :param pos: tuple(int,int,int) 方块所在位置
    :return: BlockEntityData或None 可操作该方块实体内数据的对象
    """
    block_entity_comp = serverApi.GetEngineCompFactory().CreateBlockEntityData(level_id)
    return block_entity_comp.GetBlockEntityData(dimension, pos)


def check_block_to_pos(from_pos, to_pos, dimension=0):
    """
    判断位置之间是否有方块

    1.23 调整 废弃player_id参数

    1.20 调整 新增dimensionId参数，默认为-1，传入非负值时不依赖playerId，可判断对应维度的常加载区块内位置之间是否有方块

    :param from_pos: tuple(float,float,float) 起始位置
    :param to_pos: tuple(float,float,float) 终止位置
    :param dimension: int 位置所在维度，默认值为0，传入非负值时不依赖playerId
    :return: int result -1：获取失败  0：没有方块  1：有方块
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.CheckBlockToPos(from_pos, to_pos, dimension)


def clear_block_tile_entity_custom_data(player_id, pos):
    """
    清空指定位置的特殊方块（箱子、头颅、熔炉、花盆等）绑定的TileEntity内存储的自定义数据

    该接口使用创建组件时的playerId来定位具体维度，且仅可获取玩家附近的方块，若方块位置离玩家太远，可能无法获取到正确的返回信息。

    1.19 新增 清空指定位置的特殊方块（箱子、头颅、熔炉、花盆等）绑定的TileEntity内存储的自定义数据。

    :param player_id:
    :param pos: tuple(int,int,int) 绑定TileEntity的特殊方块的位置坐标
    :return: bool 清空结果，假如对应位置的block不存在或者没有绑定的TileEntity，就会失败
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.CleanBlockTileEntityCustomData(pos)


def get_bed_color(player_id, pos):
    """
    获取床（方块）的颜色，仅Apollo网络服可用

    1.19.0 新增 获取床（方块）的颜色

    :param player_id:
    :param pos: tuple(int,int,int) 床的位置坐标（床占地两格，任意一个格子都可以）
    :return: int [ItemColor]枚举 当输入的坐标位置的方块不是床的时候，返回-1
    """
    warnings.warn("1.20 目前GetBedColor仅Apollo网络服可用", DeprecationWarning)

    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.GetBedColor(pos)


def set_bed_color(player_id, pos, color):
    """
    设置床（方块）的颜色，仅Apollo网络服可用

    1.19 新增 设置床（方块）的颜色

    :param player_id:
    :param pos: tuple(int,int,int) 床的位置坐标（床占地两格，任意一个格子都可以）
    :param color: int [ItemColor]枚举
    :return: bool 是否设置成功
    """
    warnings.warn("1.20 目前SetBedColor仅Apollo网络服可用", DeprecationWarning)

    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.SetBedColor(pos, color)


def get_block_entity_info(dimension, pos):
    """
    用于获取方块（包括自定义方块）的数据

    适用于：[方块实体]
    https://minecraft-zh.gamepedia.com/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93

    * **注意：通过此方法获取的数据只读不可写**
    * **随着版本更迭，方块中包含的数据结构可能被微软团队调整，并且不会公告，使用该接口的开发者需注意版本更新时做好测试和兼容。**
    * **数据编码为UTF-8**
    * **特殊情况：末影箱的物品信息不能通过该接口获取**

    1.18 新增 获取方块（包括自定义方块）的数据

    :param dimension: int 维度
    :param pos: tuple(int,int,int) 方块所在位置
    :return: dict或None 方块实体内数据的对象
    """
    block_entity_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_entity_comp.GetBlockEntityData(dimension, pos)


def get_block_light_level(pos, dimension=0):
    """
    获取方块位置的光照等级

    1.23 调整 废弃player_id参数

    1.20 调整 新增dimensionId参数，默认为-1，传入非负值时不依赖playerId，可获取对应维度的常加载区块内光照等级

    :param pos: tuple(int,int,int) 方块位置
    :param dimension: int 方块所在维度，默认值为0，传入非负值时不依赖playerId
    :return: int 光照等级
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.GetBlockLightLevel(pos, dimension)


def get_block(pos, dimension=0):
    """
    获取某一位置的block

    已经加载的地形才能获取方块信息，支持获取对应维度的常加载区块内方块信息

    对于有多种状态的方块，aux计算比较复杂，推荐使用GetBlockStates获取方块状态字典

    1.23 调整 废弃player_id参数

    1.20 调整 新增dimensionId参数，默认为-1，传入非负值时不依赖playerId，可在对应维度的常加载区块获取方块

    :param pos: tuple(int,int,int) 方块位置
    :param dimension: int 方块所在维度，默认值为0，传入非负值时不依赖playerId
    :return: dict 方块信息字典
        name: str 必须设置，方块identifier，包含命名空间及名称，如minecraft:air
        aux: int 方块附加值，可缺省，默认为0
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.GetBlockNew(pos, dimension)


def set_block(pos, block_dict, dimension=0, old_block_handling=0):
    """
    设置某一位置的方块

    已经加载的地形才能设置方块，支持在对应维度的常加载区块内设置方块

    若使用SetBlockNew接口替换含方块实体的方块，除自定义方块实体外，当替换前后方块实体类型相同时，其方块实体内数据不会发生改变。
    例如在箱子中放置了物品，使用SetBlockNew接口将箱子方块替换为箱子方块后，新的箱子中依然保留旧箱子内的物品。
    要避免这种情况，中间添加一次不同方块实体类型（或不含方块实体）的方块替换即可。比如先将箱子替换为空气，再将空气替换为箱子。

    对于有多种状态的方块，aux计算方式比较复杂，推荐先设置完方块后再使用SetBlockStates设置方块状态字典

    1.23 调整 废弃player_id参数

    1.20 调整 增加参数dimensionId，默认为-1，传入非负值时不依赖playerId，可在对应维度的常加载区块设置方块

    1.18 调整 增加参数oldBlockHandling，默认为替换replace

    :param pos: tuple(int,int,int) 方块位置
    :param block_dict: dict 方块信息字典
        name: str 必须设置，方块identifier，包含命名空间及名称，如minecraft:air
        aux: int 方块附加值，可缺省，默认为0
    :param dimension: int 方块所在维度，默认值为0，传入非负值时不依赖playerId
    :param old_block_handling: int 0：替换，1：销毁，2：保留，默认为0
    :return: bool 设置结果
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.SetBlockNew(pos, block_dict, old_block_handling, dimension)


def get_block_tile_entity_custom_data(player_id, pos, key):
    """
    读取指定位置的特殊方块（箱子、头颅、熔炉、花盆等）绑定的TileEntity内存储的自定义数据

    该接口使用创建组件时的playerId来定位具体维度，且仅可获取玩家附近的方块，若方块位置离玩家太远，可能无法获取到正确的返回信息。

    1.19 新增 读取指定位置的特殊方块（箱子、头颅、熔炉、花盆等）绑定的TileEntity内存储的自定义数据

    :param player_id:
    :param pos: tuple(int,int,int) 绑定TileEntity的特殊方块的位置坐标
    :param key: str 自定义key
    :return: any 设定的value值，假如对应的数据不存在，则会返回None
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.GetBlockTileEntityCustomData(pos, key)


def get_block_tile_entity_whole_custom_data(player_id, pos):
    """
    读取指定位置的特殊方块（箱子、头颅、熔炉、花盆等）绑定的TileEntity内存储的自定义数据字典

    该接口使用创建组件时的playerId来定位具体维度，且仅可获取玩家附近的方块，若方块位置离玩家太远，可能无法获取到正确的返回信息

    1.19 新增 读取指定位置的特殊方块（箱子、头颅、熔炉、花盆等）绑定的TileEntity内存储的自定义数据字典

    :param player_id:
    :param pos: tuple(int,int,int) 绑定TileEntity的特殊方块的位置坐标
    :return: dict或None TileEntity自定义存储数据字典，假如没有任何额外存储数据，那么返回None或者空字典
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.GetBlockTileEntityWholeCustomData(pos)


def set_block_tile_entity_custom_data(player_id, pos, key, value):
    """
    设置指定位置的特殊方块（箱子、头颅、熔炉、花盆等）绑定的TileEntity内存储的自定义数据

    该接口使用创建组件时的playerId来定位具体维度，且仅可获取玩家附近的方块，若方块位置离玩家太远，可能无法获取到正确的返回信息

    1.19 新增 设置指定位置的特殊方块（箱子、头颅、熔炉、花盆等）绑定的TileEntity内存储的自定义数据

    :param player_id:
    :param pos: tuple(int,int,int) 绑定TileEntity的特殊方块的位置坐标
    :param key: str 自定义key
    :param value: any 支持python基本数据类型，tuple不支持
    :return: bool 设置结果，假如对应位置的block不存在或者没有绑定的TileEntity，就会设置失败
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.SetBlockTileEntityCustomData(pos, key, value)


def get_chest_paired_position(player_id, pos):
    """
    获取与箱子A合并成一个大箱子的箱子B的坐标

    该接口使用创建组件时的playerId来定位具体维度，且仅可获取玩家附近的方块，若方块位置离玩家太远，可能无法获取到正确的返回信息。

    1.19 新增 获取与箱子A合并成一个大箱子的箱子B的坐标

    :param player_id:
    :param pos: tuple(int,int,int) 箱子A的位置坐标
    :return: tuple(int,int,int)或None 箱子B的位置坐标，假如输入的箱子A坐标上的方块不是箱子类方块或者没有和其他箱子方块组合成一个大箱子，就会返回None
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.GetChestPairedPosition(pos)


def get_sign_block_text(player_id, pos):
    """
    获取告示牌（方块）的文本内容

    1.19.0 新增 获取告示牌（方块）的文本内容

    :param player_id:
    :param pos: tuple(int,int,int) 告示牌的位置坐标
    :return: str 告示牌上的文本内容
        当输入的坐标位置的方块不是告示牌的时候，返回None
    """
    warnings.warn("1.20 目前GetSignBlockText仅Apollo网络服可用", DeprecationWarning)
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.GetSignBlockText(pos)


def set_sign_block_text(player_id, pos, text):
    """
    设置告示牌（方块）的文本内容，仅Apollo网络服可用

    1.19 新增 设置告示牌（方块）的文本内容

    :param player_id:
    :param pos: tuple(int,int,int) 告示牌的位置坐标
    :param text: str 想要设置的文本内容
    :return: bool 是否设置成功
    """
    warnings.warn("1.20 目前SetSignBlockText仅Apollo网络服可用", DeprecationWarning)

    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.SetSignBlockText(pos, text)


def get_destroy_total_time(block_name, item_name=None):
    """
    获取使用物品破坏方块需要的时间

    1.22 新增 获取使用物品破坏方块需要的时间

    :param block_name: str 方块标识符，格式[namespace:name:auxvalue]，auxvalue默认为0
    :param item_name: str 物品标识符，格式[namespace:name:auxvalue]，auxvalue默认为0，默认为None（不使用物品）
    :return: int 高度
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.GetDestroyTotalTime(block_name, item_name)


def get_top_block_height(pos, dimension=0):
    """
    获取某一位置最高的非空气方块的高度

    1.20 新增 获取某一位置最高的非空气方块的高度

    :param pos: tuple(int,int) x轴与z轴位置
    :param dimension: int 维度id，默认为0，可在获取常加载区块内最高非空气方块高度
    :return: int 高度
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.GetTopBlockHeight(pos, dimension)


def change_listen_block_remove_event(identifier, listen):
    """
    是否监听方块BlockRemoveServerEvent事件，可以动态修改json组件netease:listen_block_remove的值

    :param identifier: str 方块identifier，如minecraft:wheat
    :param listen: bool 是否监听
    :return: bool 是否设置成功
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.ListenOnBlockRemoveEvent(identifier, listen)


def can_place_block(identifier, block_pos, facing, dimension=0):
    """
    判断方块是否可以放置

    :param identifier: str 方块identifier，如minecraft:wheat
    :param block_pos: tuple(int,int,int) 方块将要放置的坐标
    :param facing: int 朝向，详见[Facing]枚举
    :param dimension: int 维度，默认为主世界0
    :return: bool 方块是否可以放置
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.MayPlace(identifier, block_pos, facing, dimension)


def player_destroy_block(player_id, pos, particle=True, send_inv=False):
    """
    玩家使用手上工具破坏方块

    手上工具的附魔效果会生效，同时扣除耐久度

    会触发ServerPlayerTryDestroyBlockEvent事件，并且可以被这个事件cancel

    1.23 调整 新增sendInv参数，用于同步服务端背包信息,默认为不同步

    1.22 调整 新增particle参数，用于设置是否开启破坏粒子效果,1:开启,0:关闭,默认为1

    1.20 新增 增加使用手上工具破坏方块接口

    :param player_id: 此处playerId为block的破坏者
    :param pos: tuple(int,int,int) 方块位置
    :param particle: bool 是否开启破坏粒子效果，默认为开
    :param send_inv: bool 是否同步服务端背包信息，默认为不同步。
        因为破坏方块可能会造成手持物品耐久度降低等信息改变，不同步信息可能会造成后续一些逻辑异常，若大批量破坏方块，每次同步会有性能问题，建议前面的调用可令sendInv为False，在最后一次调用此函数时传入sendInv为True。
    :return: bool 设置结果
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.PlayerDestoryBlock(pos, 1 if particle else 0, send_inv)


def player_use_item_to_pos(player_id, pos, slot_type, slot_pos=0, facing=1):
    """
    玩家对某个坐标使用物品

    当使用抛射物时，只有在非创造模式下才会返回True

    如果要对"盔甲架"等实体使用物品，请使用PlayerUseItemToEntity接口

    只能对玩家周边200格以内的坐标使用

    :param player_id: 使用物品的玩家
    :param pos: tuple(int,int,int) 坐标
    :param slot_type: int 物品所在的地方[ItemPosType]枚举
    :param slot_pos: int 槽位，获取INVENTORY及ARMOR时需要设置，其他情况写0即可
    :param facing: int 朝向，详见[Facing]枚举
    :return: bool 设置结果
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.PlayerUseItemToPos(pos, slot_type, slot_pos, facing)


def player_use_item_to_entity(player_id, entity_id):
    """
    玩家使用手上物品对某个生物使用

    :param player_id: 使用物品的玩家
    :param entity_id: str 生物entityId
    :return: bool 设置结果
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(player_id)
    return block_info_comp.PlayerUseItemToEntity(entity_id)


def spawn_resources(identifier, pos, aux, **kwargs):
    """
    产生方块随机掉落（该方法不适用于实体方块）

    1.20 调整 新增dimensionId，默认为-1，传入非负值时用于控制产生方块掉落的维度，可在对应维度的常加载区块产生掉落

    1.18 新增 产生方块随机掉落

    :param identifier: str 方块的identifier，如minecraft:wool
    :param pos: tuple(int,int,int) 掉落位置
    :param aux: int 方块的附加值
    :param kwargs: dict
        dimensionId: int 掉落方块的维度，默认值为0，传入非负值时用于获取产生方块掉落的维度；否则将随机挑选一个存在玩家的维度产生掉落
        probability: float 掉落概率，范围为[0, 1]，0为不掉落，1为100%掉落，对部分农作物树叶不生效
        bonusLootLevel: int [时运等级]，默认为0，只对部分方块生效
        allowRandomness: bool 是否允许随机采集，默认为True，如果为False，掉落概率probability无效
    :return: bool 是否成功
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.SpawnResources(identifier, pos, aux, **kwargs)


def spawn_resources_silk_touched(identifier, pos, aux, dimension_id):
    """
    模拟方块精准采集掉落

    如果指定方块不属于精准采集方块，返回False

    1.22 新增 模拟方块精准采集掉落

    :param identifier: str 方块的identifier，如minecraft:wool
    :param pos: tuple(int,int,int) 掉落位置
    :param aux: int 方块的附加值
    :param dimension_id: int 掉落方块的维度，默认值为0，传入非负值时用于获取产生方块掉落的维度；否则将随机挑选一个存在玩家的维度产生掉落
    :return: bool 是否成功
    """
    block_info_comp = serverApi.GetEngineCompFactory().CreateBlockInfo(level_id)
    return block_info_comp.SpawnResourcesSilkTouched(identifier, pos, aux, dimension_id)


def get_block_states(pos, dimension=0):
    """
    获取[方块状态]

    https://minecraft.gamepedia.com/Block_states

    1.23 调整 废弃player_id参数

    1.20 调整 新增dimensionId参数，默认为-1，传入非负值时不依赖playerId，可获取对应维度的常加载区块内方块状态

    1.18 新增 获取方块状态

    :param pos: tuple(float,float,float) 方块位置
    :param dimension: int 方块所在维度，默认值为0，传入非负值时不依赖playerId
    :return: dict 方块状态，异常时为None
    """
    block_state_comp = serverApi.GetEngineCompFactory().CreateBlockState(level_id)
    return block_state_comp.GetBlockStates(pos, dimension)


def set_block_states(pos, data, dimension=0):
    """
    获取[方块状态]

    https://minecraft.gamepedia.com/Block_states

    仅可设置已加载区块内的方块状态，支持设置对应维度的常加载区块内方块状态

    1.23 调整 废弃player_id参数

    1.18 新增 设置方块状态

    1.20 调整 增加参数dimensionId，默认为-1，传入非负值时不依赖playerId，可设置对应维度的常加载区块内方块状态

    :param pos: tuple(float,float,float) 方块位置
    :param data: dict 方块状态
    :param dimension: int 方块所在维度，默认值为0，传入非负值时不依赖playerId
    :return: bool 设置是否成功
    """
    block_state_comp = serverApi.GetEngineCompFactory().CreateBlockState(level_id)
    return block_state_comp.SetBlockStates(pos, data, dimension)


def get_block_aux_from_states(block_name, states):
    """
    根据方块名称和[方块状态]获取方块附加值AuxValue

    1.19 新增 根据方块名称和[方块状态]获取方块附加值AuxValue

    :param block_name: str 方块名称
    :param states: dict 方块状态
    :return: int 方块附加值AuxValue，异常时为-1
    """
    block_state_comp = serverApi.GetEngineCompFactory().CreateBlockState(level_id)
    return block_state_comp.GetBlockAuxValueFromStates(block_name, states)


def get_block_states_from_aux(block_name, aux_value):
    """
    根据方块名称和方块附加值AuxValue获取[方块状态]

    1.18 新增 根据方块名称和方块附加值AuxValue获取方块状态

    :param block_name: str 方块名称
    :param aux_value: int 方块附加值AuxValue
    :return: dict 方块状态，异常时为None
    """
    block_state_comp = serverApi.GetEngineCompFactory().CreateBlockState(level_id)
    return block_state_comp.GetBlockStatesFromAuxValue(block_name, aux_value)


def add_block_item_listen_for_use_event(block_name):
    """
    增加blockName方块对ServerBlockUseEvent事件的脚本层监听

    1.19 调整 去掉增加原版方块监听ServerBlockUseEvent事件时同步到客户端的功能

    :param block_name: str 方块名称，格式：namespace:name:AuxValue，其中namespace:name:*匹配所有的方块数据值AuxValue
    :return: bool 是否增加成功
    """
    block_use_event_white_list_comp = serverApi.GetEngineCompFactory().CreateBlockUseEventWhiteList(level_id)
    return block_use_event_white_list_comp.AddBlockItemListenForUseEvent(block_name)


def clear_all_block_item_listen_for_use_event():
    """
    清空所有已添加方块对ServerBlockUseEvent事件的脚本层监听

    1.19 调整 去掉清空原版方块监听ServerBlockUseEvent事件时同步到客户端的功能

    :return: bool 是否清空成功
    """
    block_use_event_white_list_comp = serverApi.GetEngineCompFactory().CreateBlockUseEventWhiteList(level_id)
    return block_use_event_white_list_comp.ClearAllListenForBlockUseEventItems()


def remove_block_item_listen_for_use_event(block_name):
    """
    移除blockName方块对ServerBlockUseEvent事件的脚本层监听

    1.19 调整 去掉移除原版方块监听ServerBlockUseEvent事件时同步到客户端的功能

    :param block_name: str 方块名称，格式：namespace:name:AuxValue，其中namespace:name:*匹配所有的方块数据值AuxValue
    :return: bool 是否移除成功
    """
    block_use_event_white_list_comp = serverApi.GetEngineCompFactory().CreateBlockUseEventWhiteList(level_id)
    return block_use_event_white_list_comp.RemoveBlockItemListenForUseEvent(block_name)


def get_block_powered_state(pos, dimension):
    """
    获取某个坐标方块的充能状态

    1.20 新增 获取某个坐标方块的充能状态

    :param pos: tuple(float,float,float) 方块坐标位置
    :param dimension: int 目标维度
    :return: int 充能状态 0:未充能；1：弱充能；2：强充能
    """
    red_stone_comp = serverApi.GetEngineCompFactory().CreateRedStone(level_id)
    return red_stone_comp.GetBlockPoweredState(pos, dimension)


def get_redstone_signal_strength(pos, dimension=0):
    """
    获取某个坐标的红石信号强度

    1.23 调整 废弃player_id参数

    1.20 调整 新增dimensionId参数，默认为-1，传入非负值时不依赖playerId，可获取对应维度的常加载区块内红石信号强度

    1.18 新增 获取某个坐标的红石信号强度

    :param pos: pos tuple(float,float,float) 坐标位置
    :param dimension: int 目标维度，默认值为0，传入非负值时不依赖playerId，CreateRedStone可传入levelId，否则CreateRedStone需传入playerId来获取玩家当前维度
    :return: int 红石信号强度[0, 15]
    """
    red_stone_comp = serverApi.GetEngineCompFactory().CreateRedStone(level_id)
    return red_stone_comp.GetStrength(pos, dimension)
