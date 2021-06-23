# -*- coding: utf-8 -*-
from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modCommon.utils import item_utils
from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer, get_player_all_items, \
    spawn_item_to_player_inv, get_player_item, set_player_inv_item_num
from infiniteCompressTableScripts.modServer.server_block._block import Block


class CompressTable(Block):

    @classmethod
    def player_use_block(cls, args):
        player_id = args['playerId']
        block_name = args['blockName']
        pos = (args['x'], args['y'], args['z'])
        dimension = args['dimensionId']

        if not player_id:
            return

        # 打开UI
        notify_to_client(player_id, 'OpenBlockUI', {
            "block_name": block_name,
            "pos": pos,
            "dimension": dimension,
            # "equipped_items": player.equipped_items.items,
            # "eu": block_entity_data['eu'],
        })
        add_timer(0.1, cls.update_inventory_ui, player_id, block_name)

    @staticmethod
    def update_inventory_ui(player_id, block_name):
        inv_items = get_player_all_items(player_id, ItemPosType.INVENTORY, True)
        print '++++++++++++++++++++++++++++++ inv_items =', inv_items
        notify_to_client(player_id, 'UpdateBlockUI', {
            'block_name': block_name,
            'inventory': inv_items,
        })

    @staticmethod
    def on_custom_container_item_swap(args):
        print '=================== on_custom_container_item_swap ====================== args =', args
        player_id = args['player_id']
        block_name = args['block_name']
        from_slot = args['from_slot']
        to_slot = args['to_slot']
        from_item = args['from_item']
        to_item = args['to_item']
        take_percent = args['take_percent']
        # logger.info("custom_container_item_swap=={}-+{}".format(isinstance(from_slot, str), isinstance(to_slot, str)))
        # logger.info("custom_swap_item==={}:{}".format(to_item, from_item))
        # 因为自定义槽位名是str，背包槽位名是int所以做如下判断

        # 执行到此处说明此次交换必定有一个自定义槽位存在----------
        test = {'from_slot': 34, 'block_name': 'xl:block_compress_table',
                'from_item': {'itemId': 61, 'count': 3, 'isDiggerItem': False, 'enchantData': [], 'durability': 0,
                              'customTips': '', 'extraId': '', 'modId': '', 'userData': None, 'modItemId': '',
                              'itemName': 'minecraft:furnace', 'auxValue': 0, 'showInHand': True},
                'to_item': {'itemId': -159, 'count': 55, 'isDiggerItem': False, 'enchantData': [], 'durability': 0,
                            'customTips': '', 'extraId': '', 'modId': '', 'userData': None, 'modItemId': '',
                            'itemName': 'minecraft:turtle_egg', 'auxValue': 0, 'showInHand': True},
                'to_slot': 'input_slot', 'player_id': '-38654705663', 'block_pos': (3059, 68, 16), 'take_percent': 1,
                'dimension': 0}

        # 输出框不允许放入操作
        if isinstance(to_slot, str) and to_slot == 'output_slot':
            return False

            # 两个自定义槽位之间不允许交换
        if isinstance(from_slot, str) and isinstance(to_slot, str):
            return False

        # 只允许背包栏位为空的时候取出，不能从输入栏位替换到背包栏位
        if isinstance(to_slot, int) and to_item:
            return False

        # 压缩台暂时不进行分堆操作
        # if take_percent < 1 and not to_item:
        #     # 简单处理分堆
        #     to_num = int(from_item.get("count") * take_percent)
        #     from_num = int(from_item.get("count")) - to_num
        #     from_item["count"] = to_num
        #     import copy
        #     to_item = copy.deepcopy(from_item)
        #     to_item["count"] = from_num
        #     if isinstance(to_slot, int):
        #         spawn_item_to_player_inv(to_item, player_id, to_slot)
        #     if isinstance(from_slot, int):
        #         spawn_item_to_player_inv(from_item, player_id, from_slot)

        # 输出框 ==》背包（只存在直接取出的情况）
        if isinstance(from_slot, str) and from_slot == 'output_slot':
            to_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
            # 设置物品自定义tips和标识符
            # cls.set_item_custom_tips({'player_id': player_id, 'slot': to_slot, 'count': from_item['count']})
            # set_item_custom_tips({'player_id': player_id, 'slot': to_slot})
            if take_percent == 1 and not to_item:
                spawn_item_to_player_inv(from_item, player_id, to_slot)
        # 背包 ==》放入框
        elif isinstance(from_slot, int) and to_slot == 'input_slot':
            from_item = get_player_item(player_id, ItemPosType.INVENTORY, from_slot, True)
            # 放入框为没有物品时
            if take_percent == 1 and not to_item:
                set_player_inv_item_num(player_id, from_slot, 0)
                # 如果两个物品不一样，而且放入框中还有物品
            if not item_utils.is_same_item(from_item, to_item) and to_item:
                spawn_item_to_player_inv(to_item, player_id, from_slot)
        # 放入框 ==》背包
        elif isinstance(from_slot, str) and from_slot == 'input_slot':
            to_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
            # set_item_custom_tips({'player_id': player_id, 'slot': to_slot, 'count': 20})
            # 只有在存在空余槽位时才被允许放入背包
            if take_percent == 1 and not to_item:
                spawn_item_to_player_inv(from_item, player_id, to_slot)
        notify_to_client(player_id, 'OnItemSwapServerEvent', args)
        return False
