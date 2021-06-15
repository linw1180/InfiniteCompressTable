# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()
local_player = clientApi.GetLocalPlayerId()


def get_fov():
    """
    获取视野大小
    
    :return: float 即视频设置中的视野，单位为角度
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetFov()


def set_fov(fov):
    """
    设置视野大小

    :param fov: float 单位为角度
    :return: bool 设置是否成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.SetFov(fov)


def lock_camera(lock_pos, lock_rot):
    """
    锁定摄像机

    锁定摄像机时只是锁定画面视角，玩家仍然可以移动

    :param lock_pos: tuple(float,float,float) 世界坐标
    :param lock_rot: tuple(float,float) 摄像机的角度（俯仰角及偏航角）
    :return: bool 设置是否成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.LockCamera(lock_pos, lock_rot)


def un_lock_camera():
    """
    解除摄像机锁定

    :return: bool 设置是否成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.UnLockCamera()


def pick_facing():
    """
    获取准星选中的实体或者方块
        http://mc.163.com/dev/mcmanual/mc-dev/mcdocs/1-ModAPI/%E6%8E%A5%E5%8F%A3/%E6%8E%A7%E5%88%B6/PickFacing.html#pickfacing

    :return: dict 选中目标的数据
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.PickFacing()


def get_fp_height():
    """
    获取本地玩家当前状态下，第一人称视角时的摄像机高度偏移量。游泳时，滑翔时以及普通状态下会有所不同

    :return: float 高度偏移量
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetFpHeight()


def get_chosen_entity():
    """
    获取屏幕点击位置的实体id，通常与GetEntityByCoordEvent配合使用

    目前只有在第一人称视角才能准确获取

    :return: str 实体id
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetChosenEntity()


def get_chosen():
    """
    获取屏幕点击位置的实体或方块信息，通常与GetEntityByCoordEvent配合使用

    目前只有在第一人称视角才能准确获取

    :return: dict 选中目标的数据，详见[PickFacing]的备注
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetChosen()


def depart_camera():
    """
    分离玩家与摄像机

    分离之后，可以看到玩家四周

    :return:
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.DepartCamera()


def un_depart_camera():
    """
    绑定玩家与摄像机

    绑定之后，只能看到玩家背部

    :return:
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.UnDepartCamera()


def set_camera_bind_actor_id(target_id):
    """
    将摄像机绑定到目标玩家身上（需要先DepartCamera，调用者与targetId必须在同一个dimension，同时需要在加载范围之内）

    调用该接口时，脚本层需要处理绑定的目标实体不存在的情况（包括实体不存在或者死亡的情况）

    :param target_id: str 目标玩家id
    :return: bool 是否设置成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.SetCameraBindActorId(target_id)


def reset_camera_bind_actor_id():
    """
    重置将摄像机绑定到目标玩家身上

    :return: bool 是否设置成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.ResetCameraBindActorId()


def get_camera_forward():
    """
    返回相机向前的方向

    :return: tuple(float,float,float) 向前的方向
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetForward()


def get_camera_pos():
    """
    返回相机中心

    :return: tuple(float,float,float) 相机中心位置
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetPosition()


def set_camera_pos(pos):
    """
    设置相机中心的位置

    :param pos: tuple(float,float,float) 位置
    :return: bool 是否设置成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.SetCameraPos(pos)


def set_camera_rot(rot):
    """
    设定相机转向

    :param rot: tuple(float,float) 转向
    :return: bool 是否设置成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.SetCameraRot(rot)


def get_camera_rot():
    """
    获取相机转向

    :return: tuple(float,float) 转向
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetCameraRot()


def set_camera_offset(offset):
    """
    设置摄像机偏移量

    :param offset: tuple(float,float,float) 偏移量
    :return: bool 是否设置成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.SetCameraOffset(offset)


def get_camera_offset():
    """
    获取摄像机偏移量

    :return: tuple(float,float,float) 偏移量
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetCameraOffset()


def set_camera_anchor(offset):
    """
    设置相机锚点,暂时只支持高度,其他维度无效

    :param offset: tuple(float,float,float) 锚点偏移量
    :return: bool 是否设置成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.SetCameraAnchor(offset)


def get_camera_anchor():
    """
    获取相机锚点

    :return: tuple(float,float,float) 锚点偏移量
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetCameraAnchor()


def lock_mod_camera_pitch(lock):
    """
    锁定摄像机上下角度（第三人称下生效，锁定后不能上下调整视角）

    :param lock: bool True:锁定 False:解锁
    :return: bool 是否设置成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.LockModCameraPitch(1 if lock else 0)


def is_mod_camera_lock_pitch():
    """
    是否锁定摄像机上下角度

    :return: bool 是否锁定
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.IsModCameraLockPitch()


def get_camera_pitch_limit():
    """
    获取摄像机上下角度限制值

    :return: tuple(float,float) 上下角度限制值
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.GetCameraPitchLimit()


