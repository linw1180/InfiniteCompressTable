# -*- coding: utf-8 -*-

import warnings

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def set_attack_target(entity_id, target_id):
    """
    设置攻击目标
    
    :param entity_id: 
    :param target_id: str 攻击目标实体id
    :return: bool 设置结果
    """
    action_comp = serverApi.GetEngineCompFactory().CreateAction(entity_id)
    action_comp.SetAttackTarget(target_id)


def clear_attack_target(entity_id):
    """
    清除标记攻击目标
    
    :param entity_id: 
    :return: bool 设置结果
    """
    action_comp = serverApi.GetEngineCompFactory().CreateAction(entity_id)
    action_comp.ResetAttackTarget()


def get_attack_target(entity_id):
    """
    获取攻击目标

    :param entity_id:
    :return: str 攻击目标实体id
    """
    action_comp = serverApi.GetEngineCompFactory().CreateAction(entity_id)
    action_comp.GetAttackTarget()


def set_hurt_by(entity_id, attacker_id):
    """
    设置攻击自己的对象实体id
    
    :param entity_id: 
    :param attacker_id: str 攻击自己的对象实体id
    :return: bool 设置结果
    """
    action_comp = serverApi.GetEngineCompFactory().CreateAction(entity_id)
    action_comp.SetHurtBy(attacker_id)


def clear_hurt_by(entity_id):
    """
    清除标记攻击自己的对象实体id
    
    :param entity_id: 
    :return: bool 设置结果
    """
    action_comp = serverApi.GetEngineCompFactory().CreateAction(entity_id)
    action_comp.ResetHurtBy()


def get_hurt_by(entity_id):
    """
    获取攻击自己的对象实体id
    
    :param entity_id: 
    :return: str 攻击自己的对象实体id
    """
    action_comp = serverApi.GetEngineCompFactory().CreateAction(entity_id)
    action_comp.GetHurtBy()


def set_mob_knockback(entity_id, **kwargs):
    """
    设置击退的初始速度，需要考虑阻力的影响
    
    :param entity_id: 
    :param kwargs: 
        xd: float x轴方向，用來控制角度
        zd: float z轴方向，用來控制角度
        power: float 用来控制水平方向的初速度
        height: float 竖直方向的初速度
        heightCap: float 向上速度阈值，当实体本身已经有向上的速度时需要考虑这个值，用来确保最终向上的速度不会超过heightCap
    :return: 
    """
    action_comp = serverApi.GetEngineCompFactory().CreateAction(entity_id)
    action_comp.SetMobKnockback(**kwargs)


def spawn_loot_table(player_id, pos, identifier, player_killer_id=None, damage_cause_entity_id=None):
    """
    使用生物类型模拟一次随机掉落，生成的物品与json定义的概率有关

    需要在对应的player实体附近生成，否则会生成失败。对于某些特殊的生物，如minecraft:sheep，需要使用SpawnLootTableWithActor接口来模拟随机掉落。

    1.18 新增 生成生物一次随机掉落

    :param player_id:
    :param pos: tuple(int,int,int) 掉落位置
    :param identifier: str 实体identifier，如minecraft:guardian
    :param player_killer_id: str 玩家杀手（只能是玩家），默认None
    :param damage_cause_entity_id: str 伤害来源实体Id（掉落与该实体手持物品的抢夺附魔等级有关），默认None
    :return: bool 是否成功生成掉落
    """
    loot_comp = serverApi.GetEngineCompFactory().CreateActorLoot(player_id)
    return loot_comp.SpawnLootTable(pos, identifier, player_killer_id, damage_cause_entity_id)


def spawn_loot_table_with_actor(player_id, pos, entity_id, player_killer_id=None, damage_cause_entity_id=None):
    """
    使用生物实例模拟一次随机掉落，生成的物品与json定义的概率有关

    需要在对应的player实体附近生成，否则会生成失败

    1.18 新增 使用生物Id生成一次随机掉落

    :param player_id:
    :param pos: tuple(int,int,int) 掉落位置
    :param entity_id: str 模拟生物的生物Id
    :param player_killer_id: str 玩家杀手（只能是玩家），默认None
    :param damage_cause_entity_id: str 伤害来源实体Id（掉落与该实体手持物品的抢夺附魔等级有关），默认None
    :return: bool 是否成功生成掉落
    """
    loot_comp = serverApi.GetEngineCompFactory().CreateActorLoot(player_id)
    return loot_comp.SpawnLootTableWithActor(pos, entity_id, player_killer_id, damage_cause_entity_id)


