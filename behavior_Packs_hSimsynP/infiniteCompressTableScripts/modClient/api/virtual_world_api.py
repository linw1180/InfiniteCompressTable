# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
from mod.common.minecraftEnum import TimeEaseType, VirtualWorldObjectType

level_id = clientApi.GetLevelId()


def virtual_world_create():
    # type: () -> bool
    """
    创建虚拟世界，虚拟世界只允许存在一个，已经存在虚拟世界的情况下再调用此方法则无效
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.VirtualWorldCreate()


def virtual_world_destroy():
    # type: () -> bool
    """
    销毁虚拟世界
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.VirtualWorldDestroy()


def virtual_world_toggle_visibility(visible=True):
    # type: (bool) -> bool
    """
    设置虚拟世界是否显示
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.VirtualWorldToggleVisibility(visible)


def virtual_world_set_colliders_visible(visible=True):
    # type: (bool) -> bool
    """
    设置虚拟世界中模型的包围盒是否显示,主要用于调试,默认为不显示

    建议在需要频繁在主世界跟虚拟世界切换的时候使用该方法，若后续长时间不需要使用虚拟世界，建议调用VirtualWorldDestroy进行销毁释放资源
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.VirtualWorldSetCollidersVisible(visible)


def virtual_world_set_sky_texture(texture_path, mode):
    """
    设置虚拟世界中天空的贴图

    :param texture_path: str 贴图路径
    :param mode: int 拉伸模式，0或1。0代表贴图宽高都拉伸至全屏，可能造成贴图变形；1代表高度拉伸至全屏，宽度按贴图原宽高比进行相应缩放，能保持贴图不被拉伸，但会造成贴图超出屏幕或不完全铺满屏幕。
    :return: bool 是否设置成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.VirtualWorldSetSkyTexture(texture_path, mode)


def virtual_world_set_sky_bg_color(color):
    """
    设置虚拟世界中天空背景的颜色

    :param color: tuple(float,float,float) 颜色的r,g,b值，均为0.0到1.0的浮点值
    :return: bool 是否设置成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(clientApi.GetLevelId())
    return virtual_world_comp.VirtualWorldSetSkyBgColor(color)


def camera_set_pos(pos):
    # type: (tuple[float,float,float]) -> bool
    """
    设置相机位置
    坐标值(x,y,z)初始默认为 (0,0,0)，且朝向z轴负方向
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraSetPos(pos)


def camera_get_pos():
    # type: () -> tuple[float,float,float]
    """
    返回相机位置
    坐标值(x, y, z), 若虚拟世界没有创建则返回None
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraGetPos()


def camera_set_fov(fov):
    # type: (float) -> bool
    """
    设置相机视野大小
    视野大小( field of view )，单位为角度, 范围为[30, 110]，若fov小于30则设置为30，若fov大于110，则设置为110。不修改时默认为45。
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraSetFov(fov)


def camera_get_fov():
    # type: () -> float
    """
    获取相机视野大小
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraGetFov()


def camera_set_zoom(zoom):
    # type: (float) -> bool
    """
    设置相机缩放
    缩放值, 范围为[0.1,100.0]，小于0.1则设置为0.1，大于100则设置为100，不修改时默认为1。
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraSetZoom(zoom)


def camera_look_at(target_pos, up_vector):
    # type: (tuple[float,float,float], tuple[float,float,float]) -> bool
    """
    修改相机朝向
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraLookAt(target_pos, up_vector)


def camera_move_to(pos, target_pos, up_vector, zoom, time, ease=TimeEaseType.linear):
    # type: (tuple[float,float,float], tuple[float,float,float], tuple[float,float,float], float, float, TimeEaseType) -> bool
    """
    设置相机移动动画, 会根据当前相机状态与传入参数按时间进行插值显示
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraMoveTo(pos, target_pos, up_vector, zoom, time, ease)


def camera_stop_actions():
    # type: () -> bool
    """
    停止相机移动动画
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraStopActions()


def camera_get_zoom():
    # type: () -> float
    """
    获取相机的缩放值
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraGetZoom()


def camera_get_click_model():
    # type: () -> int
    """
    获取相机当前指向的模型的id，会返回离相机最近的，通常与GetEntityByCoordEvent配合使用
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.CameraGetClickModel()


