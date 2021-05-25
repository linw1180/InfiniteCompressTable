# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()
SystemName = serverApi.GetEngineSystemName()
Namespace = serverApi.GetEngineNamespace()


# 服务端系统
class InfiniteCompressTableServerSystem(ServerSystem):

    # 初始化
    def __init__(self, namespace, system_name):
        ServerSystem.__init__(self, namespace, system_name)
        # TODO: 服务端系统功能

