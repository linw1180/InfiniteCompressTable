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


def get_playing_anim_list(entity_id, model_id):
    """
    获取指定的骨骼模型中正处于播放状态的骨骼动画名称列表

    1.23 调整 由于现在骨骼模型支持同时播放多个动画，所以接口由GetPlayingAnim改为GetPlayingAnimList

    :param entity_id:
    :param model_id: int 骨骼模型Id
    :return: list(str) 骨骼动画名称列表
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.GetPlayingAnimList(model_id)


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

    1.23 调整 挂接的模型不再会与实体模型播放相同的动作，现在可以对挂接模型播放单独的骨骼动画。

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

    1.23 调整 挂接的模型不再会与实体模型播放相同的动作，现在可以对挂接模型播放单独的骨骼动画。

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
    import warnings
    warnings.warn("1.21 骨骼模型创建时默认为False，不再需要设置。但是对于旧版特效，仍然可以设置为True来适配。", DeprecationWarning)

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
    :return: int 创建成功返回 model_id，创建失败返回 0
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


def model_play_ani(entity_id, model_id, anim, loop=False, is_blended=False, layer=0):
    """
    纯骨骼播放动作

    支持骨骼动画混合，可参考SetAnimationBoneMask接口以及RegisterAnim1DControlParam接口说明。

    在动画的层级相同的情况下，动画的优先度播放顺序则首先按照：
        1.是否与需要其他动画进行混合。
        2.是否率先播放 这两个因素来先后决定。

    例如，我们首先对动画A，动画B使用接口RegisterAnim1DControlParam注册1D线性混合参数alpha， 然后对动画A和动画C使用接口RegisterAnim1DControlParam注册线性混合参数beta。
    接着，先后播放动画A, 动画C，动画B，动画D。
    这时，由于动画A，动画C具有混合需要，并且率先播放，因此骨骼模型会率先播放动画A和动画C的混合动画（注意，1D线性混合参数的初始值为0，因此此时混合动画的表现还是动画A），如果此时再暂停动画C，则会播放动画A与动画B的混合动画。接着暂停动画B，则会播放动画A，最后再暂停动画A，则才会播放动画D。

    1.23 调整 新增动画混合功能, 新增设置动画层级参数，增加是否播放成功的返回值。

    :param entity_id:
    :param model_id: int 要设置的modelId
    :param anim: str 要设置的动画名称
    :param loop: bool 是否循环播放，默认为 False
    :param is_blended: bool 播放时是与当前动画混合还是中止当前动画的播放，默认False，即中止当前动画播放。设置为True时，将允许即将播放的动画进行混合。注意，动画混合仅在相同层级的动画之间进行。若当前播放的动画与即将播放的动画层级不一样，则isBlended参数无效。
    :param layer: 设置骨骼动画的层级，范围为0~255，默认为0。注意，如果播放的动画已经存在，则会将原有的动画层级覆盖。动画层级越大，则优先度越高，骨骼模型的骨骼优先播放优先度最高的动画。
    :return: bool 是否成功设置
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.ModelPlayAni(model_id, anim, loop, is_blended, layer)


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


def set_common_hurt_color(entity_id, show=False):
    """
    设置挂接骨骼模型的实体是否显示通用的受伤变红效果

    引擎默认打开该选项，需要改变受伤效果可以关闭之后再进行定制

    :param entity_id:
    :param show: bool 是否显示
    :return: bool 设置结果
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.ShowCommonHurtColor(show)


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


def set_show_arm_model(entity_id, model_id, show):
    """
    设置使用骨骼模型后切换至第一人称时是否显示手部模型

    需要先为骨骼模型定义arm_model，arm_model的定义可参考demo示例-AwesomeMod中的resourcePack/models/netease_models.json中的大天狗模型定义

    :param entity_id:
    :param model_id: int 模型id
    :param show: bool 是否显示
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetShowArmModel(model_id, show)


