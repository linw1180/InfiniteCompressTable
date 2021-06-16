# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi


def set_model(entity_id, model_name):
    """
    替换实体的骨骼模型
    
    使用客户端组件更换模型不会同步及存盘，仅是纯客户端表现，如需要同步及存盘，请使用服务器的model组件
    
    要恢复原版模型请使用ResetModel接口
    
    :param entity_id: 
    :param model_name: str 骨骼模型的名称
    :return: int 替换的骨骼模型实例的id。失败返回-1
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetModel(model_name)


def get_model_id(entity_id):
    """
    获取骨骼模型的Id，主要用于特效绑定骨骼模型
    
    :param entity_id: 
    :return: int 当前骨骼模型实例的id
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.GetModelId()


def reset_model(entity_id):
    """
    恢复实体为原版模型
    
    :param entity_id: 
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.ResetModel()


def play_anim(entity_id, ani_name, is_loop):
    """
    播放骨骼动画

    :param entity_id:
    :param ani_name: str 动画名称
    :param is_loop: bool 是否循环播放
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.PlayAnim(ani_name, is_loop)


def get_playing_anim(entity_id):
    """
    获取当前播放的骨骼动画名称

    :param entity_id:
    :return: str 骨骼动画名称
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.GetPlayingAnim()


def get_anim_length(entity_id, ani_name):
    """
    获取某个骨骼动画的长度，单位为秒

    :param entity_id:
    :param ani_name: str 骨骼动画名称
    :return: float 骨骼动画长度
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.GetAnimLength(ani_name)


def set_anim_speed(entity_id, ani_name, speed):
    """
    设置某个骨骼动画的播放速度

    :param entity_id:
    :param ani_name: str 骨骼动画名称
    :param speed: float 速度倍率
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetAnimSpeed(ani_name, speed)


def bind_model_to_model(entity_id, bone_name, model_name):
    """
    在骨骼模型上挂接其他骨骼模型

    :param entity_id:
    :param bone_name: str 挂接的骨骼名称
    :param model_name: str 要挂接的骨骼模型名称
    :return: int 挂到骨骼上的骨骼模型的Id，失败返回-1
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.BindModelToModel(bone_name, model_name)


def un_bind_model_to_model(entity_id, model_id):
    """
    取消骨骼模型上挂接的某个骨骼模型。取消挂接后，这个modelId的模型便会销毁，无法再使用，如果是临时隐藏可以使用HideModel

    :param entity_id:
    :param model_id: int 要取消挂接的骨骼模型的id
    :return: bool 挂到骨骼上的骨骼模型的Id，失败返回-1 FIXME ?
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.UnBindModelToModel(model_id)


def bind_model_to_entity(entity_id, bone_name, model_name):
    """
    实体替换骨骼模型后，再往上其他挂接骨骼模型。对实体播骨骼动作时，其上面挂接的模型也会播相同的动作。

    :param entity_id:
    :param bone_name: str 挂接的骨骼名称
    :param model_name: str 要挂接的骨骼模型名称
    :return: int 挂到骨骼上的骨骼模型的Id，失败返回-1
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.BindModelToEntity(bone_name, model_name)


def un_bind_model_to_entity(entity_id, model_id):
    """
    取消实体上挂接的某个骨骼模型。取消挂接后，这个modelId的模型便会销毁，无法再使用，如果是临时隐藏可以使用HideModel

    :param entity_id:
    :param model_id: int 要取消挂接的骨骼模型的id
    :return: bool 挂到骨骼上的骨骼模型的Id，失败返回-1
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.UnBindModelToEntity(model_id)


def get_all_bind_model_to_entity(entity_id, bone_name):
    """
    获取实体上某个骨骼上挂接的所有骨骼模型的id

    :param entity_id:
    :param bone_name: str 要获取的骨骼名称
    :return: list(int) 骨骼模型的id的列表
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.GetAllBindModelToEntity(bone_name)


def play_body_anim(entity_id, body_ani_name, loop=False):
    """
    上下半身分离时，对上半身播放动画

    骨骼模型需要有一根名为“up”的骨骼，并且上半身的其他骨骼都以up为父骨骼

    :param entity_id:
    :param body_ani_name: str 骨骼动画名称
    :param loop: bool 是否循环播放
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.PlayBodyAnim(body_ani_name, loop)


def stop_body_anim(entity_id):
    """
    停止上半身动画

    :param entity_id:
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.StopBodyAnim()


def play_leg_anim(entity_id, leg_ani_name, loop):
    """
    上下半身分离时，对下半身播放动画

    骨骼模型需要有一根名为“down”的骨骼，并且下半身的其他骨骼都以down为父骨骼

    :param entity_id:
    :param leg_ani_name: str 骨骼动画名称
    :param loop: bool 是否循环播放
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.PlayLegAnim(leg_ani_name, loop)


def stop_leg_anim(entity_id):
    """
    停止下半身动画

    :param entity_id:
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.StopLegAnim()


def set_model_texture(entity_id, texture):
    """
    替换骨骼模型的贴图

    :param entity_id:
    :param texture: str 贴图路径，以textures/models为当前路径的相对路径
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetTexture(texture)


def set_skin(entity_id, skin):
    """
    更换原版自定义皮肤

    会覆盖原有皮肤（包括4d皮肤）。但会被骨骼模型覆盖

    :param entity_id:
    :param skin: str 贴图路径，以textures/models为当前路径的相对路径
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetSkin(skin)


def set_legacy_bind_rot(entity_id, enable=False):
    """
    用于修复特效挂接到骨骼时的方向

    在挂接特效前调用即可

    :param entity_id:
    :param enable: bool 设置为False时，可以使特效与骨骼方向一致
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetLegacyBindRot(enable)


def get_bone_world_pos(entity_id, bone_name):
    """
    获取骨骼的坐标

    :param entity_id:
    :param bone_name: 获取骨骼的坐标
    :return: tuple(int,int,int) 位置坐标
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.GetBoneWorldPos(bone_name)