def set_actor_pushable(entity_id, is_pushable=False):
    """
    设置实体是否可推动

    :param entity_id:
    :param is_pushable: bool False:不可推动  True:可推动
    :return: bool True表示设置成功
    """
    actor_pushable_comp = serverApi.GetEngineCompFactory().CreateActorPushable(entity_id)
    return actor_pushable_comp.SetActorPushable(1 if is_pushable else 0)


def set_attr_value(entity_id, attr_type, value):
    """
    设置属性值

    设置接口暂不支持 ABSORPTION

    1.20 调整 新增类型说明

    :param entity_id:
    :param attr_type: int [AttrType]枚举
    :param value: float 属性值
    :return: bool 设置结果
    """
    attr_comp = serverApi.GetEngineCompFactory().CreateAttr(entity_id)
    return attr_comp.SetAttrValue(attr_type, value)


def get_attr_value(entity_id, attr_type):
    """
    获取属性值

    1.20 调整 新增ABSORPTION(伤害吸收生命值)类型支持

    :param entity_id:
    :param attr_type: int [AttrType]枚举
    :return: float 属性结果
    """
    attr_comp = serverApi.GetEngineCompFactory().CreateAttr(entity_id)
    return attr_comp.GetAttrValue(attr_type)


def set_attr_max_value(entity_id, attr_type, value):
    """
    设置属性最大值

    设置的最大饱和度不能超过当前的饥饿值; 食用食物后，最大饱和度会被原版游戏机制修改

    设置接口暂不支持 ABSORPTION

    1.20 调整 新增类型说明

    :param entity_id:
    :param attr_type:
    :param value: float 属性值
    :return: bool 设置结果
    """
    attr_comp = serverApi.GetEngineCompFactory().CreateAttr(entity_id)
    return attr_comp.SetAttrMaxValue(attr_type, value)


def get_attr_max_value(entity_id, attr_type):
    """
    获取属性最大值

    1.20 调整 新增ABSORPTION(伤害吸收生命值)类型支持

    :param entity_id:
    :param attr_type: int [AttrType]枚举
    :return: float 属性值结果
    """
    attr_comp = serverApi.GetEngineCompFactory().CreateAttr(entity_id)
    return attr_comp.GetAttrMaxValue(attr_type)


def is_entity_on_fire(entity_id):
    """
    获取实体是否着火

    1.18 新增 获取实体是否着火

    :param entity_id:
    :return: bool 是否着火
    """
    attr_comp = serverApi.GetEngineCompFactory().CreateAttr(entity_id)
    return attr_comp.IsEntityOnFire()


def set_entity_on_fire(entity_id, seconds):
    """
    设置实体着火

    在水中或者雨中不会生效，着火时间受生物装备、生物的状态影响，不一定等于设置的参数

    1.18 新增 设置实体是否着火

    :param entity_id:
    :param seconds: int 着火时间（单位：秒）
    :return: bool 是否设置成功
    """
    attr_comp = serverApi.GetEngineCompFactory().CreateAttr(entity_id)
    return attr_comp.SetEntityOnFire(seconds)


def get_entity_aux_value(projectile_id):
    """
    获取射出的弓箭或投掷出的药水的附加值

    :param projectile_id:
    :return: int auxValue，具体数值见wiki的“箭”及“药水”页面
    """
    aux_value_comp = serverApi.GetEngineCompFactory().CreateAuxValue(projectile_id)
    return aux_value_comp.GetAuxValue()


def set_entity_collision_box_size(entity_id, size):
    """
    设置实体的包围盒

    对新生产的实体需要经过5帧之后再设置包围盒的大小才会生效

    :param entity_id:
    :param size: tuple(int,int) 第一位表示宽度和长度，第二位表示高度
    :return: bool 设置结果
    """
    collision_box_comp = serverApi.GetEngineCompFactory().CreateCollisionBox(entity_id)
    return collision_box_comp.SetSize(size)


