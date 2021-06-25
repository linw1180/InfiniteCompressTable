# -*- coding: utf-8 -*-

from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modCommon.utils import item_utils
from infiniteCompressTableScripts.modServer.api import get_player_item, get_item_basic_info, set_player_inv_item_num, \
    spawn_item_to_player_inv, exchange_player_inv_item, notify_to_client
from infiniteCompressTableScripts.modServer.server_system import block_server


def on_item_swap(args):
    print '------------------- server ---> on_item_swap --------------------- args =', args
    player_id = args['player_id']
    block_name = args['block_name']
    from_slot = args['from_slot']
    to_slot = args['to_slot']
    from_item = args['from_item']
    to_item = args['to_item']
    take_percent = args['take_percent']

    # 自定义容器和背包之间的交换
    if isinstance(from_slot, str) or isinstance(to_slot, str):
        if block_name in block_server.BLOCK_SERVER_MAPPING:
            block = block_server.BLOCK_SERVER_MAPPING[block_name]
            # if not block.on_custom_container_item_swap(args):
            #     return
            block.on_custom_container_item_swap(args)
            return

    # 背包内部交换
    else:
        print '---------------------- server ---> in bag exchange ------------------------'
        if isinstance(to_slot, int):
            to_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
            print '................. server ..................... to_item =', to_item
        if isinstance(from_slot, int):
            from_item = get_player_item(player_id, ItemPosType.INVENTORY, from_slot, True)
            print '.................. server .................... from_item =', from_item

        if item_utils.is_same_item(from_item, to_item):
            # 两个槽物品相同时处理堆叠
            basic_info = get_item_basic_info(to_item.get("itemName"), to_item.get("auxValue"))
            if not basic_info:
                return
            max_size = basic_info.get("maxStackSize")
            take_num = int(from_item.get("count") * take_percent)
            from_num = from_item.get("count")
            to_num = to_item.get("count")
            if not take_num and not to_num:
                print "OnItemSwap Error!!!"
                return
            if to_num == max_size:
                return
            if to_num + take_num >= max_size:
                from_num -= max_size - to_num
                to_num = max_size
            else:
                to_num += take_num
                from_num -= take_num
            from_item["count"] = to_num
            to_item["count"] = from_num
            if from_num == 0:
                to_item = None
            if isinstance(from_slot, int):
                set_player_inv_item_num(player_id, from_slot, to_num)
            if isinstance(to_slot, int):
                set_player_inv_item_num(player_id, to_slot, from_num)

        if take_percent < 1 and not to_item:
            # 处理分堆
            to_num = int(from_item.get("count") * take_percent)
            from_num = int(from_item.get("count")) - to_num
            from_item["count"] = to_num
            import copy
            to_item = copy.deepcopy(from_item)
            to_item["count"] = from_num
            if isinstance(to_slot, int):
                spawn_item_to_player_inv(to_item, player_id, to_slot)
            if isinstance(from_slot, int):
                spawn_item_to_player_inv(from_item, player_id, from_slot)

        exchange_player_inv_item(player_id, from_slot, to_slot)

    args["from_item"] = from_item
    args["to_item"] = to_item
    notify_to_client(player_id, 'OnItemSwapServerEvent', args)
