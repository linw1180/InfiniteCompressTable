# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def set_command(cmd_str, player_id=None, show_output=False):
    """
    使用游戏内指令
    
    :param cmd_str: str 指令
    :param player_id: str 玩家id:可选，如果playerId不设置，则随机选择玩家
    :param show_output: bool 是否输出到聊天窗口：可选，默认False，如果为True的话会和聊天窗口输入原生指令一样输出返回信息。
        只有当该参数为True的时候会触发OnCommandOutputClientEvent
    :return: bool 设置结果
    """
    command_comp = serverApi.GetEngineCompFactory().CreateCommand(level_id)
    command_comp.SetCommand(cmd_str, player_id, show_output)  # 传送指令
