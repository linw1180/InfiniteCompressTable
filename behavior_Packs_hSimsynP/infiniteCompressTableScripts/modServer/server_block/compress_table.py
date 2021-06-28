# -*- coding: utf-8 -*-
import copy
import json

from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modCommon.utils import item_utils
from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer, get_player_all_items, \
    spawn_item_to_player_inv, get_player_item, set_player_inv_item_num, get_item_basic_info
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
        print '========= server ===> on_custom_container_item_swap ========= args =', args
        player_id = args['player_id']
        block_name = args['block_name']
        from_slot = args['from_slot']
        to_slot = args['to_slot']
        from_item = args['from_item']
        to_item = args['to_item']
        take_percent = args['take_percent']
        from_item_detail_text = args['from_item_detail_text']

        # 存储放入框到背包物品中已压缩和未压缩的物品数量
        # count_data = {'no_compress_count': 0, 'have_compress_count': []}

        # 执行到此处说明此次交换必定有一个自定义槽位存在
        # 因为自定义槽位名是str，背包槽位名是int所以做如下判断

        # 输出框不允许放入操作
        if isinstance(to_slot, str) and to_slot == 'output_slot':
            return False

        # 两个自定义槽位之间不允许交换
        if isinstance(from_slot, str) and isinstance(to_slot, str):
            return False

        # 从放入框和输出框中取，不允许取出到有物品的背包槽位（因为取出数量非常可能超过64）
        if isinstance(to_slot, int) and to_item:
            return False

        # 背包 ===》放入框
        if isinstance(from_slot, int) and to_slot == 'input_slot':

            # 只支持一键放入，不支持分堆
            if take_percent < 1:
                return False

            # 当背包槽和放入框中均有物品，而且两个物品不一样时，不允许交换
            # 判断思路：根据默认count=1的原始物品信息字典是否相同来判断
            if from_item and to_item and from_item['extraId']:  # 背包槽物品已压缩
                from_item_dict = json.loads(from_item['extraId'])
                to_item_dict = json.loads(to_item['extraId'])
                if from_item_dict['item_dict'] != to_item_dict['item_dict']:
                    return False

            # 当背包槽和放入框中均有物品，而且两个物品不一样时，不允许交换
            # 判断思路：根据默认count=1的原始物品信息字典是否相同来判断
            if from_item and to_item and not from_item['extraId']:  # 背包槽物品未压缩
                temp_item = copy.deepcopy(from_item)
                temp_item['count'] = 1
                to_item_dict = json.loads(to_item['extraId'])
                if temp_item != to_item_dict['item_dict']:
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

        # ------------------------ 下面必须实时处理背包内的数据（增加，减少，归零等...） --------------------------

        # 输出框 ==》背包（只存在直接取出的情况）
        if from_slot == 'output_slot' and isinstance(to_slot, int):
            if take_percent < 1:  # 不允许分堆取出
                return False
            if take_percent == 1 and not to_item:

                # region 设置生成压缩物品的相关数据，主要设置 count tips extraId
                # 最初from_item数据
                from_item_copy = copy.deepcopy(from_item)

                # json字符串 ==》python对象
                data = json.loads(from_item['extraId'])
                # 将存储在extraId中最原始的物品信息赋给from_item
                from_item = data['item_dict']
                from_item['count'] = 1

                tips = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(data['compress_count']) + "§r"
                from_item['customTips'] = tips

                from_item['extraId'] = from_item_copy['extraId']

                spawn_item_to_player_inv(from_item, player_id, to_slot)
                # 最新的物品数据传送到客户端进行交换
                from_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                # endregion

        # 背包 ==》放入框
        elif isinstance(from_slot, int) and to_slot == 'input_slot':
            # 当放入框中没有物品时
            if take_percent == 1 and not to_item:

                if not from_item['extraId']:
                    # 处理：未压缩物品放入
                    # 处理思路：将待压缩数量和原始物品字典存入到extraId中，count默认均设置为1
                    temp_item = copy.deepcopy(from_item)
                    compress_count = temp_item['count']

                    # 处理存入extraId中count_data中数据，放入框到背包生成物品使用
                    no_compress_count = 0
                    no_compress_count += compress_count

                    from_item['count'] = 1
                    temp_item['count'] = 1

                    data = {'item_dict': temp_item, 'compress_count': compress_count, 'count_data': {'no_compress_count': no_compress_count, 'have_compress_count': []}}
                    # python对象 --》json字符串
                    str_extra_id = json.dumps(data)
                    # extraId存储数据类型必须为字符串
                    from_item['extraId'] = str_extra_id
                else:
                    # 处理：已压缩物品放入
                    # 思路：count设置为1、customTips设置为空、userData设置为None
                    from_item['count'] = 1
                    from_item['customTips'] = ''
                    # 已压缩物品需要同时处理 customTips 和 userData
                    from_item['userData'] = None

                    # 处理存入extraId中count_data中数据，放入框到背包生成物品使用
                    d = json.loads(from_item['extraId'])
                    have_compress_count = []
                    have_compress_count.append(d['compress_count'])
                    d['count_data'] = {'no_compress_count': 0, 'have_compress_count': have_compress_count}
                    str_data = json.dumps(d)
                    from_item['extraId'] = str_data

                # 处理背包数据，清空指定槽位物品
                set_player_inv_item_num(player_id, from_slot, 0)

            # 当放入框中有物品，并且和背包槽物品相同时，处理堆叠
            # 处理思路：物品是否相同主要根据count=1的物品信息字典是否相同来判断
            elif take_percent == 1 and to_item and (not from_item['extraId']):  # 背包槽为未压缩物品
                t_item = copy.deepcopy(from_item)
                t_item['count'] = 1
                item_dict_obj = json.loads(to_item['extraId'])

                if t_item == item_dict_obj['item_dict']:  # 未压缩物品和放入框物品相同
                    compress_count = from_item['count'] + item_dict_obj['compress_count']
                    temp_count = from_item['count']
                    from_item['count'] = 1
                    from_item['customTips'] = ''
                    # 处理存入extraId中count_data中数据，放入框到背包生成物品使用
                    item_dict_obj['count_data']['no_compress_count'] += temp_count
                    data = {'item_dict': t_item, 'compress_count': compress_count, 'count_data': item_dict_obj['count_data']}

                    str_extra_id = json.dumps(data)
                    from_item['extraId'] = str_extra_id
                    to_item = None
                    set_player_inv_item_num(player_id, from_slot, 0)

            # 当放入框中有物品，并且和背包槽物品相同时，处理堆叠
            # 处理思路：物品是否相同主要根据count=1的物品信息字典是否相同来判断
            elif take_percent == 1 and to_item and from_item['extraId']:  # 背包槽为已压缩物品
                from_item_dict = json.loads(from_item['extraId'])
                to_item_dict = json.loads(to_item['extraId'])
                new_compress_count = from_item_dict['compress_count'] + to_item_dict['compress_count']

                # 处理存入extraId中count_data中数据，放入框到背包生成物品使用
                to_item_dict['count_data']['have_compress_count'].append(from_item_dict['compress_count'])

                from_item['count'] = 1
                from_item['customTips'] = ''
                from_item['userData'] = None
                new_extra_id = {'item_dict': from_item_dict['item_dict'], 'compress_count': new_compress_count, 'count_data': to_item_dict['count_data']}
                str_extra_id = json.dumps(new_extra_id)
                from_item['extraId'] = str_extra_id
                to_item = None
                set_player_inv_item_num(player_id, from_slot, 0)

            # if item_utils.is_same_item(from_item, to_item):
            #     basic_info = get_item_basic_info(to_item.get("itemName"), to_item.get("auxValue"))
            #     if not basic_info:
            #         return
            #     # max_size = basic_info.get("maxStackSize")
            #     take_num = int(from_item.get("count") * take_percent)
            #     from_num = from_item.get("count")
            #     to_num = to_item.get("count")
            #     if not take_num and not to_num:
            #         return
            #     # if to_num == max_size:
            #     #     return
            #     # if to_num + take_num >= max_size:
            #     #     from_num -= max_size - to_num
            #     #     to_num = max_size
            #     # else:
            #     #     to_num += take_num
            #     #     from_num -= take_num
            #
            #     all_count = to_num + from_num
            #     to_num = all_count
            #     from_num = 0
            #
            #     from_item["count"] = to_num
            #     to_item["count"] = from_num
            #     if from_num == 0:
            #         to_item = None
            #     if isinstance(from_slot, int):
            #         set_player_inv_item_num(player_id, from_slot, from_num)
            #     if isinstance(to_slot, int):
            #         # 此处需要处理两种情况
            #         # 当未压缩数小于64和未压缩数大于64
            #         # set_player_inv_item_num(player_id, to_slot, 1)
            #         pass

        # 放入框 ==》背包
        elif isinstance(from_slot, str) and from_slot == 'input_slot':
            print '--------------- linwei ------------------- to_item =', to_item
            # 设置物品自定义tips和标识符
            # 只有在存在空余槽位时才被允许放入背包
            if take_percent == 1 and not to_item:
                # spawn_item_to_player_inv(from_item, player_id, to_slot)

                from_item_dict = json.loads(from_item['extraId'])
                no_compress_count = from_item_dict['count_data']['no_compress_count']
                have_compress_count = from_item_dict['count_data']['have_compress_count']

                # 未压缩物品生成到背包
                if no_compress_count != 0:
                    temp_item = copy.deepcopy(from_item)
                    temp_item['count'] = no_compress_count
                    temp_item['extraId'] = ''
                    spawn_item_to_player_inv(temp_item, player_id, to_slot)
                    args["from_item"] = temp_item
                    args["to_item"] = to_item
                    notify_to_client(player_id, 'OnItemSwapServerEvent', args)

                # 已压缩物品生成到背包
                if have_compress_count:
                    for i in have_compress_count:
                        temp_item = copy.deepcopy(from_item)
                        # json字符串 ==》python对象
                        data = json.loads(temp_item['extraId'])
                        data.pop('count_data')
                        # 将存储在extraId中最原始的物品信息赋给last_item
                        last_item = data['item_dict']
                        last_item['count'] = 1
                        tips = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(data['compress_count']) + "§r"
                        last_item['customTips'] = tips
                        data['compress_count'] = i
                        last_extra_id = json.dumps(data)
                        last_item['extraId'] = last_extra_id
                        spawn_item_to_player_inv(last_item, player_id, to_slot)  # FIXME 压缩物品生成到哪个槽位问题待解决
                        # 最新的物品数据传送到客户端进行交换
                        last_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                        args["from_item"] = last_item
                        args["to_item"] = to_item
                        notify_to_client(player_id, 'OnItemSwapServerEvent', args)

                return False

                        # # region 设置生成压缩物品的相关数据，主要设置 count tips extraId
                        # # 最初from_item数据
                        # from_item_copy = copy.deepcopy(from_item)
                        #
                        # # json字符串 ==》python对象
                        # data = json.loads(from_item['extraId'])
                        # # 将存储在extraId中最原始的物品信息赋给from_item
                        # from_item = data['item_dict']
                        # from_item['count'] = 1
                        #
                        # tips = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(data['compress_count']) + "§r"
                        # from_item['customTips'] = tips
                        #
                        # from_item['extraId'] = from_item_copy['extraId']
                        #
                        # spawn_item_to_player_inv(from_item, player_id, to_slot)
                        # # 最新的物品数据传送到客户端进行交换
                        # from_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                        # # endregion

            if take_percent < 1:  # 输入框取出不允许分堆操作
                return False

        args["from_item"] = from_item
        args["to_item"] = to_item
        notify_to_client(player_id, 'OnItemSwapServerEvent', args)
        return False

    # @staticmethod
    # def set_item_custom_tips(player_id, slot, compress_count):
    #     item_dict = get_player_item(player_id, ItemPosType.INVENTORY, slot)
    #
    #     # if not item_dict or item_dict['customTips']:
    #     #     return
    #     if not item_dict:
    #         return
    #
    #     tips = "已压缩数量 " + "§b§o" + str(compress_count) + "§r"
    #
    #     extra_id_dict = {"compress_count": compress_count, "item_dict": item_dict}
    #     # python对象 --》json字符串
    #     str_extra_id = json.dumps(extra_id_dict)
    #     # 修改玩家物品的自定义tips和自定义标识符
    #     ret = change_player_item_tips_and_extra_id(player_id, ItemPosType.INVENTORY, slot, tips, str_extra_id)
    #     print '---------------- set_item_custom_tips ------------------ ret =', ret
