# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi


def play_origin_music(entity_id, play=False):
    """
    播放/停止原生背景音乐
    
    :param entity_id: 
    :param play: bool True表示播放，False表示停止
    :return: bool 设置是否成功
    """
    audio_comp = clientApi.GetEngineCompFactory().CreateCustomAudio(entity_id)
    return audio_comp.DisableOriginMusic(play)


def play_global_custom_music(entity_id, name, volume=1, loop=False):
    """
    播放全局自定义音乐
    
    全局音乐的播放速度需要从配置json里进行修改
    
    全局音乐仅能播放一个，当指定全局音乐播放时，会停止掉之前播放的音乐
    
    全局音乐的优先级大于普通音乐，当全局音乐在播放时，会让同名普通音乐播放失败
    
    针对比较大的全局音乐，请将load_on_low_memory和stream设为true
    
    全局音乐需要在json里定义category为music
    
    与示例对应的sound_definitions.json配置：
    {
      "Gsound001": {
        "category": "music",
        "sounds": [
          {
            "name": "sounds/testaudio/Music001",
            "load_on_low_memory": true,
            "stream": true,
            "pitch": 1,
            "volume": 1
          }
        ]
      }
    }
    
    :param entity_id: 
    :param name: str 音乐名称
    :param volume: float 音量大小，范围0-1，可以从 json 文件里进行修改
    :param loop: bool 是否循环播放
    :return: bool 播放是否成功
    """
    audio_comp = clientApi.GetEngineCompFactory().CreateCustomAudio(entity_id)
    return audio_comp.PlayGlobalCustomMusic(name, volume, loop)


def play_custom_music(entity_id, name, pos=(0, 0, 0), volume=1, pitch=1, loop=False):
    """
    播放场景音效，包括原版音效及自定义音效

    当播放音乐错误时，将返回相应的错误id

    错误id&错误描述 :
        * -1: 无法在服务端播放自定义音乐
        * -2: 播放位置错误
        * -3: 已有同名全局音乐正在播放
        * -4: 播放失败
        * -5: 绑定实体不存在
        * -6: 位置距离本地玩家距离大于16格，跳过音效播放（绑定实体的音效不受此限制）


    * 当全局音乐在播放的时候，请不要播放同名的普通音乐
    * 针对比较大的音乐，请将load_on_low_memory和stream设为true
    * 该接口触发PlaySoundClientEvent

    与示例对应的sound_definitions.json配置：
    {
      "sound001": {
        "min_distance": 0,
        "max_distance": 20.0,
        "sounds": [
          {
            "name": "sounds/testaudio/largeBlast1",
            "load_on_low_memory": true,
            "stream": true,
            "pitch": 1,
            "volume": 1
          }
        ]
      }
    }

    1.23 调整 添加可以播放原版音效的描述。添加了与本地玩家距离大于16格则跳过播放的优化。

    :param entity_id:
    :param name: str 音乐名称
    :param pos: tuple(float,float,float) 播放位置
    :param volume: float 音量大小，范围0-1，可以从json文件里进行修改
    :param pitch: float 播放速度，范围0-256，1表示原速，可以从json文件里进行修改
    :param loop: bool 是否循环播放
    :return: str 音乐播放id，可用于控制音乐的停止和循环
    """
    audio_comp = clientApi.GetEngineCompFactory().CreateCustomAudio(entity_id)
    return audio_comp.PlayCustomMusic(name, pos, volume, pitch, loop)


def stop_custom_music_by_name(entity_id, name, fade_out_time=0.0):
    """
    停止自定义音乐，包括全局音乐，将依据fade_out_time触发OnMusicStopClientEvent事件

    :param entity_id:
    :param name: str 音乐名称
    :param fade_out_time: float 停止的淡出时间，单位为秒，如果剩余时间小于淡出时间，将以剩余时间为准
    :return: bool 停止是否成功
    """
    audio_comp = clientApi.GetEngineCompFactory().CreateCustomAudio(entity_id)
    return audio_comp.StopCustomMusic(name, fade_out_time)


def stop_custom_music_by_id(entity_id, music_id, fade_out_time=0.0):
    """
    停止自定义音乐

    :param entity_id:
    :param music_id: str 音乐id，播放指定音乐获取的音乐id
    :param fade_out_time: float 停止的淡出时间，单位为秒
    :return: bool 停止是否成功
    """
    audio_comp = clientApi.GetEngineCompFactory().CreateCustomAudio(entity_id)
    return audio_comp.StopCustomMusicById(music_id, fade_out_time)


def set_custom_music_loop(entity_id, name, loop=True):
    """
    设定指定音乐是否循环播放，包括全局音乐

    :param entity_id:
    :param name: str 音乐名称
    :param loop: bool True则循环播放，False则停止循环，停止会持续到播放到本次结束
    :return: bool 停止是否成功
    """
    audio_comp = clientApi.GetEngineCompFactory().CreateCustomAudio(entity_id)
    return audio_comp.SetCustomMusicLoop(name, loop)


def set_custom_music_loop_by_id(entity_id, music_id, loop=True):
    """
    设定指定音乐是否循环播放
    
    :param entity_id: 
    :param music_id: str 音乐id，播放指定音乐获取的音乐id
    :param loop: bool True则循环播放，False则停止循环，停止会持续到播放到本次结束
    :return: bool 停止是否成功
    """
    audio_comp = clientApi.GetEngineCompFactory().CreateCustomAudio(entity_id)
    return audio_comp.SetCustomMusicLoopById(music_id, loop)