def get_entity_collision_box_size(entity_id):
    """
    获取实体的包围盒

    :param entity_id:
    :return: tuple(int,int) 包围盒大小
    """
    collision_box_comp = serverApi.GetEngineCompFactory().CreateCollisionBox(entity_id)
    return collision_box_comp.GetSize()


def change_player_dimension(player_id, dimension, pos):
    """
    传送玩家

    :param player_id:
    :param dimension: int 维度，0-overWorld; 1-nether; 2-theEnd
    :param pos: tuple(int,int,int) 传送的坐标
    :return: bool 是否设置成功
    """
    dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(player_id)
    return dimension_comp.ChangePlayerDimension(dimension, pos)


def get_entity_dimension(entity_id):
    """
    获取实体dimension

    :param entity_id:
    :return: int 实体维度
    """
    dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(entity_id)
    return dimension_comp.GetEntityDimensionId()


def change_entity_dimension(entity_id, dimension, pos=None):
    """
    传送实体，仅Apollo网络服可用

    1.19.0 新增 传送实体，仅Apollo网络服可用

    :param entity_id:
    :param dimension: int 维度，0-overWorld; 1-nether; 2-theEnd
    :param pos: tuple(int,int,int) 传送的坐标，假如输入None，那么就优先选择目标维度的传送门作为目的地，其次使用维度坐标映射逻辑确定目的地
    :return: bool 是否设置成功
    """
    warnings.warn("1.20 目前ChangeEntityDimension仅Apollo网络服可用", DeprecationWarning)

    dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(entity_id)
    return dimension_comp.ChangeEntityDimension(dimension, pos)


def create_new_dimension(dimension):
    """
    创建新的dimension

    要求在初始化mod时调用

    :param dimension: dimensionId int 维度，0/1/2维度是不需要创建的。dimensionId取值范围为[0, 20]
    :return: bool 是否创建成功
    """
    dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(level_id)
    return dimension_comp.CreateDimension(dimension)


def mirror_dimension(player_id, from_id, to_id):
    """
    复制不同dimension的地形

    :param player_id:
    :param from_id: int 原dimensionId
    :param to_id: int 目标dimensionId
    :return: bool 是否设置成功
    """
    dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(player_id)
    return dimension_comp.MirrorDimension(from_id, to_id)


def register_entity_aoi_event(player_id, dimension, name, aabb, ignored_entities):
    """
    注册感应区域，有生物进入时和离开时会有消息通知

    :param player_id:
    :param dimension: int 维度id
    :param name: str 注册的感应区域名
    :param aabb: tuple(float,float,float,float,float,float) 感应区域的坐标范围，依次为minX, minY, minZ, maxX, maxY, maxZ
    :param ignored_entities: list(str) 忽略的实体id列表
    :return: bool 是否注册成功
    """
    dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(player_id)
    return dimension_comp.RegisterEntityAOIEvent(dimension, name, aabb, ignored_entities)


def remove_entity_aoi_event(player_id, dimension, name):
    """
    反注册感应区域

    :param player_id:
    :param dimension: int 维度id
    :param name: str 需要反注册的感应区域名
    :return: bool 是否注册成功
    """
    dimension_comp = serverApi.GetEngineCompFactory().CreateDimension(player_id)
    return dimension_comp.UnRegisterEntityAOIEvent(dimension, name)


def add_effect_to_entity(entity_id, effect_name, duration, amplifier=0, show_particles=False):
    """
    为实体添加指定状态效果，如果添加的状态已存在则有以下集中情况：
        1. 等级大于已存在则更新状态等级及持续时间；
        2. 状态等级相等且剩余时间duration大于已存在则刷新剩余时间；
        3. 等级小于已存在则不做修改；
        4. 粒子效果以新的为准

    :param entity_id:
    :param effect_name:	状态效果名称字符串，包括自定义状态效果和原版状态效果，
    :param duration: 状态效果持续时间，单位秒
    :param amplifier: 状态效果的额外等级。
        1. 必须在0至255之间（含）。若未指定，默认为0。
        2. 注意，状态效果的第一级（如生命恢复 I）对应为0，因此第二级状态效果，如生命回复 II，应指定强度为1。
        3. 部分效果及自定义状态效果没有强度之分，如夜视
    :param show_particles: 是否显示粒子效果，True显示，False不显示
    :return: bool: True表示设置成功
    """
    effect_comp = serverApi.GetEngineCompFactory().CreateEffect(entity_id)
    return effect_comp.AddEffectToEntity(effect_name, duration, amplifier, show_particles)


