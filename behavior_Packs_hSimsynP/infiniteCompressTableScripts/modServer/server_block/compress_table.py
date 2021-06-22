# -*- coding: utf-8 -*-
from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer, get_player_all_items, \
    spawn_item_to_player_inv, set_extra_data
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
        """
        与附魔台的附魔槽位进行物品交换
        :param from_item:
        :param to_item:
        :param args:
        :return:
        """
        print '=================== on_custom_container_item_swap ====================== args =', args
        player_id = args['player_id']
        block_name = args['block_name']
        from_slot = args['from_slot']
        to_slot = args['to_slot']
        from_item = args['from_item']
        to_item = args['to_item']
        # logger.info("custom_container_item_swap=={}-+{}".format(isinstance(from_slot, str), isinstance(to_slot, str)))
        # logger.info("custom_swap_item==={}:{}".format(to_item, from_item))
        # 因为自定义槽位名是str，背包槽位名是int所以做如下判断

        # 执行到此处说明此次交换必定有一个自定义槽位存在----------

        # 输出框不允许放入操作
        if isinstance(to_slot, str) and to_slot == 'output_slot':
            return False

        # 两个自定义槽位之间不允许交换
        if isinstance(from_slot, str) and isinstance(to_slot, str):
            return False

        # 输出框 ==》背包 TODO 取出逻辑待写
        if isinstance(from_slot, str) and from_slot == 'output_slot':
            pass
        # 背包 ==》放入框
        elif isinstance(from_slot, int) and isinstance(to_slot, str):
            spawn_item_to_player_inv(from_item, player_id, from_slot)
            set_extra_data(player_id, "to_enchant_equipment", to_item)
            to_enchant_item = to_item
        # 放入框 ==》背包
        elif isinstance(from_slot, str) and isinstance(to_slot, int):
            if to_item is not None:
                spawn_item_to_player_inv(to_item, player_id, to_slot)
                set_extra_data(player_id, "to_enchant_equipment", from_item)
                to_enchant_item = from_item
                print '111111111111111111111'
            else:
                spawn_item_to_player_inv(from_item, player_id, to_slot)
            # notify_to_client(player_id, "OnEnchantSlotItem", {
        #     "to_enchant_equipment": to_enchant_item,
        #     ""
        #     "block_name": block_name
        # })
        args["from_item"] = to_item
        args["to_item"] = from_item
        notify_to_client(player_id, 'OnItemSwapServerEvent', args)
        return True

        # if to_item.get("count") > 1 or from_item.get('count') > 1:
        #     return False
        # # logger.info("to_enchant_equipment:{}".format(to_enchant_equipment))
        # if isinstance(from_slot, int):
        #     # logger.info("=======from_bag_to_slot-{}''{}".format(to_item, from_item))
        #     spawn_item_to_player_inv(from_item, player_id, from_slot)
        #     set_extra_data(player_id, "to_enchant_equipment", to_item)
        #     to_enchant_item = to_item
        #
        # else:
        #     # logger.info("-----swap_items=={},,,{}".format(to_item, to_enchant_equipment))
        #     spawn_item_to_player_inv(to_item, player_id, to_slot)
        #     set_extra_data(player_id, "to_enchant_equipment", from_item)
        #     to_enchant_item = from_item
        # # if to_enchant_item:
        # notify_to_client(player_id, "OnEnchantSlotItem", {
        #     "to_enchant_equipment": to_enchant_item,
        #     ""
        #     "block_name": block_name
        # })
        # args["from_item"] = to_item
        # args["to_item"] = from_item
        # notify_to_client(player_id, 'OnItemSwapServerEvent', args)
        # return True