def set_extra_uniform_value(entity_id, model_id, uniform_index, vec4data):
    """
    设置shader中特定Uniform的值

    若在游戏运行过程中修改shader文件，需要调用clientApi.ReloadAllShaders()或者重启游戏才会生效

    :param entity_id:
    :param model_id: int 要设置的modelId
    :param uniform_index: int 要设置的uniform下标，目前支持4个，范围为1到4。分别对应Shader中的EXTRA_VECTOR1,EXTRA_VECTOR2,EXTRA_VECTOR3,EXTRA_VECTOR4
    :param vec4data: tuple(float,float,float,float)	要设置的vec4的值。初始值为(0.0, 0.0, 0.0, 0.0)
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetExtraUniformValue(model_id, uniform_index, vec4data)


def model_stop_anim(entity_id, model_id, anim):
    """
    暂停指定的骨骼动画

    :param entity_id:
    :param model_id: int 需要设置的模型id，包括实体模型以及自由模型
    :param anim: str 动画名称
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.ModelStopAni(model_id, anim)


def set_animation_bone_mask(entity_id, model_id, anim, bone_names_list, enable, apply_to_child=True):
    """
    设置是否屏蔽动画中指定的骨骼的动画，若开启骨骼屏蔽后，该骨骼将不再播放该动画中的动作。

    通过屏蔽指定骨骼的动画可实现同一个骨骼模型同时在不同骨骼上播放不同的动作动画，从而实现快捷的动作融合。

    在使用该接口屏蔽上下半身的动画时，如果骨骼当中存在root骨骼，并且root骨骼的子骨骼包含上下半身的骨骼的话，root骨骼往往会控制整体骨骼模型的移动，要注意root骨骼对其他骨骼的影响。

    :param entity_id:
    :param model_id: int 需要设置的模型id，包括实体模型以及自由模型
    :param anim: str 动画名称
    :param bone_names_list: list(str)	骨骼名称列表
    :param enable: bool 是否启用该骨骼的动画。True为不屏蔽，启动该骨骼的动画。False为屏蔽，不启动该骨骼的动画。
    :param apply_to_child: bool True为对该骨骼及其子骨骼生效，False为仅对该骨骼生效，默认为True
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetAnimationBoneMask(model_id, anim, bone_names_list, enable, apply_to_child)


def set_animation_all_bone_mask(entity_id, model_id, anim, ignore_bones_list, enable, apply_to_child=True):
    """
    设置是否屏蔽动画中所有骨骼的动画，若开启骨骼屏蔽后，该骨骼将不再播放该动画中的动作。

    该接口会对该动画中所有骨骼生效，可通过参数ignoreBoneList来指定不受影响的骨骼名称。

    通过屏蔽指定骨骼的动画可实现同一个骨骼模型同时在不同骨骼上播放不同的动作动画，从而实现快捷的动作融合。

    在使用该接口屏蔽上下半身的动画时，如果骨骼当中存在root骨骼，并且root骨骼的子骨骼包含上下半身的骨骼的话，root骨骼往往会控制整体骨骼模型的移动，要注意root骨骼对其他骨骼的影响。

    :param entity_id:
    :param model_id: int 需要设置的模型id，包括实体模型以及自由模型
    :param anim: str 动画名称
    :param ignore_bones_list: list(str) 忽视的骨骼名称列表。在这个列表中的骨骼将不会被影响。输入空列表时则对所有骨骼执行这次设置。
    :param enable: bool 是否启用该骨骼的动画。True为不屏蔽，启动该骨骼的动画。False为屏蔽，不启动该骨骼的动画。
    :param apply_to_child: bool True为对ignoreBoneList中的骨骼的子骨骼也生效，False为仅对ignoreBoneList中的骨骼生效，默认为True。若ignoreBoneList为空列表，则applyToChild无效果。
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetAnimationAllBoneMask(model_id, anim, ignore_bones_list, enable, apply_to_child)


def cancel_all_bone_mask(entity_id, model_id, anim):
    """
    取消动画中的所有骨骼屏蔽。

    :param entity_id:
    :param model_id: int 需要设置的模型id，包括实体模型以及自由模型
    :param anim: str 动画名称
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.CancelAllBoneMask(model_id, anim)


def set_anim_layer(entity_id, model_id, anim, layer):
    """
    设置骨骼动画的层级，动画层级越大，则优先度越高，骨骼模型的骨骼优先播放优先度最高的动画，相同层级的动画则优先播放率先播放的动画。

    注意，设置层级相同的情况下不会改变当前的优先播放序列。举个例子：
        当前存在动画A及动画B，动画A的层级为1，动画B的层级为0，此时骨骼模型播放的动画为动画A。
        如果将动画A的层级设置为0，即动画A及动画B的层级相同，则当前仍然会播放动画A，因为层级相同的情况下不会改变目前的优先播放序列。

    要想让骨骼模型播放动画B，则需要动画B的层级比动画A的层级高。

    :param entity_id:
    :param model_id: int 需要设置的模型id，包括实体模型以及自由模型
    :param anim: str 动画名称
    :param layer: int 动画层级， 正整数，范围为0~255
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetAnimLayer(model_id, anim, layer)


