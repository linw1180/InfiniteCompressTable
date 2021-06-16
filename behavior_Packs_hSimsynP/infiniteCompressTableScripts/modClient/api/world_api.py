# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()


def add_timer(delay, func, *args, **kwargs):
    """
    添加服务端触发的定时器，非重复

    :param delay: float 延迟时间，单位秒
    :param func: function 定时器触发函数
    :param args: any 变长参数，可以不设置
    :param kwargs: any 字典变长参数，可以不设置
    :return: CallLater 返回单次触发的定时器实例
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.AddTimer(delay, func, *args, **kwargs)


def add_repeated_timer(delay, func, *args, **kwargs):
    """
    添加服务端触发的定时器，重复执行

    :param delay: float 延迟时间，单位秒
    :param func: function 定时器触发函数
    :param args: any 变长参数，可以不设置
    :param kwargs: any 字典变长参数，可以不设置
    :return: CallLater 返回触发的定时器实例
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    return game_comp.AddRepeatedTimer(delay, func, *args, **kwargs)


def cancel_timer(timer):
    """
    取消定时器

    :param timer: CallLater AddTimer和AddRepeatedTimer时返回的定时器实例
    :return:
    """
    game_comp = clientApi.GetEngineCompFactory().CreateGame(level_id)
    game_comp.CancelTimer(timer)
