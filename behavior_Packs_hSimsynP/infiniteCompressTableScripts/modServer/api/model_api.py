# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi


def get_model_name(entity_id):
    """
    获取实体的模型名称

    :param entity_id:
    :return: str 模型名称
    """
    model_comp = serverApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.GetModelName()


def set_model(entity_id, model_name):
    """
    设置骨骼模型

    :param entity_id:
    :param model_name: str 模型名称,值为""时重置模型
    :return: bool 设置结果
    """
    model_comp = serverApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetModel(model_name)


def set_model_offset(entity_id, offset):
    """
    设置骨骼模型相对于局部坐标系的偏移量，初始值为(0, 0, 0)

    :param entity_id:
    :param offset: tuple(float,float,float) 偏移量
    :return:
    """
    model_comp = serverApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetModelOffset(offset)


def set_model_texture(entity_id, texture):
    """
    设置骨骼模型贴图

    :param entity_id:
    :param texture: str 模型纹理
    :return: bool 设置结果
    """
    model_comp = serverApi.GetEngineCompFactory().CreateModel(entity_id)
    return model_comp.SetModelTexture(texture)


def set_entity_scale(entity_id, scale):
    """
    设置实体的放缩比例大小，设置比例过大会导致游戏卡顿，建议控制在20倍以内

    目前此功能只支持设置生物的骨骼模型，游戏原生实体（包括手持物品）的暂不做支持与维护

    :param entity_id: str 要设置的实体
    :param scale: float 比例因子
    :return: int 成功返回1，失败返回-1
    """
    scale_comp = serverApi.GetEngineCompFactory().CreateScale(entity_id)
    return scale_comp.SetEntityScale(entity_id, scale)


def get_entity_scale(entity_id):
    """
    获取实体的放缩比例大小

    :param entity_id:
    :return: float 比例因子
    """
    scale_comp = serverApi.GetEngineCompFactory().CreateScale(entity_id)
    return scale_comp.GetEntityScale()
