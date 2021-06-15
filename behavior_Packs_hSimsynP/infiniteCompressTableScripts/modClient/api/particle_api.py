# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi


def play_particle(particle_entity_id):
    """
    播放粒子特效

    :param particle_entity_id:
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleControl(particle_entity_id)
    return particle_comp.Play()


def stop_particle(particle_entity_id):
    """
    停止粒子播放

    :param particle_entity_id:
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleControl(particle_entity_id)
    return particle_comp.Stop()


def set_particle_relative(particle_entity_id, relative=True):
    """
    当粒子绑定了entity或骨骼模型时，发射出的粒子使用entity坐标系还是世界坐标系。

    与MCStudio特效编辑器中粒子的“相对挂点运动”选项功能相同。

    :param particle_entity_id:
    :param relative: bool True表示相对坐标系，False表示世界坐标系
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleControl(particle_entity_id)
    return particle_comp.SetRelative(relative)


def set_particle_layer(particle_entity_id, layer):
    """
    粒子默认层级为1，当层级不为1时表示该特效开启特效分层渲染功能。

    特效（粒子和帧动画）分层渲染时，层级越高渲染越靠后，层级大的会遮挡层级低的，且同一层级的特效会根据特效的相对位置产生正确的相互遮挡关系。

    该接口只针对粒子进行设置，序列帧特效请使用frameAniControl组件

    :param particle_entity_id:
    :param layer: int 粒子渲染层级，总共包含0-15的层级。
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleControl(particle_entity_id)
    return particle_comp.SetLayer(layer)


def set_particle_fade_distance(particle_entity_id, fade_distance):
    """
    设置粒子开始自动调整透明度的距离。

    粒子与摄像机之间的距离小于该值时会自动调整粒子的透明度，距离摄像机越近，粒子越透明

    :param particle_entity_id:
    :param fade_distance: float 自动调整透明度的距离，应为正数，负数将视作零来处理
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleControl(particle_entity_id)
    return particle_comp.SetFadeDistance(fade_distance)


def set_sfx_point_filtering(particle_entity_id, use):
    """
    设置粒子材质的纹理滤波是否使用点滤波方法。默认为使用双线性滤波

    使用点滤波的图像通常边缘清晰、可能会有较强烈的锯齿感；使用双线性插值的图像通常比较平滑、可能会使图像一定程度上变得模糊

    :param particle_entity_id:
    :param use: True为使用点滤波，False为使用双线性插值（默认使用）
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleControl(particle_entity_id)
    return particle_comp.SetUsePointFiltering(use)


def set_particle_pos(particle_entity_id, pos):
    """
    设置粒子的位置

    :param particle_entity_id:
    :param pos: tuple(float,float,float)
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleTrans(particle_entity_id)
    return particle_comp.SetPos(pos)


def set_particle_rot(particle_entity_id, rot):
    """
    设置粒子的角度

    :param particle_entity_id:
    :param rot: tuple(float,float,float)
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleTrans(particle_entity_id)
    return particle_comp.SetRot(rot)


def bind_particle_to_entity(particle_entity_id, entity_id, offset, rot, correction=False):
    """
    绑定entity
    
    :param particle_entity_id: 
    :param entity_id: str 绑定的entity的ID
    :param offset: tuple(float,float,float) 绑定的偏移量，相对绑定entity脚下中心
    :param rot: tuple(float,float,float) 绑定的旋转角度
    :param correction: bool 默认不开启，开启后可以使特效的旋转角度准确设置为参照玩家的相对角度
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleEntityBind(particle_entity_id)
    return particle_comp.Bind(entity_id, offset, rot, correction)


def bind_particle_to_model(particle_entity_id, model_id, bone_name, offset, rot):
    """
    绑定骨骼模型

    :param particle_entity_id:
    :param model_id: int 绑定的骨骼模型的ID（见model组件的GetModelId）
    :param bone_name: str 绑定具体骨骼的名称
    :param offset: tuple(float,float,float) 绑定的偏移量
    :param rot: tuple(float,float,float) 绑定的旋转角度
    :return: bool 设置是否成功
    """
    particle_comp = clientApi.GetEngineCompFactory().CreateParticleSkeletonBind(particle_entity_id)
    return particle_comp.Bind(model_id, bone_name, offset, rot)
