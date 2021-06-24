# -*- coding: utf-8 -*-
import copy
import json

from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modCommon.utils import item_utils
from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer, get_player_all_items, \
    spawn_item_to_player_inv, get_player_item, set_player_inv_item_num, change_player_item_tips_and_extra_id, \
    get_item_basic_info
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
        notify_to_client(player_id, 'UpdateBlockUI', {
            'block_name': block_name,
            'inventory': inv_items,
        })

    @classmethod
    def on_custom_container_item_swap(cls, args):
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

        # 从放入框和输出框中取，不允许取出到有物品的背包槽位（因为取出数量非常可能超过64）
        if isinstance(to_slot, int) and to_item:
            return False

        # 背包到放入框
        if isinstance(from_slot, int) and to_slot == 'input_slot':
            # 只支持一键放入，不支持分堆
            if take_percent < 1:
                return False
            # 当两个物品不一样，而且放入框中还有物品时（不允许交换，因为放入框物品数可能非常多）
            if not item_utils.is_same_item(from_item, to_item) and to_item:
                return False

        # 压缩台暂时不支持分堆操作
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

        # 背包 ===》放入框 槽位
        # 两个槽位物品相同时处理堆叠（只对从背包到放入框起作用，因为放入框不允许取出到有物品的槽位）
        if item_utils.is_same_item(from_item, to_item):
            basic_info = get_item_basic_info(to_item.get("itemName"), to_item.get("auxValue"))
            if not basic_info:
                return
            # max_size = basic_info.get("maxStackSize")
            take_num = int(from_item.get("count") * take_percent)
            from_num = from_item.get("count")
            to_num = to_item.get("count")
            if not take_num and not to_num:
                return
            # if to_num == max_size:
            #     return
            # if to_num + take_num >= max_size:
            #     from_num -= max_size - to_num
            #     to_num = max_size
            # else:
            #     to_num += take_num
            #     from_num -= take_num

            all_count = to_num + from_num
            to_num = all_count
            from_num = 0

            from_item["count"] = to_num
            to_item["count"] = from_num
            if from_num == 0:
                to_item = None
            if isinstance(from_slot, int):
                set_player_inv_item_num(player_id, from_slot, from_num)
            if isinstance(to_slot, int):
                # 此处需要处理两种情况
                # 当未压缩数小于64和未压缩数大于64
                # set_player_inv_item_num(player_id, to_slot, 1)
                pass

        # 只对从背包到放入框起作用
        # if item_utils.is_same_item(from_item, to_item):
        #     # 两个槽物品相同时处理堆叠
        #     basic_info = get_item_basic_info(to_item.get("itemName"), to_item.get("auxValue"))
        #     if not basic_info:
        #         return
        #     max_size = basic_info.get("maxStackSize")
        #     take_num = int(from_item.get("count") * take_percent)
        #     from_num = from_item.get("count")
        #     to_num = to_item.get("count")
        #     if not take_num and not to_num:
        #         return
        #     if to_num == max_size:
        #         return
        #     if to_num + take_num >= max_size:
        #         from_num -= max_size - to_num
        #         to_num = max_size
        #     else:
        #         to_num += take_num
        #         from_num -= take_num
        #     from_item["count"] = to_num
        #     to_item["count"] = from_num
        #     if from_num == 0:
        #         to_item = None
        #     if isinstance(from_slot, int):
        #         set_player_inv_item_num(player_id, from_slot, from_num)
        #     if isinstance(to_slot, int):
        #         set_player_inv_item_num(player_id, to_slot, to_num)

        # ------------------------ 下面必须实时处理背包内的数据（增加，减少，归零等...） --------------------------

        # 输出框 ==》背包（只存在直接取出的情况）
        if from_slot == 'output_slot' and isinstance(to_slot, int):
            if take_percent < 1:  # 不允许分堆取出
                return False
            if take_percent == 1 and not to_item:
                # 背包指定槽位无数据，需要手动进行生成
                temp_item = copy.deepcopy(from_item)
                temp_item['count'] = 1
                spawn_item_to_player_inv(temp_item, player_id, to_slot)
                # 设置物品自定义tips和标识符
                cls.set_item_custom_tips(player_id, to_slot, from_item['count'])
        # 背包 ==》放入框
        elif isinstance(from_slot, int) and to_slot == 'input_slot':
            # 当放入框为没有物品时
            if take_percent == 1 and not to_item:
                # 处理背包数据，清空指定槽位物品
                set_player_inv_item_num(player_id, from_slot, 0)
                # 设置物品自定义tips和标识符
                # cls.set_item_custom_tips(player_id, from_slot, from_item['count'])
        # 放入框 ==》背包
        elif isinstance(from_slot, str) and from_slot == 'input_slot':
            to_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
            # 设置物品自定义tips和标识符
            # cls.set_item_custom_tips({'player_id': player_id, 'slot': to_slot, 'count': 20})
            # 只有在存在空余槽位时才被允许放入背包
            if take_percent == 1 and not to_item:
                spawn_item_to_player_inv(from_item, player_id, to_slot)
            if take_percent < 1:  # 输入框取出不允许分堆操作
                return False
        notify_to_client(player_id, 'OnItemSwapServerEvent', args)
        return False

    @staticmethod
    def set_item_custom_tips(player_id, slot, count):
        # player_id = args['player_id']
        # slot = args['slot']
        # count = args['count']
        item_dict = get_player_item(player_id, ItemPosType.INVENTORY, slot)

        # if not item_dict or item_dict['customTips']:
        #     return
        if not item_dict:
            return

        # from_item = {'itemId': -745, 'count': 1, 'modItemId': '', 'enchantData': [], 'durability': 0,
        #              'customTips': '\xe5\xb7\xb2\xe5\x8e\x8b\xe7\xbc\xa9\xe6\x95\xb0\xe9\x87\x8f \xc2\xa7b\xc2\xa7o128\xc2\xa7r',
        #              'extraId': '{"cus_tips": "\\u5df2\\u538b\\u7f29\\u6570\\u91cf \\u00a7b\\u00a7o128\\u00a7r", "new_count": 128}',
        #              'modId': '', 'userData': {'ItemExtraID': {'__type__': 8,
        #                                                        '__value__': '{"cus_tips": "\\u5df2\\u538b\\u7f29\\u6570\\u91cf \\u00a7b\\u00a7o128\\u00a7r", "new_count": 128}'},
        #                                        'ItemCustomTips': {'__type__': 8,
        #                                                           '__value__': '\xe5\xb7\xb2\xe5\x8e\x8b\xe7\xbc\xa9\xe6\x95\xb0\xe9\x87\x8f \xc2\xa7b\xc2\xa7o128\xc2\xa7r'}},
        #              'isDiggerItem': False, 'itemName': 'xl:block_limited_compress_table', 'auxValue': 0,
        #              'showInHand': True}

        # item_name = item_dict['itemName']
        # if item_name in ITEM_CUSTOM_TIPS:
        #     cn_name = get_item_basic_info(item_name)['itemName']
        #     tips = cn_name + '\n' + ITEM_CUSTOM_TIPS[item_name]

        tips = "已压缩数量 " + "§b§o" + str(count) + "§r"

        extra_id_dict = {'new_count': count, 'cus_tips': tips}
        # python对象 --》json字符串
        str_extra_id = json.dumps(extra_id_dict)
        # 修改玩家物品的自定义tips和自定义标识符
        print '99999', change_player_item_tips_and_extra_id(player_id, ItemPosType.INVENTORY, slot, tips, str_extra_id)