def model_create_object(model_name, animation_name):
    # type: (str, str) -> int
    """
    在虚拟世界中创建模型
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelCreateObject(model_name, animation_name)


def model_set_visible(obj_id, visible):
    # type: (int, bool) -> bool
    """
    设置模型可见性
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelSetVisible(obj_id, visible)


def model_is_visible(obj_id):
    # type: (int) -> bool
    """
    返回模型可见性
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelIsVisible(obj_id)


def model_play_animation(obj_id, anim, loop, is_blended=False, layer=0):
    """
    模型播放动画，支持动作融合，其功能与模型接口ModelPlayAni相同。

    支持骨骼动画混合，可参考SetAnimationBoneMask接口以及RegisterAnim1DControlParam接口说明。

    1.23 调整 新增动画混合功能, 新增设置动画层级参数，增加是否播放成功的返回值。

    :param obj_id: int 模型对象的id
    :param anim: str 要设置的动画名称
    :param loop: bool 是否循环播放，默认为 False
    :param is_blended: bool 播放时是与当前动画混合还是中止当前动画的播放，默认False，即中止当前动画播放。设置为True时，将允许即将播放的动画进行混合。注意，动画混合仅在相同层级的动画之间进行。若当前播放的动画与即将播放的动画层级不一样，则isBlended参数无效。
    :param layer: 设置骨骼动画的层级，范围为0~255，默认为0。注意，如果播放的动画已经存在，则会将原有的动画层级覆盖。动画层级越大，则优先度越高，骨骼模型的骨骼优先播放优先度最高的动画。
    :return: bool 是否成功设置
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelPlayAnimation(obj_id, anim, loop, is_blended, layer)


def model_stop_animation(obj_id, anim):
    """
    停止播放指定的模型动画

    :param obj_id: int 模型对象的id
    :param anim: str 模型的动画
    :return: bool 是否暂停成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(clientApi.GetLevelId())
    virtual_world_comp.ModelStopAnimation(obj_id, anim)


def model_set_anim_bone_mask(obj_id, anim, bone_names_list, enable, apply_to_child=True):
    """
    设置是否屏蔽动画中指定的骨骼的动画，若开启骨骼屏蔽后，该骨骼将不再播放该动画中的动作。

    通过屏蔽指定骨骼的动画可实现同一个骨骼模型同时在不同骨骼上播放不同的动作动画，从而实现快捷的动作融合。

    在使用该接口屏蔽上下半身的动画时，如果骨骼当中存在root骨骼，并且root骨骼的子骨骼包含上下半身的骨骼的话，root骨骼往往会控制整体骨骼模型的移动，要注意root骨骼对其他骨骼的影响。

    :param obj_id: int 模型对象的id
    :param anim: str 动画名称
    :param bone_names_list: list(str)	骨骼名称列表
    :param enable: bool 是否启用该骨骼的动画。True为不屏蔽，启动该骨骼的动画。False为屏蔽，不启动该骨骼的动画。
    :param apply_to_child: bool True为对该骨骼及其子骨骼生效，False为仅对该骨骼生效，默认为True
    :return: bool 设置是否成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(clientApi.GetLevelId())
    virtual_world_comp.ModelSetAnimBoneMask(obj_id, anim, bone_names_list, enable, apply_to_child)


def model_set_anim_all_bone_mask(obj_id, anim, ignore_bones_list, enable, apply_to_child=True):
    """
    设置是否屏蔽动画中所有骨骼的动画，若开启骨骼屏蔽后，该骨骼将不再播放该动画中的动作。

    该接口会对该动画中所有骨骼生效，可通过参数ignoreBoneList来指定不受影响的骨骼名称。

    通过屏蔽指定骨骼的动画可实现同一个骨骼模型同时在不同骨骼上播放不同的动作动画，从而实现快捷的动作融合。

    在使用该接口屏蔽上下半身的动画时，如果骨骼当中存在root骨骼，并且root骨骼的子骨骼包含上下半身的骨骼的话，root骨骼往往会控制整体骨骼模型的移动，要注意root骨骼对其他骨骼的影响。

    :param obj_id: int 模型对象的id
    :param anim: str 动画名称
    :param ignore_bones_list: list(str) 忽视的骨骼名称列表。在这个列表中的骨骼将不会被影响。输入空列表时则对所有骨骼执行这次设置。
    :param enable: bool 是否启用该骨骼的动画。True为不屏蔽，启动该骨骼的动画。False为屏蔽，不启动该骨骼的动画。
    :param apply_to_child: bool True为对ignoreBoneList中的骨骼的子骨骼也生效，False为仅对ignoreBoneList中的骨骼生效，默认为True。若ignoreBoneList为空列表，则applyToChild无效果。
    :return: bool 设置是否成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(clientApi.GetLevelId())
    virtual_world_comp.ModelSetAnimAllBoneMask(obj_id, anim, ignore_bones_list, enable, apply_to_child)


def model_cancel_all_bone_mask(obj_id, anim):
    """
    取消动画中的所有骨骼屏蔽。

    :param obj_id: int 模型对象的id
    :param anim: str 动画名称
    :return: bool 设置是否成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(clientApi.GetLevelId())
    virtual_world_comp.ModelCancelAllBoneMask(obj_id, anim)


