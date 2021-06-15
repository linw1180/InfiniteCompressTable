# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def notify_one_message(player_id, msg, color="§f"):
    """
    给指定玩家发送聊天框消息

    :param player_id:
    :param msg: str 消息内容
    :param color: str 颜色样式代码字符串，可参考wiki[样式代码](https://minecraft-zh.gamepedia.com/%E6%A0%B7%E5%BC%8F%E4%BB%A3%E7%A0%81)，默认为白色
    :return:
    """
    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
    msg_comp.NotifyOneMessage(player_id, msg, color)


def send_msg(player_id, name, msg):
    """
    创建消息实体

    name参数需要设置玩家的名字(可通过name组件获取)，如果设置的玩家名字不存在，则随机找一个玩家发出该消息

    :param player_id: str 玩家id
    :param name: str 发送者玩家的名字
    :param msg: str 消息内容
    :return: bool 设置结果
    """
    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(player_id)
    return msg_comp.SendMsg(name, msg)


def send_msg_to_player(from_player_id, to_player_id, msg):
    """
    创建消息实体，然后发送给某个玩家

    :param from_player_id: str 发送者玩家ID
    :param to_player_id: str 接受者玩家ID
    :param msg: str 消息内容
    :return:
    """
    msg_comp = serverApi.GetEngineCompFactory().CreateMsg(from_player_id)
    msg_comp.SendMsgToPlayer(from_player_id, to_player_id, msg)
