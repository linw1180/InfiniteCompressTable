# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def detect_portal_structure(pattern, defines, touch_pos, pos, dimension=0):
    """
    检测自定义门的结构

    http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/02-Python%E8%84%9A%E6%9C%AC%E5%BC%80%E5%8F%91/99-ModAPI/4-%E7%BB%84%E4%BB%B6/2-%E6%9C%8D%E5%8A%A1%E7%AB%AF%E7%BB%84%E4%BB%B6.html#detectstructure

    1.23 调整 新增dimensionId参数，默认为-1，传入非负值时不依赖playerId，废弃player_id参数

    1.18 新增 检测自定义门的结构
    
    :param pattern: list(str) 传送门形状
    :param defines: dict 传送门定义
    :param touch_pos: list(tuple(int,int)) 传送门可激活的位置（相对参数pattern中定义的位置）
    :param pos: tuple(int,int,int) 使用物品坐标
    :param dimension: int 传送门所在维度
    :return: tuple(bool,tuple(int,int,int),tuple(int,int,int)) 检测结果,传送门起始位置,方向
    """
    portal_comp = serverApi.GetEngineCompFactory().CreatePortal(level_id)
    return portal_comp.DetectStructure(None, pattern, defines, touch_pos, pos, dimension)