def get_all_effects(entity_id):
    """
    获取实体当前所有状态效果

    :param entity_id:
    :return: list: [
        effectDict: {
            effectName:str 状态效果名称,
            duration:int 状态效果剩余持续时间，单位秒,
            amplifier:int 状态效果额外等级
            }
        ]
    """
    effect_comp = serverApi.GetEngineCompFactory().CreateEffect(entity_id)
    return effect_comp.GetAllEffects()


def remove_effect_from_entity(entity_id, effect_name):
    """
    为实体删除指定状态效果

    :param entity_id:
    :param effect_name: 状态效果名称字符串，包括自定义状态效果和原版状态效果
    :return: bool:True表示删除成功
    """
    effect_comp = serverApi.GetEngineCompFactory().CreateEffect(entity_id)
    return effect_comp.RemoveEffectFromEntity(effect_name)


def get_entity_type(entity_id):
    """
    获取实体类型

    :param entity_id:
    :return: int 详见[EntityType]枚举
    """
    engine_type_comp = serverApi.GetEngineCompFactory().CreateEngineType(entity_id)
    return engine_type_comp.GetEngineType()


def get_entity_type_str(entity_id):
    """
    获取实体在游戏中的类型id的str

    :param entity_id:
    :return: str 实体类型的string描述
    """
    engine_type_comp = serverApi.GetEngineCompFactory().CreateEngineType(entity_id)
    return engine_type_comp.GetEngineTypeStr()


def set_extra_data(save_id, key, value):
    """
    用于设置实体的自定义数据或者世界的自定义数据，数据以键值对的形式保存。设置实体数据时使用对应实体id创建组件，设置世界数据时使用levelId创建组件

    :param save_id: 实体id或level_id
    :param key: str 自定义key
    :param value: any key对应的值，支持python基本数据类型
    :return: bool 设置结果
    """
    ex_data_comp = serverApi.GetEngineCompFactory().CreateExtraData(save_id)
    return ex_data_comp.SetExtraData(key, value)


def remove_extra_data(save_id, key):
    """
    清除实体的自定义数据或者世界的自定义数据，清除实体数据时使用对应实体id创建组件，设置世界数据时使用levelId创建组件

    1.18 新增 清理指定key的实体数据/全局数据，数据存放到leveldb

    :param save_id: 实体id或level_id
    :param key: str 自定义key
    :return: bool 设置结果
    """
    ex_data_comp = serverApi.GetEngineCompFactory().CreateExtraData(save_id)
    return ex_data_comp.CleanExtraData(key)


def get_extra_data(save_id, key):
    """
    获取实体的自定义数据或者世界的自定义数据，某个键所对应的值。获取实体数据时使用对应实体id创建组件，获取世界数据时使用levelId创建组件

    :param save_id: 实体id或level_id
    :param key: str 自定义key
    :return: any key对应的值
    """
    ex_data_comp = serverApi.GetEngineCompFactory().CreateExtraData(save_id)
    return ex_data_comp.GetExtraData(key)


def get_whole_extra_data(save_id):
    """
    获取完整的实体的自定义数据或者世界的自定义数据，获取实体数据时使用对应实体id创建组件，获取世界数据时使用levelId创建组件

    1.18 新增 获取完整的实体数据/全局数据字典，数据存放到leveldb。

    :param save_id: 实体id或level_id
    :return: dict或None 获取指定实体或者全局的额外存储数据字典，假如没有任何额外存储数据，那么返回None或者空字典
    """
    ex_data_comp = serverApi.GetEngineCompFactory().CreateExtraData(save_id)
    return ex_data_comp.GetWholeExtraData()