def set_camera_pitch_limit(limit):
    """
    设置摄像机上下角度限制值，默认是（-90，90）

    :param limit: tuple(float,float) 上下角度限制值
    :return: bool 是否成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.SetCameraPitchLimit(limit)


def lock_mod_camera_yaw(lock):
    """
    锁定摄像机左右角度（第三人称下生效，锁定后不能通过鼠标左右调整视角）

    :param lock: bool True:锁定 False:解锁
    :return: bool 是否设置成功
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.LockModCameraYaw(1 if lock else 0)


def is_mod_camera_lock_yaw():
    """
    是否锁定摄像机左右角度

    :return: bool 是否锁定
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.IsModCameraLockYaw()


def set_speed_fov_lock(lock):
    """
    是否锁定相机视野fov，锁定后不随速度变化而变化

    :param lock: bool 是否锁定
    :return:
    """
    camera_comp = clientApi.GetEngineCompFactory().CreateCamera(level_id)
    return camera_comp.SetSpeedFovLock(lock)


def enable_player_hit_block_detection(entity_id, precision):
    """
    开启碰撞方块的检测，开启后碰撞时会触发OnPlayerHitBlockClientEvent事件
    
    注：该碰撞检测会屏蔽草、空气、火、高草四种方块

    :param entity_id:
    :param precision: float 碰撞检测精度，参数需要在区间[0, 1)
    :return: bool 是否设置成功
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.OpenPlayerHitBlockDetection(precision)


def disable_player_hit_block_detection(entity_id):
    """
    关闭碰撞方块的检测，关闭后将不会触发OnPlayerHitBlockClientEvent事件

    :param entity_id:
    :return: bool 是否设置成功
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.ClosePlayerHitBlockDetection()


def enable_player_hit_mob_detection(entity_id):
    """
    开启碰撞生物的检测，开启后碰撞时会触发OnPlayerHitMobClientEvent事件

    :param entity_id:
    :return: bool 是否开启成功
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.OpenPlayerHitMobDetection()


def disable_player_hit_mob_detection(entity_id):
    """
    关闭碰撞生物的检测，关闭后将不会触发OnPlayerHitMobClientEvent事件

    :param entity_id:
    :return: bool 是否关闭成功
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.ClosePlayerHitMobDetection()


def is_gliding(entity_id):
    """
    获取玩家是否鞘翅飞行

    :param entity_id:
    :return: bool 是否鞘翅飞行
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.isGliding()


def is_swimming(entity_id):
    """
    获取玩家是否在游泳

    :param entity_id:
    :return: bool 是否游泳
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.isSwimming()


def is_riding(entity_id):
    """
    获取玩家是否在骑乘

    :param entity_id:
    :return: bool 是否骑乘
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.isRiding()


def is_sneaking(entity_id):
    """
    获取玩家是否在潜行

    :param entity_id:
    :return: bool 是否潜行
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.isSneaking()


def set_sneaking():
    """
    设置是否潜行，只能设置本地玩家（只适用于移动端）

    :return: bool 设置是否成功
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(local_player)
    return player_comp.setSneaking()


def is_sprinting(entity_id):
    """
    获取玩家是否在疾跑

    :param entity_id:
    :return: bool 是否在疾跑
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.isSprinting()


def set_sprinting():
    """
    设置是否疾跑，只能设置本地玩家v（只适用于移动端）

    :return:
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(local_player)
    return player_comp.setSprinting()


def is_in_water(entity_id):
    """
    获取玩家是否在水中

    :param entity_id:
    :return: bool 是否在水中
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.isInWater()


def is_moving(entity_id):
    """
    获取玩家是否在行走

    :param entity_id:
    :return: bool 是否在行走
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(entity_id)
    return player_comp.isMoving()


def set_moving():
    """
    设置是否行走，只能设置本地玩家（只适用于移动端）

    :return:
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(local_player)
    return player_comp.setMoving()


def get_local_player_uid():
    """
    获取本地玩家的uid

    不是客户端线程或者没有经过登录认证获取的uid为None。在当前机器上调用改接口获取的值为固定值，不依赖创建的player

    :return:
    """
    player_comp = clientApi.GetEngineCompFactory().CreatePlayer(local_player)
    return player_comp.getUid()


def play_tp_animation(player_id, anim):
    """
    第三人称视角播放玩家通用动作

    支持的动作包括：sneaking、sneaking_inverted、swim、sleeping、holding_left、holding_right、crossbow_hold、crossbow_equipped、bow_equipped、upside_down、tp_attack

    :param player_id:
    :param anim:
    :return:
    """
    player_anim_comp = clientApi.GetEngineCompFactory().CreatePlayerAnim(player_id)
    return player_anim_comp.PlayTpAnimation(anim)


def stop_animation(player_id, anim):
    """
    停止播放玩家通用动作

    :param player_id:
    :param anim:
    :return:
    """
    player_anim_comp = clientApi.GetEngineCompFactory().CreatePlayerAnim(player_id)
    return player_anim_comp.StopAnimation(anim)
