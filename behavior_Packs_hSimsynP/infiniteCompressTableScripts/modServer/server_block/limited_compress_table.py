# -*- coding: utf-8 -*-
import json

from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer, get_player_all_items, \
    spawn_item_to_player_inv, get_player_item, set_player_inv_item_num
from infiniteCompressTableScripts.modServer.server_block._block import Block


class LimitedCompressTable(Block):

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
        player_id = args['player_id']
        block_name = args['block_name']
        from_slot = args['from_slot']
        to_slot = args['to_slot']
        from_item = args['from_item']
        to_item = args['to_item']
        take_percent = args['take_percent']
        from_item_detail_text = args['from_item_detail_text']

        # 执行到此处说明此次交换必定有一个自定义槽位存在
        # 因为自定义槽位名是str，背包槽位名是int所以做如下判断

        # region 解压缩工作台相关操作限制条件
        # 输出框不允许放入操作
        if isinstance(to_slot, str) and to_slot == 'output_slot':
            return False
        # 输出框不允许取出操作
        if isinstance(from_slot, str) and from_slot == 'output_slot':
            return False
        # 未压缩物品不允许放入（extraId存在的情况下，根据extraId中是否有compress_count作为是否压缩的判断条件）
        if isinstance(to_slot, str) and to_slot == 'input_slot':
            if not from_item['extraId']:
                # 发送事件到客户端，显示提示信息
                notify_to_client(player_id, 'ShowShortTimeMsg1Event', {'block_name': block_name})
                return False
            check_extra_id_dict = json.loads(from_item['extraId'])
            if not check_extra_id_dict['compress_count']:
                # 发送事件到客户端，显示提示信息
                notify_to_client(player_id, 'ShowShortTimeMsg1Event', {'block_name': block_name})
                return False
        # 当放入框中存在物品，不允许继续放入 
        if isinstance(to_slot, str) and to_slot == 'input_slot':
            if to_item:
                return False
        # 不允许分堆情况下进行交换
        if take_percent != 1:
            return False
        # 放入框中有压缩物品，不允许放入到有物品的背包槽位
        if from_slot == 'input_slot' and to_item:
            return False
        # endregion

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

        # ------------------------ 下面必须实时处理背包内的数据（增加，减少，归零等...） --------------------------

        # 背包中已压缩物品 ===》空的放入框
        if isinstance(from_slot, int) and to_slot == 'input_slot':
            # 前边已经筛选过数据，这里直接写已压缩物品放入到空的放入框的交换逻辑
            extra_id_dict = json.loads(from_item['extraId'])
            # 构建新的from_item
            from_item = extra_id_dict['item_dict']
            # 初始化tips，主要是为了初始化之前已压缩过物品中存在的tips数据
            from_item['customTips'] = ''
            new_extra_id_dict = {'item_dict': from_item, 'compress_count': extra_id_dict['compress_count']}
            str_dict_data = json.dumps(new_extra_id_dict)
            from_item['extraId'] = str_dict_data
            # 处理背包数据，清空指定槽位物品
            set_player_inv_item_num(player_id, from_slot, 0)

        # 放入框已压缩物品 ==》背包中无物品槽位
        elif isinstance(from_slot, str) and from_slot == 'input_slot':
            # 只需要设置物品自定义tips
            # json字符串 ==》python对象
            extra_id_dict = json.loads(from_item['extraId'])
            tips = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(extra_id_dict['compress_count']) + "§r"
            from_item['customTips'] = tips
            spawn_item_to_player_inv(from_item, player_id, to_slot)
            # 最新的物品数据传送到客户端进行交换
            from_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)

        args["from_item"] = from_item
        args["to_item"] = to_item
        notify_to_client(player_id, 'OnItemSwapServerEvent', args)
        return False