def model_set_anim_layer(obj_id, anim, layer):
    """
    设置骨骼动画的层级，动画层级越大，则优先度越高，骨骼模型的骨骼优先播放优先度最高的动画，相同层级的动画则优先播放率先播放的动画。

    注意，设置层级相同的情况下不会改变当前的优先播放序列。举个例子：
        当前存在动画A及动画B，动画A的层级为1，动画B的层级为0，此时骨骼模型播放的动画为动画A。
        如果将动画A的层级设置为0，即动画A及动画B的层级相同，则当前仍然会播放动画A，因为层级相同的情况下不会改变目前的优先播放序列。

    要想让骨骼模型播放动画B，则需要动画B的层级比动画A的层级高。

    :param obj_id: int 模型对象的id
    :param anim: str 动画名称
    :param layer: int 动画层级， 正整数，范围为0~255
    :return: bool 设置是否成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(clientApi.GetLevelId())
    virtual_world_comp.ModelSetAnimLayer(obj_id, anim, layer)


def model_register_anim1_d_control_param(obj_id, anim1, anim2, param_name):
    """
    当同时播放多个骨骼动画时，新建用于控制动画进行1D线性混合的参数。

    目前线性混合仅支持对两个动画进行混合。新建的参数值范围为[0,1]。指定的骨骼将会按照这个参数的值对两个动画进行线性混合。

    * 注意，如果对某个骨骼使用了骨骼屏蔽，则这个1D线性混合将对该骨骼不会生效。另外，如果在使用该接口时新建一个已经存在的参数名称，则会将原来的参数覆盖。
    * 在动画的层级相同的情况下，动画的优先度播放顺序则首先按照：1.是否与需要其他动画进行混合。2.是否率先播放 这两个因素来先后决定。例如，我们首先对动画A，动画B使用接口RegisterAnim1DControlParam注册1D线性混合参数alpha， 然后对动画A和动画C使用接口RegisterAnim1DControlParam注册线性混合参数beta。接着，先后播放动画A, 动画C，动画B，动画D。这时，由于动画A，动画C具有混合需要，并且率先播放，因此骨骼模型会率先播放动画A和动画C的混合动画（注意，由于1D线性混合参数的初始值为0，因此此时混合动画的表现还是动画A），如果此时再暂停动画C，则会播放动画A与动画B的混合动画。接着暂停动画B，则会播放动画A，最后再暂停动画A，则才会播放动画D。
    * 另一种需要注意的情况：如果我们首先对动画A，动画B使用接口RegisterAnim1DControlParam注册1D线性混合参数alpha， 然后对动画A和动画C使用接口RegisterAnim1DControlParam注册线性混合参数beta。接着，先后播放动画A, 动画B，动画C。这时，我们调用SetAnim1DControlParam接口设置参数beta的值为0.5。此时模型仍然是播放动画A，这是由于动画A和动画B具有混合需求并且率先播放的，即率先凑齐了参数混合两个动画，因此此时模型实际上是在进行动画A和动画B的混合，但是由于alpha的值为0，因此模型还是表现为动画A，如果此时再用SetAnim1DControlParam接口设置参数alpha的值为0.5，则能够看到动画A和动画B的混合动画了。

    :param obj_id: int 模型对象的id
    :param anim1: str 混合的第一个动画名称，当1D参数的值为0时指定的骨骼仅播放这个动画。
    :param anim2: str 混合的第二个动画名称，当1D参数的值为1时指定的骨骼仅播放这个动画。
    :param param_name: str 自定义的1D参数名称。该参数新建后的初始值为0。
    :return: bool 设置是否成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(clientApi.GetLevelId())
    virtual_world_comp.ModelRegisterAnim1DControlParam(obj_id, anim1, anim2, param_name)


