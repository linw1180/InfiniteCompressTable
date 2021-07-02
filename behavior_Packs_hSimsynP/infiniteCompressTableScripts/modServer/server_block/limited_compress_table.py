# -*- coding: utf-8 -*-
import copy
import json

from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer, get_player_all_items, \
    spawn_item_to_player_inv, get_player_item, set_player_inv_item_num
from infiniteCompressTableScripts.modServer.server_block._block import Block


class LimitedCompressTable(Block):

    @classmethod
    def take_out_item(cls, args):
        from_item = args['from_item']
        from_slot = args['from_slot']
        to_slot = args['to_slot']
        take_out_num = args['take_out_num']
        player_id = args['player_id']
        block_name = args['block_name']
        empty_slot_list = args['empty_slot_list']

        # try：尝试处理取出逻辑

        # 根据取出数，将物品生成到背包空的槽位中
        extra_id_dict = json.loads(from_item['extraId'])
        # 原始item物品数据
        bag_item = extra_id_dict['item_dict']
        # 自定义容器中item物品数据
        container_item = copy.deepcopy(from_item)

        # 自定义槽位中剩余未解压缩数量
        remain_count = extra_id_dict['compress_count'] - take_out_num
        new_extra_id = extra_id_dict
        new_extra_id['compress_count'] = remain_count
        str_extra_id = json.dumps(new_extra_id)
        container_item['extraId'] = str_extra_id
        container_slot = from_slot
        notify_to_client(player_id, "OnItemProcessedServerEvent", {
            'item': container_item,
            'slot': container_slot,
            'block_name': block_name
        })

        if take_out_num <= 64:
            # 解压缩数量 <= 64，直接生成到该指定的空槽位
            bag_item['count'] = take_out_num
            spawn_item_to_player_inv(bag_item, player_id)
            bag_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
            bag_slot = to_slot
            notify_to_client(player_id, "OnItemProcessedServerEvent", {
                'item': bag_item,
                'slot': bag_slot,
                'block_name': block_name
            })
        else:
            # 解压缩数量 > 64，此时需要将物品分批生成到空余槽位
            # 需要生成的次数
            spawn_times = take_out_num / 64
            # 按照槽位生成后不足64的数量
            extra_count = take_out_num % 64
            for i in xrange(spawn_times):
                bag_item['count'] = 64
                spawn_slot = empty_slot_list[-1]
                spawn_item_to_player_inv(bag_item, player_id, spawn_slot)
                bag_item = get_player_item(player_id, ItemPosType.INVENTORY, spawn_slot, True)
                bag_slot = spawn_slot
                empty_slot_list.pop()
                notify_to_client(player_id, "OnItemProcessedServerEvent", {
                    'item': bag_item,
                    'slot': bag_slot,
                    'block_name': block_name
                })
            if extra_count != 0:
                bag_item['count'] = extra_count
                spawn_slot = empty_slot_list[-1]
                spawn_item_to_player_inv(bag_item, player_id)
                bag_item = get_player_item(player_id, ItemPosType.INVENTORY, spawn_slot, True)
                bag_slot = spawn_slot
                empty_slot_list.pop()
                notify_to_client(player_id, "OnItemProcessedServerEvent", {
                    'item': bag_item,
                    'slot': bag_slot,
                    'block_name': block_name
                })
        # 统一更新背包UI
        cls.update_inventory_ui(player_id, block_name)

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
        if isinstance(to_slot, str) and to_slot == 'input_slot' and to_item is None:
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

        # 分两种情况
        elif isinstance(from_slot, str) and from_slot == 'input_slot':
            # 处理取出
            if args.get('can_take_out'):
                extra_id_dict = json.loads(from_item['extraId'])
                compress_count = extra_id_dict['compress_count']

                copy_item = copy.deepcopy(from_item)
                temp_item = (json.loads(copy_item['extraId']))['item_dict']
                temp_item['count'] = compress_count
                spawn_item_to_player_inv(temp_item, player_id)
                temp_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                args["from_item"] = temp_item
                args["to_item"] = to_item
                notify_to_client(player_id, 'OnItemSwapServerEvent', args)
                # 更新背包UI
                cls.update_inventory_ui(player_id, block_name)
                return False

            if args.get('can_take_out_direct'):

                extra_id_dict = json.loads(from_item['extraId'])
                compress_count = extra_id_dict['compress_count']

                copy_item = copy.deepcopy(from_item)
                temp_item = (json.loads(copy_item['extraId']))['item_dict']
                temp_item['count'] = compress_count
                spawn_item_to_player_inv(temp_item, player_id)
                temp_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                args["from_item"] = temp_item
                args["to_item"] = to_item
                notify_to_client(player_id, 'OnItemSwapServerEvent', args)
                # 更新背包UI
                cls.update_inventory_ui(player_id, block_name)
                return False
            else:
                # 处理放入框已压缩物品 ==》背包中无物品槽位
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
