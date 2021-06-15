# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi


def get_player_exp(player_id, is_percent=True):
    """
    获取玩家经验值

    如果设置返回百分比为False，则返回玩家当前等级下经验的绝对值（非当前玩家总经验值）。

    :param player_id:
    :param is_percent: bool 是否为百分比，默认为True
    :return: float 玩家经验值
    """
    exp_comp = serverApi.GetEngineCompFactory().CreateExp(player_id)
    return exp_comp.GetPlayerExp(is_percent)


def get_player_total_exp(player_id):
    """
    获取玩家的总经验值

    :param player_id:
    :return: int 经验值，正整数。获取失败的情况下返回-1。
    """
    exp_comp = serverApi.GetEngineCompFactory().CreateExp(player_id)
    return exp_comp.GetPlayerTotalExp()


def set_player_total_exp(player_id, exp):
    """
    设置玩家的总经验值

    根据总经验值会重新计算等级，该接口可引起等级的变化

    内部运算采用浮点数，数值较大时会出现误差

    :param player_id:
    :param exp: int	总经验值，正整数
    :return: bool 设置是否成功
    """
    exp_comp = serverApi.GetEngineCompFactory().CreateExp(player_id)
    return exp_comp.SetPlayerTotalExp(exp)


def add_player_exp(player_id, exp):
    """
    修改玩家经验值

    如果设置的exp值为负数，且超过当前等级已有的经验值，调用接口后，该玩家等级不会下降但是经验值会置为最小值

    :param player_id:
    :param exp: int 玩家经验值，可设置负数
    :return: bool 设置是否成功
    """
    exp_comp = serverApi.GetEngineCompFactory().CreateExp(player_id)
    return exp_comp.AddPlayerExperience(exp)


def set_exp_orb_value(player_id, exp):
    """
    修改经验球经验

    设置经验球经验，entityId是经验球的entityId,如果经验小于等于0，拾取后不再加经验

    1.18 新增 修改经验球经验

    :param player_id:
    :param exp: int 经验球经验
    :return: bool 设置是否成功
    """
    exp_comp = serverApi.GetEngineCompFactory().CreateExp(player_id)
    return exp_comp.SetOrbExperience(exp)


def get_exp_orb_value(player_id):
    """
    获取经验球的经验

    :param player_id:
    :return: int 经验值，正整数。获取失败的情况下返回-1。
    """
    exp_comp = serverApi.GetEngineCompFactory().CreateExp(player_id)
    return exp_comp.GetOrbExperience()


def create_exp_orb(player_id, exp, position, is_special=True):
    """
    创建专属经验球

    设置经验球经验，entityId是人的entityId。专属的经验球只有entityId的人才能拾取

    1.18 新增 创建专属经验球

    :param player_id:
    :param exp: int 经验球经验
    :param position: tuple(float,float,float) 创建的位置
    :param is_special: bool 是否专属经验球
    :return: bool 设置是否成功
    """
    exp_comp = serverApi.GetEngineCompFactory().CreateExp(player_id)
    return exp_comp.CreateExperienceOrb(exp, position, is_special)


def is_player_flying(player_id):
    """
    获取玩家是否在飞行

    1.18 新增 获取玩家是否在飞行

    :param player_id:
    :return: bool True:是 False:否
    """
    fly_comp = serverApi.GetEngineCompFactory().CreateFly(player_id)
    return fly_comp.IsPlayerFlying()


def change_player_fly_state(player_id, is_fly):
    """
    改变玩家的飞行状态

    1.19 新增 改变玩家的飞行状态

    :param player_id:
    :param is_fly: isFly bool 飞行状态，True：飞行模式，False：正常行走模式
    :return: bool True:是 False:否
    """
    fly_comp = serverApi.GetEngineCompFactory().CreateFly(player_id)
    return fly_comp.ChangePlayerFlyState(is_fly)


