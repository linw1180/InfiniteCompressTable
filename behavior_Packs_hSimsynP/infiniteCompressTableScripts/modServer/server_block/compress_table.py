# -*- coding: utf-8 -*-
from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modCommon.utils import item_utils
from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer, get_player_all_items, \
    spawn_item_to_player_inv, set_extra_data, get_extra_data, get_player_item, get_item_basic_info, \
    set_player_inv_item_num
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

    # copy
    # @staticmethod
    # def on_custom_container_item_swap(args):
    #     player_id = args['player_id']
    #     from_slot = args['from_slot']
    #     to_slot = args['to_slot']
    #     from_item = args['from_item']
    #     to_item = args['to_item']
    #     take_percent = args['take_percent']
    #     # page = str(args['pages'])
    #     f_slot = 1
    #     t_slot = 1
    #
    #     # bag_info = get_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey))
    #
    #     if isinstance(from_slot, str):
    #         f_slot = int(from_slot.split("item_btn")[1])
    #         # from_item = bag_info[page][f_slot - 1]
    #
    #     if isinstance(to_slot, str):
    #         t_slot = int(to_slot.split("item_btn")[1])
    #         # to_item = bag_info[page][t_slot - 1]
    #
    #     if isinstance(to_slot, int):
    #         to_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
    #
    #     if isinstance(from_slot, int):
    #         from_item = get_player_item(player_id, ItemPosType.INVENTORY, from_slot, True)
    #
    #     if item_utils.is_same_item(from_item, to_item):
    #         # 两个槽物品相同时处理堆叠
    #         basic_info = get_item_basic_info(to_item.get("itemName"), to_item.get("auxValue"))
    #         if not basic_info:
    #             return
    #         max_size = basic_info.get("maxStackSize")
    #         take_num = int(from_item.get("count") * take_percent)
    #         from_num = from_item.get("count")
    #         to_num = to_item.get("count")
    #         if not take_num and not to_num:
    #             return
    #         if to_num == max_size:
    #             return
    #         if to_num + take_num >= max_size:
    #             from_num -= max_size - to_num
    #             to_num = max_size
    #         else:
    #             to_num += take_num
    #             from_num -= take_num
    #         from_item["count"] = to_num
    #         to_item["count"] = from_num
    #         if from_num == 0:
    #             to_item = None
    #         if isinstance(from_slot, int):
    #             set_player_inv_item_num(player_id, from_slot, from_num)
    #         if isinstance(to_slot, int):
    #             set_player_inv_item_num(player_id, to_slot, to_num)
    #         if isinstance(from_slot, str):
    #             # bag_info[page][f_slot - 1] = to_item
    #             # set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #             pass
    #         if isinstance(to_slot, str):
    #             # bag_info[page][t_slot - 1] = from_item
    #             # set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #             pass
    #     if take_percent < 1 and not to_item:
    #         # 处理分堆
    #         to_num = int(from_item.get("count") * take_percent)
    #         from_num = int(from_item.get("count")) - to_num
    #         from_item["count"] = to_num
    #         import copy
    #         to_item = copy.deepcopy(from_item)
    #         to_item["count"] = from_num
    #         if isinstance(to_slot, int):
    #             spawn_item_to_player_inv(to_item, player_id, to_slot)
    #
    #         if isinstance(from_slot, int):
    #             spawn_item_to_player_inv(to_item, player_id, from_slot)
    #
    #         if isinstance(from_slot, str):
    #             # bag_info[page][f_slot - 1] = to_item
    #             # set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #             pass
    #
    #         if isinstance(to_slot, str):
    #             # bag_info[page][t_slot - 1] = from_item
    #             # set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #             pass
    #
    #     if isinstance(to_slot, str) and isinstance(from_slot, str):
    #         if take_percent == 1 and not to_item:
    #             tem_args = args['flag'].split('/main_panel/panel0/grid1')
    #             if not tem_args[0]:
    #                 # bag_info[page][t_slot - 1] = args['from_item']
    #                 search_data = args['search_data']['search_item']
    #
    #                 for item in search_data:
    #                     if item == args['from_item']:
    #                         search_data.remove(item)
    #
    #                 set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #                 notify_to_client(player_id, 'UpdateBlockUI', {
    #                     'block_name': args['block_name'],
    #                     # 'eu': bag_info[page],
    #                     'search_item': search_data,
    #                     'state': True
    #                 })
    #                 return False
    #             bag_info[page][t_slot - 1] = from_item
    #             bag_info[page][f_slot - 1] = None
    #             set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #         if not item_utils.is_same_item(from_item, to_item) and to_item:
    #             tem_args = args['flag'].split('/main_panel/panel0/grid1')
    #             if not tem_args[0]:
    #                 return False
    #             bag_info[page][t_slot - 1] = from_item
    #             bag_info[page][f_slot - 1] = to_item
    #             set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #
    #     # 从末影台向背包传数据
    #     if isinstance(from_slot, str) and isinstance(to_slot, int):
    #         if take_percent == 1 and not to_item:
    #             spawn_item_to_player_inv(from_item, player_id, to_slot)
    #             bag_info[page][f_slot - 1] = None
    #             set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #         if not item_utils.is_same_item(from_item, to_item) and to_item:
    #             spawn_item_to_player_inv(from_item, player_id, to_slot)
    #             bag_info[page][f_slot - 1] = to_item
    #             set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #     # 从背包向末影台
    #     if isinstance(to_slot, str) and isinstance(from_slot, int):
    #         if take_percent == 1 and not to_item:
    #             set_player_inv_item_num(player_id, from_slot, 0)
    #             bag_info[page][t_slot - 1] = from_item
    #             set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #         if not item_utils.is_same_item(from_item, to_item) and to_item:
    #             spawn_item_to_player_inv(to_item, player_id, from_slot)
    #             bag_info[page][t_slot - 1] = from_item
    #             set_extra_data(player_id, '{prefix}.{name}'.format(prefix=ModName, name=ModKey), bag_info)
    #
    #     args["from_item"] = from_item
    #     args["to_item"] = to_item
    #     notify_to_client(player_id, 'OnItemSwapServerEvent', args)
    #
    #     return False

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
            print '000000000'
            # spawn_item_to_player_inv(from_item, player_id, from_slot)
            # set_extra_data(player_id, "to_enchant_equipment", to_item)
            # to_enchant_item = to_item
        # 放入框 ==》背包
        elif isinstance(from_slot, str) and isinstance(to_slot, int):
            if to_item is not None:
                spawn_item_to_player_inv(to_item, player_id, to_slot)
                set_extra_data(player_id, "to_enchant_equipment", from_item)
                to_enchant_item = from_item
                print '111111111111111111111'
            else:
                print '222222222222222222222222'
                spawn_item_to_player_inv(from_item, player_id, to_slot)
            # notify_to_client(player_id, "OnEnchantSlotItem", {
        #     "to_enchant_equipment": to_enchant_item,
        #     ""
        #     "block_name": block_name
        # })
        args["from_item"] = to_item
        args["to_item"] = from_item
        print '-------------- after -------------------- from_item =', args["from_item"]
        print '-------------- after -------------------- to_item =', args["to_item"]
        # notify_to_client(player_id, 'OnItemSwapServerEvent', args)
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
