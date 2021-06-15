# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def disable_official_pet():
    """
    关闭官方伙伴功能，单人游戏以及本地联机不支持该接口

    1.18 新增 禁用官方伙伴功能

    :return: bool 关闭结果
    """
    pet_comp = serverApi.GetEngineCompFactory().CreatePet(level_id)
    return pet_comp.Disable()


def enable_official_pet():
    """
    启用官方伙伴功能，单人游戏以及本地联机不支持该接口

    1.18 新增 开启官方伙伴功能

    :return: bool 启用结果
    """
    pet_comp = serverApi.GetEngineCompFactory().CreatePet(level_id)
    return pet_comp.Enable()