def get_entity_bone_world_pos(entity_id, bone_name):
    """
    获取换了骨骼模型的实体的骨骼坐标

    :param entity_id: str 实体id
    :param bone_name: str 骨骼名称
    :return: tuple(int,int,int) 位置坐标
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.GetEntityBoneWorldPos(entity_id, bone_name)


def create_free_model(entity_id, model_name):
    """
    创建自由的模型（无需绑定Entity）

    :param entity_id:
    :param model_name: str 模型名称
    :return: int 创建成功返回 modelId，创建失败返回 0
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.CreateFreeModel(model_name)


def remove_free_model(entity_id, model_id):
    """
    移除自由模型

    :param entity_id:
    :param model_id: int 要移除的modelId
    :return: bool 是否成功移除
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.RemoveFreeModel(model_id)


def set_free_model_pos(entity_id, model_id, x, y, z):
    """
    设置自由模型的位置

    :param entity_id:
    :param model_id: int 要设置的modelId
    :param x: float 要设置的位置X轴参数
    :param y: float 要设置的位置Y轴参数
    :param z: float 要设置的位置Z轴参数
    :return: bool 是否成功设置
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetFreeModelPos(model_id, x, y, z)


def set_free_model_rot(entity_id, model_id, x, y, z):
    """
    设置自由模型的方向

    :param entity_id:
    :param model_id: int 要设置的modelId
    :param x: float 沿X方向的旋转参数
    :param y: float 沿Y方向的旋转参数
    :param z: float 沿Z方向的旋转参数
    :return: bool 是否成功设置
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetFreeModelRot(model_id, x, y, z)


def set_free_model_scale(entity_id, model_id, x, y, z):
    """
    设置自由模型的大小

    :param entity_id:
    :param model_id: int 要设置的modelId
    :param x: float 沿X方向的比例因子
    :param y: float 沿Y方向的比例因子
    :param z: float 沿Z方向的比例因子
    :return: bool 是否成功设置
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetFreeModelScale(model_id, x, y, z)


def model_play_ani(entity_id, model_id, ani_name, loop=False):
    """
    纯骨骼播放动作

    :param entity_id:
    :param model_id: int 要设置的modelId
    :param ani_name: str 要设置的动画名称
    :param loop: bool 是否循环播放，默认为 False
    :return:
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    model_comp.ModelPlayAni(model_id, ani_name, loop)


def hide_model(entity_id, model_id):
    """
    隐藏纯模型

    :param entity_id:
    :param model_id: int 要隐藏的modelId
    :return:
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    model_comp.HideModel(model_id)


def show_model(entity_id, model_id):
    """
    显示纯模型

    :param entity_id:
    :param model_id: int 要显示的modelId
    :return:
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    model_comp.ShowModel(model_id)


def set_free_model_bounding_box(entity_id, model_id, bottom, top):
    """
    设置模型包围盒
    
    模型包围盒用于判断渲染剔除：判断一个模型要不要渲染，要看它在不在视野范围内，也就是看游戏摄像机的视锥体（摄像机拍到的范围）和这个包围盒有没有交集。有则说明在视野范围内，反之则不在视野范围内。进而可以剔除掉该模型，不进行渲染。
    
    :param entity_id: 
    :param model_id: int 要设置的modelId
    :param bottom: tuple(float,float,float) 包围盒最小点
    :param top: tuple(float,float,float) 包围盒最大点
    :return: bool 成功返回True，失败返回False
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetFreeModelBoundingBox(model_id, bottom, top)


def bind_entity_to_entity(entity_id, bind_entity_id):
    """
    绑定骨骼模型跟随其他entity,摄像机也跟随其他entity

    本接口只实现视觉效果，本质上实体还是在原地，因此需要调用接口设置实体的位置到其他entity的位置上，否则当实体本身不在摄像机范围内的时候就会不进行渲染了。

    :param entity_id:
    :param bind_entity_id: str 绑定跟随的实体Id
    :return: bool False表示失败，True表示成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.BindEntityToEntity(bind_entity_id)


def reset_bind_entity(entity_id):
    """
    取消目标entity的绑定实体，取消后不再跟随任何其他entity

    :param entity_id:
    :return: bool False表示失败，True表示成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.ResetBindEntity()


def set_model_offset(entity_id, offset):
    """
    模型增加偏移量

    :param entity_id:
    :param offset: tuple(float,float,float) 偏移向量
    :return:
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetModelOffset(offset)


def set_model_perspective_effect(entity_id, is_perspective, color):
    """
    设置模型透视效果。注：只对自定义骨骼模型生效

    :param entity_id: 
    :param is_perspective: bool 是否显示透视颜色
    :param color: tuple(float,float,float,float) 透视颜色的RGBA值，范围0-1
    :return: 
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetModelPerspectiveEffect(is_perspective, color)


def set_entity_opacity(entity_id, opacity):
    """
    设置生物模型的透明度

    :param entity_id:
    :param opacity: float 透明度值，取值范围为[0, 1]，值越小越透明
    :return:
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetEntityOpacity(opacity)


def bind_model_sfx(model_id, data):
    """
    绑定序列帧动画到骨骼模型上

    :param model_id:
    :param data: dict 序列帧动画参数
        'path': 'textures/particle/2020s3/ty_04',
        'bone': 'Bone002',
        'offset': (0, 0, 0),
        'rotation': (0, 0, 0),
        'fps': 33,
        'loop': True,
        'scale': (1, 1, 1),
    :return: int 序列帧动画参数
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(model_id)
    return model_comp.BindModelSfx(data)
