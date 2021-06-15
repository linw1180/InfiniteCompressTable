# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi
from mod.common.mod import Mod

from infiniteCompressTableScripts.modCommon import *


# 主类
@Mod.Binding(name=ModName, version=ModVersion)
class InfiniteCompressTable(object):

    # 初始化
    def __init__(self):
        print '======== Initialize InfiniteCompressTable Mod ========'

    # 初始化服务端系统
    @Mod.InitServer()
    def server_init(self):
        serverApi.RegisterSystem(ModName, ModServerSystemName, ModServerSystemPath)

    # 初始化客户端系统
    @Mod.InitClient()
    def client_init(self):
        clientApi.RegisterSystem(ModName, ModClientSystemName, ModClientSystemPath)