def set_entity_gravity(entity_id, gravity):
    """
    设置实体的重力因子，当生物重力因子为0时则应用世界的重力因子
    
    :param entity_id: 
    :param gravity: float 负数，表示每帧向下的速度
    :return: bool 设置结果
    """
    gravity_comp = serverApi.GetEngineCompFactory().CreateGravity(entity_id)
    return gravity_comp.SetGravity(gravity)


def get_entity_gravity(entity_id):
    """
    获取实体的重力因子，当生物重力因子为0时则应用世界的重力因子
    
    :param entity_id:
    :return: float 重力因子
    """
    gravity_comp = serverApi.GetEngineCompFactory().CreateGravity(entity_id)
    return gravity_comp.GetGravity()


def hurt(entity_id, damage, cause, attacker_id, child_attacker_id=None, knocked=True):
    """
    对实体造成伤害

    1.21 调整 废弃SetHurtByEntity，使用Hurt

    1.19 调整 新增参数knocked，可设置是否产生击退

    :param entity_id:
    :param damage: int 伤害值
    :param cause: 伤害来源 ActorDamageCause
    :param attacker_id: str 伤害来源的实体id
    :param child_attacker_id: 伤害来源的子实体id，默认为None，比如玩家使用抛射物对实体造成伤害，该值应为抛射物Id
    :param knocked: 实体是否被击退，默认值为True
    :return: bool 是否设置成功
    """
    hurt_comp = serverApi.GetEngineCompFactory().CreateHurt(entity_id)
    return hurt_comp.Hurt(damage, cause, attacker_id, child_attacker_id, knocked)


def set_entity_immune_damage(entity_id, immune=True):
    """
    设置实体是否免疫伤害（**该属性存档**）

    :param entity_id:
    :param immune: bool 是否免疫伤害
    :return: bool 是否设置成功
    """
    hurt_comp = serverApi.GetEngineCompFactory().CreateHurt(entity_id)
    return hurt_comp.ImmuneDamage(immune)


def set_entity_mod_attr(entity_id, param_name, param_value):
    """
    设置属性值

    tuple、set在同步时会转成list。建议优先使用数字和字符串等非集合类型。

    :param entity_id:
    :param param_name: str 属性名称，str的名称建议以mod命名为前缀，避免多个mod之间冲突
    :param param_value: any 属性值，支持python基础数据
    :return:
    """
    mod_attr_comp = serverApi.GetEngineCompFactory().CreateModAttr(entity_id)
    return mod_attr_comp.SetAttr(param_name, param_value)


def get_entity_mod_attr(entity_id, param_name, default_value=None):
    """
    获取属性值

    :param entity_id:
    :param param_name: str 属性名称，str的名称建议以mod命名为前缀，避免多个mod之间冲突
    :param default_value: any 属性默认值，属性不存在时返回该默认值，此时属性值依然未设置
    :return: any 返回属性值
    """
    mod_attr_comp = serverApi.GetEngineCompFactory().CreateModAttr(entity_id)
    return mod_attr_comp.GetAttr(param_name, default_value)


def set_entity_persistence(entity_id, is_persistent=True):
    """
    设置实体是否存盘

    :param entity_id:
    :param is_persistent: bool True为存盘，False为不存盘
    :return:
    """
    persistence_comp = serverApi.GetEngineCompFactory().CreatePersistence(entity_id)
    return persistence_comp.SetPersistence(is_persistent)


def set_entity_pos(entity_id, pos):
    """
    设置实体位置
    
    实体行为与使用tp命令一致
    
    1.20 修改 修改行为与使用tp命令一致
    
    :param entity_id: 
    :param pos: pos tuple(int,int,int) xyz值
    :return: bool 设置结果
    """
    pos_comp = serverApi.GetEngineCompFactory().CreatePos(entity_id)
    return pos_comp.SetPos(pos)


def get_entity_pos(entity_id):
    """
    获取实体位置

    对于非玩家，获取到的是脚底部位的位置

    对于玩家，如果处于行走，站立，游泳，潜行，滑翔状态，获得的位置比脚底位置高1.62，如果处于睡觉状态，获得的位置比最低位置高0.2

    :param entity_id:
    :return: tuple(float,float,float) 位置信息
    """
    pos_comp = serverApi.GetEngineCompFactory().CreatePos(entity_id)
    return pos_comp.GetPos()


