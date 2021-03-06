# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

from infiniteCompressTableScripts.modClient.api import un_listen_all_events, notify_to_server, local_player
from infiniteCompressTableScripts.modClient.client_system import ui_client
from infiniteCompressTableScripts.modClient.utils.ui_utils import get_ui_manager
from infiniteCompressTableScripts.modCommon import ModName, ModServerSystemName

ClientSystem = clientApi.GetClientSystemCls()
SystemName = clientApi.GetEngineSystemName()
Namespace = clientApi.GetEngineNamespace()


# 客户端系统
class InfiniteCompressTableClientSystem(ClientSystem):

    # 初始化
    def __init__(self, namespace, system_name):
        super(InfiniteCompressTableClientSystem, self).__init__(namespace, system_name)
        self.listen_events()

    def listen_events(self):
        for event_name, instance, function in [
            ['UiInitFinished', get_ui_manager(), get_ui_manager().init_all_ui],
        ]:
            self.ListenForEvent(Namespace, SystemName, event_name, instance, function)

        for event_name, instance, function in [
            ['OpenBlockUI', ui_client, ui_client.open_block_ui],
            ['UpdateBlockUI', ui_client, ui_client.update_block_ui],
            ['OnItemSwapServerEvent', ui_client, ui_client.on_item_swap],
            ['OnItemProcessedServerEvent', ui_client, ui_client.on_item_processed],  # processed 处理
            ['ShowShortTimeMsg1Event', ui_client, ui_client.on_short_time_msg1_show],
        ]:
            self.ListenForEvent(ModName, ModServerSystemName, event_name, instance, function)

    @staticmethod
    def Destroy():
        un_listen_all_events()