def model_set_anim1_d_control_param(obj_id, param_name, value):
    """
    新建动画的1D控制参数后，使用该接口对相应的参数进行控制。

    注意，如果对某个骨骼使用了骨骼屏蔽，则这个1D线性混合将对该骨骼不会生效。

    :param obj_id: int 模型对象的id
    :param param_name: str 使用接口RegisterAnim1DControlParam所新建的自定义1D参数名称。该参数新建后的初始值为0。
    :param value: float 参数的值，范围为[0,1]。当1D参数的值为0时仅播放接口RegisterAnim1DControlParam中的leftAniName参数指定的动画，当1D参数的值为1时仅播放接口RegisterAnim1DControlParam中的rightAniName参数指定的动画
    :return: bool 设置是否成功
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(clientApi.GetLevelId())
    virtual_world_comp.ModelSetAnim1DControlParam(obj_id, param_name, value)


def model_set_box_collider(obj_id, collision, offset=(0.0, 0.0, 0.0)):
    # type: (int, tuple[float,float,float], tuple[float,float,float]) -> bool
    """
    设置模型的包围盒
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelSetBoxCollider(obj_id, collision, offset)


def model_remove(obj_id):
    # type: (int) -> bool
    """
    销毁虚拟世界中的模型
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelRemove(obj_id)


def model_rotate(obj_id, degree_angle, axis):
    # type: (int, float, tuple[float,float,float]) -> bool
    """
    模型绕某个轴旋转多少度
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelRotate(obj_id, degree_angle, axis)


def model_set_pos(obj_id, pos):
    # type: (int, tuple[float,float,float]) -> bool
    """
    设置模型坐标
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelSetPos(obj_id, pos)


def model_get_pos(obj_id):
    # type: (int) -> tuple[float,float,float]
    """
    获取模型的坐标
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelGetPos(obj_id)


def model_set_rot(obj_id, rot):
    # type: (int, tuple[float,float,float]) -> bool
    """
    设置模型的旋转角度
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelSetRot(obj_id, rot)


def model_get_rot(obj_id):
    # type: (int) -> tuple[float,float,float]
    """
    返回模型的旋转角度
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelGetRot(obj_id)


def model_set_scale(obj_id, scales):
    # type: (int, tuple[float,float,float]) -> bool
    """
    设置模型的缩放值
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelSetScale(obj_id, scales)


def model_move_to(obj_id, pos, time, ease=TimeEaseType.linear):
    # type: (int, tuple[float,float,float], float, TimeEaseType) -> bool
    """
    设置模型平移运动
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelMoveTo(obj_id, pos, time, ease)


def model_rotate_to(obj_id, rot, time, ease=TimeEaseType.linear):
    # type: (int, tuple[float,float,float], float, TimeEaseType) -> bool
    """
    设置模型旋转运动
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelRotateTo(obj_id, rot, time, ease)


def model_stop_actions(obj_id):
    # type: (int) -> bool
    """
    停止模型的移动和旋转运动
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.ModelStopActions(obj_id)


def move_to_virtual_world(obj_type, obj_id):
    # type: (VirtualWorldObjectType, int) -> bool
    """
    把对象从主世界移到虚拟世界, 非绑定的序列帧，文本，粒子需要调用该方法后才会出现在虚拟世界中，绑定的可以省略调用该方法。
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.MoveToVirtualWorld(obj_type, obj_id)


def bind_model_in_virtual_world(obj_type, obj_id, target_id, pos_offset, rot_offset, bone_name='root'):
    # type: (VirtualWorldObjectType, int, int, tuple[float,float,float], tuple[float,float,float], str) -> bool
    """
    把对象绑定到模型上, 支持绑定序列帧，粒子，文本和其它模型
    """
    virtual_world_comp = clientApi.GetEngineCompFactory().CreateVirtualWorld(level_id)
    return virtual_world_comp.BindModel(obj_type, obj_id, target_id, pos_offset, rot_offset, bone_name)