def get_entity_foot_pos(entity_id):
    """
    获取实体脚所在的位置

    获取实体脚底的位置（除了睡觉时）

    类似接口参见[获取实体位置](#GetPos)

    1.19 新增 获取实体脚底的位置（除了睡觉时）

    :param entity_id:
    :return: tuple(float,float,float) 位置信息
    """
    pos_comp = serverApi.GetEngineCompFactory().CreatePos(entity_id)
    return pos_comp.GetFootPos()


def set_entity_foot_pos(entity_id, pos):
    """
    设置实体脚所在的位置

    实体行为与使用tp命令一致

    1.19 新增 设置实体脚所在的位置

    1.20 修改 修改行为与使用tp命令一致

    :param entity_id:
    :param pos: tuple(float,float,float) 实体脚所在的位置
    :return: bool 是否设置成功
    """
    warnings.warn("可以使用SetPos代替SetFootPos", DeprecationWarning)

    pos_comp = serverApi.GetEngineCompFactory().CreatePos(entity_id)
    pos_comp.SetFootPos(pos)


def set_entity_rot(entity_id, rot):
    """
    设置体角度

    :param entity_id:
    :param rot: tuple(float,float) （上下角度，左右角度）单位是角度而不是弧度
    :return: bool 设置结果
    """
    rot_comp = serverApi.GetEngineCompFactory().CreateRot(entity_id)
    return rot_comp.SetRot(rot)


def get_entity_rot(entity_id):
    """
    获取实体角度

    :param entity_id:
    :return: tuple(float,float) （上下角度，左右角度）单位是角度而不是弧度
    """
    rot_comp = serverApi.GetEngineCompFactory().CreateRot(entity_id)
    return rot_comp.GetRot()


def get_unit_bubble_air_supply():
    """
    单位气泡数对应的氧气储备值

    :return: int 单位气泡数对应的氧气储备值
    """
    breath_comp = serverApi.GetEngineCompFactory().CreateBreath(level_id)
    return breath_comp.GetUnitBubbleAirSupply()


def get_entity_current_air_supply(entity_id):
    """
    生物当前氧气储备值

    注意：该值返回的是当前氧气储备的支持的逻辑帧数 = 氧气储备值 * 逻辑帧数（每秒20帧数）

    1.19 调整 新增备注说明

    :param entity_id:
    :return: int 生物当前氧气储备值
    """
    breath_comp = serverApi.GetEngineCompFactory().CreateBreath(entity_id)
    return breath_comp.GetCurrentAirSupply()


def get_entity_max_air_supply(entity_id):
    """
    获取生物最大氧气储备值

    注意：该值返回的是最大氧气储备的支持的逻辑帧数 = 氧气储备值 * 逻辑帧数（每秒20帧数）

    1.19 调整 新增备注说明

    :param entity_id:
    :return: int 最大氧气储备值
    """
    breath_comp = serverApi.GetEngineCompFactory().CreateBreath(entity_id)
    return breath_comp.GetMaxAirSupply()


def set_entity_current_air_supply(entity_id, data):
    """
    设置生物氧气储备值

    注意：该值设置的是当前氧气储备的支持的逻辑帧数 = 氧气储备值 * 逻辑帧数（每秒20帧数）

    1.19 调整 新增备注说明

    :param entity_id:
    :param data: int 设置生物当前氧气值
    :return: bool 设置结果
    """
    breath_comp = serverApi.GetEngineCompFactory().CreateBreath(entity_id)
    return breath_comp.SetCurrentAirSupply(data)


def set_entity_max_air_supply(entity_id, data):
    """
    设置生物最大氧气储备值

    注意：该值设置的是最大氧气储备的支持的逻辑帧数 = 氧气储备值 * 逻辑帧数（每秒20帧数）

    1.19 调整 新增备注说明

    :param entity_id:
    :param data: int 设置生物最大氧气值
    :return: bool 设置结果
    """
    breath_comp = serverApi.GetEngineCompFactory().CreateBreath(entity_id)
    return breath_comp.SetMaxAirSupply(data)


def is_consuming_air_supply(entity_id):
    """
    获取生物当前是否在消耗氧气

    :param entity_id:
    :return: bool 是否消耗氧气
    """
    breath_comp = serverApi.GetEngineCompFactory().CreateBreath(entity_id)
    return breath_comp.IsConsumingAirSupply()


