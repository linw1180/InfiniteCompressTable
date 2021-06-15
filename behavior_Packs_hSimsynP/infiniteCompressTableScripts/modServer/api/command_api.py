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
    :return: bool 命令是否执行成功
    """
    command_comp = serverApi.GetEngineCompFactory().CreateCommand(level_id)
    command_comp.SetCommand(cmd_str, player_id, show_output)


def get_command_permission_level():
    """
    返回设定使用/op命令时OP的权限等级（对应server.properties中的op-permission-level配置）

    :return: int 权限等级：1-OP可以绕过重生点保护；2-OP可以使用所有单人游戏作弊命令；3-OP可以使用大多数多人游戏中独有的命令；4-OP可以使用所有命令
    """
    command_comp = serverApi.GetEngineCompFactory().CreateCommand(level_id)
    return command_comp.GetCommandPermissionLevel()


def set_command_permission_level(op_level):
    """
    设置当玩家使用/op命令时OP的权限等级（对应server.properties中的op-permission-level配置）

    :param op_level: int 权限等级：1-OP可以绕过重生点保护；2-OP可以使用所有单人游戏作弊命令；3-OP可以使用大多数多人游戏中独有的命令；4-OP可以使用所有命令
    :return: bool 设置结果
    """
    command_comp = serverApi.GetEngineCompFactory().CreateCommand(level_id)
    return command_comp.SetCommandPermissionLevel(op_level)


def get_default_player_permission_level():
    """
    返回新玩家加入时的权限身份（对应server.properties中的default-player-permission-level配置）

    :return: int 权限身份：0-Visitor；1-Member；2-Operator；3-自定义
    """
    command_comp = serverApi.GetEngineCompFactory().CreateCommand(level_id)
    return command_comp.GetDefaultPlayerPermissionLevel()


def set_default_player_permission_level(op_level):
    """
    设置新玩家加入时的权限身份（对应server.properties中的default-player-permission-level配置）

    :param op_level: int 权限身份：0-Visitor；1-Member；2-Operator；3-自定义
    :return: bool 设置结果
    """
    command_comp = serverApi.GetEngineCompFactory().CreateCommand(level_id)
    return command_comp.SetDefaultPlayerPermissionLevel(op_level)
