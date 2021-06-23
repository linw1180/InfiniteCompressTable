# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

from infiniteCompressTableScripts.modCommon import ModName, ModClientSystemName
from infiniteCompressTableScripts.modServer.api import un_listen_all_events
from infiniteCompressTableScripts.modServer.server_system import block_server, item_server

ServerSystem = serverApi.GetServerSystemCls()
SystemName = serverApi.GetEngineSystemName()
Namespace = serverApi.GetEngineNamespace()


# 服务端系统
class InfiniteCompressTableServerSystem(ServerSystem):

    # 初始化
    def __init__(self, namespace, system_name):
        super(InfiniteCompressTableServerSystem, self).__init__(namespace, system_name)
        self.listen_events()

    def listen_events(self):

        # 注册服务端引擎事件监听
        for event_name, instance, function in [
            ["ServerBlockUseEvent", block_server, block_server.player_use_block]
        ]:
            self.ListenForEvent(Namespace, SystemName, event_name, instance, function)

        # 注册客户端事件监听
        for event_name, instance, function in [
            ["OnItemSwapClientEvent", item_server, item_server.on_item_swap],
            ["OnClickItemSlot", item_server, item_server.set_item_custom_tips],
        ]:
            self.ListenForEvent(ModName, ModClientSystemName, event_name, instance, function)

    def Destroy(self):
        un_listen_all_events()
