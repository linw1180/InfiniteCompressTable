# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def play_system_sound(player_id, sound_id, pos, block_type, entity_type, is_baby, is_global, dimension=-1):
    """
    播放游戏内原有内容
    
    由于游戏中音效是通过事件触发的。例如：鸡的死亡音效：因为死亡跟block无关，因此 soundId: Death, entityType: Chicken, blockId: -1
    
    着地音效：因为着地到不同的block，音效是不一样的， 因此 soundId: Fall, entityType: -1, blockId: grass
    
    1.20 调整 新增dimensionId参数，默认为-1，传入非负值时不依赖playerId，可在对应维度的常加载区块播放游戏音效
    
    :param player_id: str或None 玩家id/None
    :param sound_id: int 详见[SysSoundType]
    :param pos: tuple(float,float,float) 音源位置
    :param block_type: int 详见[BlockType]
    :param entity_type: int 详见[EntityType]
    :param is_baby: bool 是否为幼儿音效
    :param is_global: bool 是否为全局
    :param dimension: int 音源所在维度，默认值为-1，传入非负值时不依赖playerId，playerId可传入None，可在对应维度的常加载区块播放游戏音效
    :return: bool 设置结果
    """
    if dimension > -1:
        audio_comp = serverApi.GetEngineCompFactory().CreateSystemAudio(level_id)
        audio_comp.PlaySystemSound(None, sound_id, pos, block_type, entity_type, is_baby, is_global, dimension)

    audio_comp = serverApi.GetEngineCompFactory().CreateSystemAudio(player_id)
    audio_comp.PlaySystemSound(player_id, sound_id, pos, block_type, entity_type, is_baby, is_global)