def get_player_level(player_id):
    """
    获取玩家等级

    :param player_id:
    :return: int 玩家等级
    """
    lv_comp = serverApi.GetEngineCompFactory().CreateLv(player_id)
    return lv_comp.GetPlayerLevel()


def add_player_level(player_id, level):
    """
    修改玩家等级

    :param player_id:
    :param level: int 玩家等级，可设置负数
    :return: bool 设置是否成功
    """
    lv_comp = serverApi.GetEngineCompFactory().CreateLv(player_id)
    return lv_comp.AddPlayerLevel(level)


def get_player_hunger(player_id):
    """
    获取玩家饥饿度，展示在UI饥饿度进度条上，初始值为20，即每一个鸡腿代表2个饥饿度。

     **饱和度(saturation)** ：
        玩家当前饱和度，初始值为5，最大值始终为玩家当前饥饿度(hunger)，该值直接影响玩家

     **饥饿度(hunger)**。
        1）增加方法：吃食物。
        2）减少方法：每触发一次消耗事件，该值减少1，如果该值不大于0，直接把玩家饥饿度(hunger)减少1。

    :param player_id:
    :return: float 玩家饥饿度
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.GetPlayerHunger()


def set_player_hunger(player_id, value):
    """
    设置玩家饥饿度

    :param player_id:
    :param value: float 饥饿度
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerHunger(value)


def get_player_max_exhaustion_value(player_id):
    """
    获取玩家foodExhaustionLevel的归零值，常量值，默认为4。

    **消耗度(exhaustion)** 是指玩家当前消耗度水平，初始值为0，该值会随着玩家一系列动作（如跳跃）的影响而增加。

    当该值大于最大消耗度（maxExhaustion）后归零，并且把饱和度（saturation）减少1（为了说明饥饿度机制，我们将此定义为 **消耗事件** ）

    :param player_id:
    :return: float 玩家foodExhaustionLevel的归零值
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.GetPlayerMaxExhaustionValue()


def set_player_max_exhaustion_value(player_id, value):
    """
    设置玩家foodExhaustionLevel的归零值

    通过调整 **最大消耗度(maxExhaustion)** 的大小，就可以加快或者减慢 **饥饿度(hunger)** 的消耗，当 **最大消耗度(maxExhaustion)** 很大时，饥饿度可以看似一直不下降

    :param player_id:
    :param value: float foodExhaustionLevel的归零值
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerMaxExhaustionValue(value)


def get_player_health_level(player_id):
    """
    获取玩家健康临界值，当饥饿值大于等于健康临界值时会自动恢复血量，开启饥饿值且开启自然恢复时有效。原版默认值为18

    :param player_id:
    :return: int 健康临界值，-1表示获取失败
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.GetPlayerHealthLevel()


def set_player_health_level(player_id, health_level):
    """
    设置玩家健康临界值，当饥饿值大于等于健康临界值时会自动恢复血量，开启饥饿值且开启自然恢复时有效.原版默认值为18

    注：健康临界值始终大于等于饥饿临界值。如果设置的健康临界值小于饥饿临界值，饥饿临界值将被设置为当前的健康临界值

    :param player_id:
    :param health_level: int 健康临界值
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerHealthLevel(health_level)


def get_player_health_tick(player_id):
    """
    获取玩家自然恢复速度，当饥饿值大于等于健康临界值时会自动恢复血量，开启饥饿值且开启自然恢复时有效。

    原版默认值为80刻（即每4秒）恢复1点血量

    :param player_id:
    :return: int 自然恢复速度，-1表示获取失败
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.GetPlayerHealthTick()


def set_player_health_tick(player_id, health_tick):
    """
    设置玩家自然恢复速度，当饥饿值大于等于健康临界值时会自动恢复血量，开启饥饿值且开启自然恢复时有效。

    最小值为1，即每秒恢复20点血量

    原版默认值为80刻（即每4秒）恢复1点血量

    :param player_id:
    :param health_tick: int 自然恢复速度
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerHealthTick(health_tick)


