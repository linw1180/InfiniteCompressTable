# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def get_biome_name(pos, dimension):
    """
    获取某一位置所属的生物群系信息

    1.19 调整 添加维度参数，并支持获取未加载区块的群系，不再需要使用playerId创建comp

    :param pos: tuple(int,int,int) 指定位置
    :param dimension: int 维度id
    :return: str 该位置所属生物群系name
    """
    biome_comp = serverApi.GetEngineCompFactory().CreateBiome(level_id)
    return biome_comp.GetBiomeName(pos, dimension)