def register_anim_1d_control_param(entity_id, model_id, anim1, anim2, param_name):
    """
    当同时播放多个骨骼动画时，新建用于控制动画进行1D线性混合的参数。

    目前线性混合仅支持对两个动画进行混合。新建的参数值范围为[0,1]。指定的骨骼将会按照这个参数的值对两个动画进行线性混合。

    * 注意，如果对某个骨骼使用了骨骼屏蔽，则这个1D线性混合将对该骨骼不会生效。另外，如果在使用该接口时新建一个已经存在的参数名称，则会将原来的参数覆盖。
    * 在动画的层级相同的情况下，动画的优先度播放顺序则首先按照：1.是否与需要其他动画进行混合。2.是否率先播放 这两个因素来先后决定。例如，我们首先对动画A，动画B使用接口RegisterAnim1DControlParam注册1D线性混合参数alpha， 然后对动画A和动画C使用接口RegisterAnim1DControlParam注册线性混合参数beta。接着，先后播放动画A, 动画C，动画B，动画D。这时，由于动画A，动画C具有混合需要，并且率先播放，因此骨骼模型会率先播放动画A和动画C的混合动画（注意，由于1D线性混合参数的初始值为0，因此此时混合动画的表现还是动画A），如果此时再暂停动画C，则会播放动画A与动画B的混合动画。接着暂停动画B，则会播放动画A，最后再暂停动画A，则才会播放动画D。
    * 另一种需要注意的情况：如果我们首先对动画A，动画B使用接口RegisterAnim1DControlParam注册1D线性混合参数alpha， 然后对动画A和动画C使用接口RegisterAnim1DControlParam注册线性混合参数beta。接着，先后播放动画A, 动画B，动画C。这时，我们调用SetAnim1DControlParam接口设置参数beta的值为0.5。此时模型仍然是播放动画A，这是由于动画A和动画B具有混合需求并且率先播放的，即率先凑齐了参数混合两个动画，因此此时模型实际上是在进行动画A和动画B的混合，但是由于alpha的值为0，因此模型还是表现为动画A，如果此时再用SetAnim1DControlParam接口设置参数alpha的值为0.5，则能够看到动画A和动画B的混合动画了。

    :param entity_id:
    :param model_id: int 骨需要设置的模型id，包括实体模型以及自由模型。
    :param anim1: str 混合的第一个动画名称，当1D参数的值为0时指定的骨骼仅播放这个动画。
    :param anim2: str 混合的第二个动画名称，当1D参数的值为1时指定的骨骼仅播放这个动画。
    :param param_name: str 自定义的1D参数名称。该参数新建后的初始值为0。
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.RegisterAnim1DControlParam(model_id, anim1, anim2, param_name)


def set_anim_1d_control_param(entity_id, model_id, param_name, value):
    """
    新建动画的1D控制参数后，使用该接口对相应的参数进行控制。

    注意，如果对某个骨骼使用了骨骼屏蔽，则这个1D线性混合将对该骨骼不会生效。

    :param entity_id:
    :param model_id: int 需要设置的模型id，包括实体模型以及自由模型。
    :param param_name: str 使用接口RegisterAnim1DControlParam所新建的自定义1D参数名称。该参数新建后的初始值为0。
    :param value: float 参数的值，范围为[0,1]。当1D参数的值为0时仅播放接口RegisterAnim1DControlParam中的leftAniName参数指定的动画，当1D参数的值为1时仅播放接口RegisterAnim1DControlParam中的rightAniName参数指定的动画
    :return: bool 设置是否成功
    """
    model_comp = clientApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetAnim1DControlParam(model_id, param_name, value)