def is_player_natural_regen(player_id):
    """
    是否开启玩家自然恢复，当饥饿值大于等于健康临界值时会自动恢复血量，开启饥饿值且开启自然恢复时有效。原版默认开启

    :param player_id:
    :return: bool True表示开启，False表示关闭，None表示获取失败
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.IsPlayerNaturalRegen()


def set_player_natural_regen(player_id, value):
    """
    设置是否开启玩家自然恢复，当饥饿值大于等于健康临界值时会自动恢复血量，开启饥饿值且开启自然恢复时有效.原版默认开启

    :param player_id:
    :param value: bool True开启，False关闭
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerNaturalRegen(value)


def get_player_starve_level(player_id):
    """
    获取玩家饥饿临界值，当饥饿值小于饥饿临界值时会自动扣除血量，开启饥饿值且开启饥饿掉血时有效。原版默认值为1

    :param player_id:
    :return: int 饥饿临界值 -1表示获取失败
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.GetPlayerStarveLevel()


def set_player_starve_level(player_id, starve_level):
    """
    设置玩家饥饿临界值，当饥饿值小于饥饿临界值时会自动扣除血量，开启饥饿值且开启饥饿掉血时有效。原版默认值为1

    健康临界值始终大于等于饥饿临界值。如果设置的饥饿临界值大于健康临界值，将被设置为当前的健康临界值

    :param player_id:
    :param starve_level: int 饥饿临界值
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerStarveLevel(starve_level)


def get_player_starve_tick(player_id):
    """
    获取玩家饥饿掉血速度，当饥饿值小于饥饿临界值时会自动扣除血量，开启饥饿值且开启饥饿掉血时有效。原版默认值为80刻（即每4秒）扣除1点血量

    :param player_id:
    :return: int 饥饿掉血速度，-1表示获取失败
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.GetPlayerStarveTick()


def set_player_starve_tick(player_id, starve_tick):
    """
    设置玩家饥饿掉血速度，当饥饿值小于饥饿临界值时会自动扣除血量，开启饥饿值且开启饥饿掉血时有效。

    最小值为1，即每秒扣20点血量

    原版默认值为80刻（即每4秒）扣除1点血量

    :param player_id:
    :param starve_tick: int 饥饿掉血速度
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerStarveTick(starve_tick)


def is_player_natural_starve(player_id):
    """
    是否开启玩家饥饿掉血，当饥饿值小于饥饿临界值时会自动恢复血量，开启饥饿值且开启饥饿掉血时有效。原版默认开启

    :return: bool True表示开启，False表示关闭，None表示获取失败
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.IsPlayerNaturalStarve()


def set_player_natural_starve(player_id, value):
    """
    设置是否开启玩家饥饿掉血，当饥饿值小于饥饿临界值时会自动扣除血量，开启饥饿值且开启饥饿掉血时有效.原版默认开启

    :param player_id:
    :param value: bool True开启，False关闭
    :return:
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerNaturalStarve(value)


def enable_hit_player_crit_box(player_id):
    """
    开启玩家爆头

    开启后该玩家头部被击中后会触发ProjectileCritHitEvent事件。

    :param player_id:
    :return:
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    player_comp.OpenPlayerCritBox()


def disable_hit_player_crit_box(player_id):
    """
    关闭玩家爆头

    关闭后将无法触发ProjectileCritHitEvent事件。

    :param player_id:
    :return:
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    player_comp.ClosePlayerCritBox()


def set_player_movable(player_id, is_movable=False):
    """
    设置玩家是否可移动

    :param player_id:
    :param is_movable: bool 是否可移动,True允许移动，False禁止移动
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerMovable(is_movable)


def set_player_jumpable(player_id, is_jumpable=False):
    """
    设置玩家是否可跳跃

    :param player_id:
    :param is_jumpable: bool 是否可跳跃,True允许跳跃，False禁止跳跃
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerJumpable(is_jumpable)


