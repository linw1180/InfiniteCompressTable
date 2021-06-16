# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()


def register_update_attr_func(entity_id, param_name, func):
    """
    注册属性值变换时的回调函数，当属性变化时会调用该函数
    
    回调函数需要接受一个参数，参数是dict，具体数据示例：{'oldValue': 0, 'newValue': 1, 'entityId': ’-433231231231‘}
    
    :param entity_id: 
    :param param_name: str 监听的属性名称
    :param func: function 监听的回调函数
    :return: 
    """
    mod_attr_comp = clientApi.GetEngineCompFactory().CreateModAttr(entity_id)
    mod_attr_comp.RegisterUpdateFunc(param_name, func)


def cancel_update_attr_func(entity_id, param_name, func):
    """
    反注册属性值变换时的回调函数

    需要传注册时的 **同一个函数** 作为参数

    :param entity_id:
    :param param_name: str 监听的属性名称
    :param func: function 监听的回调函数
    :return:
    """
    mod_attr_comp = clientApi.GetEngineCompFactory().CreateModAttr(entity_id)
    mod_attr_comp.UnRegisterUpdateFunc(param_name, func)


def set_mod_attr(entity_id, param_name, param_value):
    """
    设置客户端属性值

    注意：这里设置了只在本地有效，并不会同步到服务端和其他客户端

    :param entity_id:
    :param param_name: str 属性名称，str的名称建议以mod命名为前缀，避免多个mod之间冲突
    :param param_value: any 属性值，支持python基础数据
    :return:
    """
    mod_attr_comp = clientApi.GetEngineCompFactory().CreateModAttr(entity_id)
    mod_attr_comp.SetAttr(param_name, param_value)


def get_mod_attr(entity_id, param_name, default_value=None):
    """
    获取属性值

    defaultValue不传的时候默认为None

    :param entity_id:
    :param param_name: str 属性名称，str的名称建议以mod命名为前缀，避免多个mod之间冲突
    :param default_value: any 属性默认值，属性不存在时返回该默认值，此时属性值依然未设置
    :return: any 返回属性值
    """
    mod_attr_comp = clientApi.GetEngineCompFactory().CreateModAttr(entity_id)
    return mod_attr_comp.GetAttr(param_name, default_value)
