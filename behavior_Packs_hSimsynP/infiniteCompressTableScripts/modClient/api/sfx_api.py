# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi


def play_sfx(frame_id):
    """
    播放序列帧
    
    :param frame_id: 
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.Play()


def stop_sfx(frame_id):
    """
    停止序列帧 **不是暂停**
    
    :param frame_id: 
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.Stop()


def set_sfx_face_camera(frame_id, face):
    """
    设置序列帧是否始终朝向摄像机，默认为是

    :param frame_id:
    :param face: bool True表示朝摄像机
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.SetFaceCamera(face)


def set_sfx_loop(frame_id, loop):
    """
    设置序列帧是否循环播放，默认为否

    :param frame_id:
    :param loop: bool True表示循环播放
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.SetLoop(loop)


def set_sfx_deep_test(frame_id, deep_test):
    """
    设置序列帧是否透视，默认为否

    :param frame_id:
    :param deep_test: bool False表示透视，则被物体/方块阻挡时仍然能看到序列帧
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.SetDeepTest(deep_test)


def set_sfx_layer(frame_id, layer):
    """
    设置序列帧渲染层级，默认层级为1，当层级不为1时表示该特效开启特效分层渲染功能。

    特效（粒子和帧动画）分层渲染时，层级越高渲染越靠后，层级大的会遮挡层级低的，且同一层级的特效会根据特效的相对位置产生正确的相互遮挡关系。

    该接口只针对序列帧进行设置，粒子特效请使用particleControl组件

    :param frame_id:
    :param layer: int 粒子渲染层级，总共包含0-15的层级。
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.SetLayer(layer)


def set_sfx_mix_color(frame_id, color):
    """
    设置序列帧混合颜色

    :param frame_id:
    :param color: tuple(float,float,float,float) 颜色的RGBA值，范围0-1
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.SetMixColor(color)


def set_sfx_fade_distance(frame_id, fade_distance):
    """
    设置序列帧开始自动调整透明度的距离。

    序列帧与摄像机之间的距离小于该值时会自动调整序列帧的透明度，距离摄像机越近，序列帧越透明

    :param frame_id:
    :param fade_distance: float 自动调整透明度的距离，应为正数，负数将视作零来处理
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.SetFadeDistance(fade_distance)


def set_sfx_point_filtering(frame_id, use):
    """
    设置序列帧是否使用点滤波

    使用点滤波的图像通常边缘清晰、可能会有较强烈的锯齿感；使用双线性插值的图像通常比较平滑、可能会使图像一定程度上变得模糊

    :param frame_id:
    :param use: True为使用点滤波，False为使用双线性插值（默认使用）
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniControl(frame_id)
    return frame_comp.SetUsePointFiltering(use)


def set_sfx_pos(frame_id, pos):
    """
    设置序列帧的位置

    :param frame_id:
    :param pos: tuple(float,float,float) 世界坐标
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frame_id)
    return frame_comp.SetPos(pos)


def set_sfx_rot(frame_id, rot):
    """
    设置序列帧的旋转

    :param frame_id:
    :param rot: tuple(float,float,float) 按顺序绕局部坐标系的+x，-y，+z轴旋转的角度
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frame_id)
    return frame_comp.SetRot(rot)


def set_sfx_scale(frame_id, scale):
    """
    设置序列帧的缩放

    :param frame_id:
    :param scale: tuple(float,float,float) 对于平面序列帧，第一个参数为贴图横向上的缩放，第二个参数为纵向上的缩放，第三个参数无用。对于环状序列帧，为三个坐标轴上的缩放
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniTrans(frame_id)
    return frame_comp.SetScale(scale)


def bind_sfx_to_entity(frame_id, entity_id, offset, rot):
    """
    绑定entity

    :param frame_id:
    :param entity_id: str 绑定的entity的ID
    :param offset: tuple(float,float,float) 绑定的偏移量
    :param rot: tuple(float,float,float) 绑定的旋转角度
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniEntityBind(frame_id)
    return frame_comp.Bind(entity_id, offset, rot)


def bind_sfx_to_model(frame_id, model_id, bone_name, offset, rot):
    """
    绑定骨骼模型

    :param frame_id:
    :param model_id: int 绑定的骨骼模型的ID（见model组件的GetModelId）
    :param bone_name: str 绑定具体骨骼的名称
    :param offset: tuple(float,float,float) 绑定的偏移量
    :param rot: tuple(float,float,float) 绑定的旋转角度
    :return: bool 设置是否成功
    """
    frame_comp = clientApi.GetEngineCompFactory().CreateFrameAniSkeletonBind(frame_id)
    return frame_comp.Bind(model_id, bone_name, offset, rot)