def set_player_game_type(player_id, game_type):
    """
    设置玩家个人游戏模式

    :param player_id:
    :param game_type: int GetMinecraftEnum().GameType.*:Survival，Creative，Adventure分别为0~2
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerGameType(game_type)


def enable_player_hit_block_detection(player_id, precision):
    """
    开启碰撞方块的检测，开启后碰撞时会触发OnPlayerHitBlockServerEvent事件

    注：该碰撞检测会屏蔽草、空气、火、高草四种方块

    :param player_id:
    :param precision: float 碰撞检测精度，参数需要在区间[0, 1)
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.OpenPlayerHitBlockDetection(precision)


def disable_player_hit_block_detection(player_id):
    """
    关闭碰撞方块的检测，关闭后将不会触发OnPlayerHitBlockServerEvent事件

    :param player_id:
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.ClosePlayerHitBlockDetection()


def enable_player_hit_mob_detection(player_id):
    """
    开启碰撞生物的检测，开启后碰撞时会触发OnPlayerHitMobServerEvent事件

    :param player_id:
    :return: bool 是否开启成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.OpenPlayerHitMobDetection()


def disable_player_hit_mob_detection(player_id):
    """
    关闭碰撞生物的检测，关闭后将不会触发OnPlayerHitMobServerEvent事件

    :param player_id:
    :return: bool 是否关闭成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.ClosePlayerHitMobDetection()


def set_player_pickup_distance(player_id, area):
    """
    设置玩家的拾取物品范围

    设置后该玩家的拾取物品范围会在 **原版拾取范围** 的基础上进行改变。

    :param player_id:
    :param area: tuple(float,float,float) 拾取物品范围，传入(0, 0, 0)时视作取消设置
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPickUpArea(area)


def set_keep_inventory(player_id, enable):
    """
    设置玩家死亡不掉落物品

    :param player_id:
    :param enable: bool 是否开启“保留物品栏”
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.EnableKeepInventory(enable)


def is_sneaking(player_id):
    """
    获取玩家是否处于潜行状态

    1.18 新增 获取玩家是否处于潜行状态

    :param player_id:
    :return: bool 当前玩家是否处于潜行状态
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.isSneaking()


def is_swimming(player_id):
    """
    获取玩家是否处于游泳状态。

    1.19 新增 获取玩家是否处于游泳状态

    :param player_id:
    :return: bool 当前玩家是否处于游泳状态
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.isSwimming()


def clear_defined_level_up_cost(player_id, level):
    """
    清理自定义的升级经验，清理后才有会再次回调ChangeLevelUpCostServerEvent事件并再次设置新的升级经验值。

    1.19 新增 清理自定义的升级经验，清理后才有会再次回调ChangeLevelUpCostServerEvent事件并再次设置新的升级经验值。

    :param player_id:
    :param level: int 指定清理的等级，加入传入的数值小于0，则清理所有等级的升级经验值缓存
    :return: bool 是否清理成功。
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.ClearDefinedLevelUpCost(level)


def get_player_operation(player_id):
    """
    获取玩家权限类型信息

    1.19 新增 获取玩家权限类型信息

    :param player_id:
    :return: int 权限类型信息，Visitor ：0,Member：1,Operator：2,Custom：3,
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.GetPlayerOperation()


def set_player_respawn_pos(player_id, pos, dimension=0):
    """
    设置玩家复活的位置

    1.22 调整 新增参数dimensionId，支持设置复活维度

    :param player_id:
    :param pos: tuple(int,int,int) 复活点的位置坐标
    :param dimension: 复活点的维度，默认值为0（主世界），注意1：维度21是不可用的；注意2：不能在玩家死亡（PlayerDieEvent）之后设置复活点
    :return: bool 是否设置成功
    """
    player_comp = serverApi.GetEngineCompFactory().CreatePlayer(player_id)
    return player_comp.SetPlayerRespawnPos(pos, dimension)
