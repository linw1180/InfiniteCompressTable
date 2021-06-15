# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi


def get_config_data(config_name, is_global=False):
    """
    获取本地存储数据

    :param config_name: str 配置名称
    :param is_global: bool 存档配置or全局配置，默认False
    :return:
    """
    config_comp = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
    return config_comp.GetConfigData(config_name, is_global)


def set_config_data(config_name, value, is_global=False):
    """
    保存本地数据

    :param config_name: str
    :param value: dict
    :param is_global: bool 存档配置or全局配置，默认False
    :return: bool 是否成功
    """
    config_comp = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
    return config_comp.SetConfigData(config_name, value, is_global)
