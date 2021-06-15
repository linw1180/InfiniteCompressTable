# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()
SystemName = clientApi.GetEngineSystemName()
Namespace = clientApi.GetEngineNamespace()


# 客户端系统
class InfiniteCompressTableClientSystem(ClientSystem):

    # 初始化
    def __init__(self, namespace, system_name):
        super(InfiniteCompressTableClientSystem, self).__init__(namespace, system_name)
        # TODO: 客户端系统功能