def set_recover_total_air_supply_time(entity_id, time_sec):
    """
    设置恢复最大氧气量的时间，单位秒

    注意：当设置的最大氧气值小于（timeSec*10）时，生物每帧恢复氧气量的值为0

    1.19 新增 设置恢复最大氧气量的时间

    :param entity_id:
    :param time_sec: float 恢复生物最大氧气值
    :return: bool 是否设置成功
    """
    breath_comp = serverApi.GetEngineCompFactory().CreateBreath(entity_id)
    return breath_comp.SetRecoverTotalAirSupplyTime(time_sec)


def set_block_control_ai(entity_id, is_block=False):
    """
    设置屏蔽生物原生AI

    屏蔽AI后的生物无法行动，不受重力且不会被推动。但是可以受到伤害，也可以被玩家交互（例如马被骑或村民被交易）

    :param entity_id:
    :param is_block: bool 是否保留AI，False为屏蔽
    :return: bool 设置结果
    """
    control_ai_comp = serverApi.GetEngineCompFactory().CreateControlAi(entity_id)
    return control_ai_comp.SetBlockControlAi(is_block)


def trigger_entity_custom_event(entity_id, event_name):
    """
    触发生物自定义事件

    :param entity_id: str 生物Id
    :param event_name: str 事件名称
    :return: bool 设置结果
    """
    entity_event_comp = serverApi.GetEngineCompFactory().CreateEntityEvent(entity_id)
    return entity_event_comp.TriggerCustomEvent(entity_id, event_name)


def set_custom_spawn_rule(biome_type, change, entity_type, probability, min_count, max_count, environment=1, **kwargs):
    """
    设置自定义刷怪

    :param biome_type: biomeType int [BiomeType]枚举
    :param change: int [Change]枚举
    :param entity_type: int [EntityType]枚举
    :param probability: int 生成的权重[1, 10]
    :param min_count: int 最小生成数量[0, 10]
    :param max_count: int 最大生成数量[0, 10]
    :param environment: int 1:生成在表面；2:生成在水里，默认为1
    :param kwargs:
        minBrightness: int 生成该生物时的最小光照[1, 15]，不设置时使用默认值
        maxBrightness: int 生成该生物时的最大光照[1, 15]，不设置时使用默认值
        minHeight: int 生成该生物时最小的海拔高度[0, 256]，不设置时使用默认值
        maxHeight: int 生成该生物时最大的海拔高度[0, 256]，不设置时使用默认值
    :return:bool 设置结果
    """
    mob_spawn_comp = serverApi.GetEngineCompFactory().CreateMobSpawn(level_id)
    return mob_spawn_comp.SpawnCustomModule(
        biome_type, change, entity_type, probability, min_count, max_count, environment, **kwargs)


def set_move_setting(entity_id, pos, speed, max_iteration, callback=None):
    """
    寻路组件

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/02-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-ModAPI/4-%E7%BB%84%E4%BB%B6/2-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E7%BB%84%E4%BB%B6.html#setmovesetting

    :param entity_id:
    :param pos: tuple(float,float,float) 寻路目标位置
    :param speed: float 移动速度
    :param max_iteration: int 寻路算法最大迭代次数 默认200
    :param callback: function 寻路结束回调函数
    :return:
    """
    move_to_comp = serverApi.GetEngineCompFactory().CreateMoveTo(entity_id)
    return move_to_comp.SetMoveSetting(pos, speed, max_iteration, callback)


def set_name(entity_id, name):
    """
    用于生成nameTag，玩家和新版流浪商人暂不支持

    :param entity_id:
    :param name: str 名称
    :return: bool 设置结果
    """
    name_comp = serverApi.GetEngineCompFactory().CreateName(entity_id)
    return name_comp.SetName(name)


def get_name(entity_id):
    """
    获取生物name

    :param entity_id:
    :return: str 生物名称
    """
    name_comp = serverApi.GetEngineCompFactory().CreateName(entity_id)
    return name_comp.GetName()


def set_player_prefix_and_suffix_name(player_id, prefix, prefix_color, suffix, suffix_color):
    """
    设置玩家前缀和后缀名字

    :param player_id:
    :param prefix: str 前缀内容
    :param prefix_color: str 前缀内容颜色描述，可以使用GenerateColor接口传入参数
    :param suffix: str 后缀内容
    :param suffix_color: str 后缀内容颜色描述，可以使用GenerateColor接口传入参数
    :return: bool 设置是否成功
    """
    name_comp = serverApi.GetEngineCompFactory().CreateName(player_id)
    return name_comp.SetPlayerPrefixAndSuffixName(prefix, prefix_color, suffix, suffix_color)


def set_entity_ride(entity_id, player_id):
    """
    驯服可骑乘生物

    驯服信息会被存盘
    
    :param entity_id: str 要驯服的可骑乘生物id
    :param player_id: str 玩家id
    :return: bool 设置结果
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.SetEntityRide(player_id, entity_id)


def set_ride_pos(entity_id, pos):
    """
    设置生物骑乘位置

    :param entity_id: str 可骑乘生物id
    :param pos: tuple(float,float,float) 骑乘时挂接点
    :return: bool 设置结果
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.SetRidePos(entity_id, pos)


def set_can_control_without_saddle(entity_id, is_control=True):
    """
    设置该生物无需装备鞍就可以控制行走跳跃

    :param entity_id: str 可骑乘生物id
    :param is_control: bool 是否控制
    :return: bool 设置结果
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.SetControl(entity_id, is_control)


def set_can_other_player_ride(entity_id, can_ride=False):
    """
    设置其他玩家受否有权限骑乘，True表示每个玩家都能骑乘，False只有驯服者才能骑乘

    :param entity_id: str 可骑乘生物id
    :param can_ride: bool 是否控制
    :return: bool 设置结果
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.SetCanOtherPlayerRide(entity_id, can_ride)


def set_show_ride_ui(entity_id, is_show_ui=False):
    """
    设置是否显示马匹的UI界面，建议不显示

    :param entity_id: str 可骑乘生物id
    :param is_show_ui: bool 是否显示UI
    :return: bool 设置结果
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.SetShowRideUI(entity_id, is_show_ui)


def is_entity_riding(entity_id):
    """
    检查玩家是否骑乘

    :param entity_id:
    :return: bool 是否骑乘
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.IsEntityRiding()


def get_entity_mount(entity_id):
    """
    获取玩家的直接骑乘对象

    :param entity_id:
    :return: str 玩家直接骑乘对象的唯一ID，假如玩家没有骑乘则返回“-1”
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.GetEntityRider()


def stop_entity_riding(entity_id):
    """
    强制玩家下坐骑

    :param entity_id:
    :return: bool 当玩家当前正在骑乘并成功下坐骑返回True，否则返回False
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.StopEntityRiding()


def set_ride_entity(entity_id, mounts_id):
    """
    设置实体骑乘生物

    通常需要配合SetEntityRide、SetControl一起使用，需要被骑乘生物json中骑乘组件支持骑车者的生物类型

    当被控制的entity有多个位置时且开发者想要添加多个玩家时，第一个被添加的玩家会被引擎默认设置为控制者

    1.18 新增 新增实体骑乘生物接口

    :param entity_id: str 被骑乘生物id
    :param mounts_id:
    :return:
    """
    ride_comp = serverApi.GetEngineCompFactory().CreateRide(entity_id)
    return ride_comp.SetPlayerRideEntity(entity_id, mounts_id)


def get_owner_id(entity_id):
    """
    获取驯服生物的主人id

    :param entity_id:
    :return: str 主人id，不存在时返回None
    """
    tame_comp = serverApi.GetEngineCompFactory().CreateTame(entity_id)
    return tame_comp.GetOwnerId()


def set_owner_id(player_id, tamed_id):
    """
    设置生物驯服，需要配合 entityEvent组件使用。该类驯服不包含骑乘功能。

    :param player_id: str 驯服玩家Id
    :param tamed_id: str 被驯服的生物Id
    :return: bool 设置结果
    """
    tame_comp = serverApi.GetEngineCompFactory().CreateTame(tamed_id)
    return tame_comp.SetEntityTamed(player_id, tamed_id)
