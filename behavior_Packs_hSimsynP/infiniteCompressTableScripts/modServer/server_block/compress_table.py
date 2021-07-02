# -*- coding: utf-8 -*-
import copy
import json

from mod.common.minecraftEnum import ItemPosType

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
                m_from_item_dict = json.loads(from_item['extraId'])
                m_dict = m_from_item_dict['item_dict']
                m_dict['customTips'] = ''
                m_to_item_dict = json.loads(to_item['extraId'])
                if m_dict != m_to_item_dict['item_dict']:
                    return False

            # 当背包槽和放入框中均有物品，而且两个物品不一样时，不允许交换
            # 判断思路：根据默认count=1的原始物品信息字典是否相同来判断
            if from_item and to_item and not from_item['extraId']:  # 背包槽物品未压缩
                n_temp_item = copy.deepcopy(from_item)
                n_temp_item['count'] = 1
                n_to_item_dict = json.loads(to_item['extraId'])
                if n_temp_item != n_to_item_dict['item_dict']:
                    return False

        # 背包 ==》放入框
        if isinstance(from_slot, int) and to_slot == 'input_slot':
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

                    data = {'item_dict': temp_item, 'compress_count': compress_count,
                            'count_data': {'no_compress_count': no_compress_count, 'have_compress_count': []}}
                    # python对象 --》json字符串
                    str_extra_id = json.dumps(data)
                    # extraId存储数据类型必须为字符串
                    from_item['extraId'] = str_extra_id
                else:
                    # 处理：已压缩物品放入
                    # 思路：直接获取extraId中item_dict，将item_dict作为基础item，在其基础上，设置新的extraId
                    from_item_dict = json.loads(from_item['extraId'])
                    # 构建新的from_item
                    from_item = from_item_dict['item_dict']
                    # 初始化tips，主要是为了初始化之前已压缩过物品中存在的tips数据
                    from_item['customTips'] = ''
                    have_compress_count = [from_item_dict['compress_count']]
                    new_extra_id_dict = {'item_dict': from_item_dict['item_dict'],
                                         'compress_count': from_item_dict['compress_count'],
                                         'count_data': {'no_compress_count': 0,
                                                        'have_compress_count': have_compress_count}}
                    str_dict_data = json.dumps(new_extra_id_dict)
                    from_item['extraId'] = str_dict_data

                # 处理背包数据，清空指定槽位物品
                set_player_inv_item_num(player_id, from_slot, 0)

            # 当放入框中有物品，并且和背包槽物品相同时，处理堆叠
            # 处理思路：物品是否相同主要根据count=1的物品信息字典是否相同来判断
            elif take_percent == 1 and to_item:

                # 背包槽为未压缩物品时，处理堆叠
                if not from_item['extraId']:  # 已默认未压缩物品和放入框物品相同
                    # 上边已经对两物品不同的情况做了筛选，能执行到此处说明是同一物品，只是压缩与否的问题
                    to_item_extra_id = json.loads(to_item['extraId'])
                    new_compress_count = from_item['count'] + to_item_extra_id['compress_count']
                    temp_count = from_item['count']
                    from_item['count'] = 1
                    # 处理存入extraId中count_data中数据，放入框到背包生成物品使用
                    to_item_extra_id['count_data']['no_compress_count'] += temp_count
                    data = {'item_dict': to_item_extra_id['item_dict'], 'compress_count': new_compress_count,
                            'count_data': to_item_extra_id['count_data']}
                    str_extra_id = json.dumps(data)
                    from_item['extraId'] = str_extra_id
                    to_item = None  # FIXME 可能会导致后边有问题
                    set_player_inv_item_num(player_id, from_slot, 0)

                # 背包槽为已压缩物品时，处理堆叠
                else:
                    # 上边已经对两物品不同的情况做了筛选，能执行到此处说明是同一物品，只是压缩与否的问题
                    from_item_dict = json.loads(from_item['extraId'])
                    to_item_dict = json.loads(to_item['extraId'])
                    new_compress_count = from_item_dict['compress_count'] + to_item_dict['compress_count']

                    # 处理存入extraId中count_data中数据，放入框到背包生成物品使用
                    to_item_dict['count_data']['have_compress_count'].append(from_item_dict['compress_count'])

                    # 构建新from_item
                    from_item = to_item_dict['item_dict']
                    new_extra_id = {'item_dict': to_item_dict['item_dict'], 'compress_count': new_compress_count,
                                    'count_data': to_item_dict['count_data']}
                    str_extra_id = json.dumps(new_extra_id)
                    from_item['extraId'] = str_extra_id
                    to_item = None  # FIXME 可能会导致后边有问题
                    set_player_inv_item_num(player_id, from_slot, 0)

        # 输出框 ==》背包（只存在直接取出的情况）
        elif from_slot == 'output_slot' and isinstance(to_slot, int):
            if take_percent < 1:  # 不允许分堆取出
                return False
            if take_percent == 1 and not to_item:
                # region 设置生成压缩物品的相关数据，主要设置 count tips extraId

                # json字符串 ==》python对象
                data = json.loads(from_item['extraId'])
                temp_item = data['item_dict']
                # 将temp_item初始化成最原始的物品字典作为原始数据使用
                temp_item['customTips'] = ''
                # 将存储在extraId中最原始的物品信息赋给from_item
                from_item = data['item_dict']
                from_item['count'] = 1

                tips = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(data['compress_count']) + "§r"
                from_item['customTips'] = tips

                extra_id_dict = {'item_dict': temp_item,
                                 'compress_count': data['compress_count']}
                str_extra_data = json.dumps(extra_id_dict)
                from_item['extraId'] = str_extra_data

                spawn_item_to_player_inv(from_item, player_id, to_slot)
                # 最新的物品数据传送到客户端进行交换
                from_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
        # endregion

        # 放入框 ==》背包
        elif isinstance(from_slot, str) and from_slot == 'input_slot':
            # 设置物品自定义tips和标识符
            # 只有在存在空余槽位时才被允许放入背包
            if take_percent == 1 and not to_item:

                from_item_dict = json.loads(from_item['extraId'])
                no_compress_count = from_item_dict['count_data']['no_compress_count']
                temp_no_compress_count = no_compress_count
                have_compress_count = from_item_dict['count_data']['have_compress_count']

                # 未压缩物品生成到背包
                if no_compress_count != 0:

                    if 0 < no_compress_count <= 64:
                        copy_item1 = copy.deepcopy(from_item)
                        temp_item1 = (json.loads(copy_item1['extraId']))['item_dict']
                        temp_item1['count'] = no_compress_count
                        spawn_item_to_player_inv(temp_item1, player_id, to_slot)
                        temp_item1 = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                        args["from_item"] = temp_item1
                        args["to_item"] = to_item
                        notify_to_client(player_id, 'OnItemSwapServerEvent', args)
                    else:
                        copy_item1 = copy.deepcopy(from_item)
                        temp_item1 = (json.loads(copy_item1['extraId']))['item_dict']
                        temp_item1['count'] = 64
                        spawn_item_to_player_inv(temp_item1, player_id, to_slot)
                        temp_item1 = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                        args["from_item"] = temp_item1
                        args["to_item"] = to_item
                        notify_to_client(player_id, 'OnItemSwapServerEvent', args)

                        no_compress_count -= 64
                        for i in xrange(36):
                            item = get_player_item(player_id, ItemPosType.INVENTORY, i, True)
                            if item:
                                continue
                            if no_compress_count <= 0:
                                return False
                            if 0 < no_compress_count <= 64:
                                copy_item3 = copy.deepcopy(from_item)
                                temp_item3 = (json.loads(copy_item3['extraId']))['item_dict']
                                temp_item3['count'] = no_compress_count
                                spawn_item_to_player_inv(temp_item3, player_id, i)
                                temp_item3 = get_player_item(player_id, ItemPosType.INVENTORY, i, True)
                                args["from_item"] = temp_item3
                                args["to_item"] = to_item
                                notify_to_client(player_id, 'OnItemSwapServerEvent', args)
                                break
                            copy_item2 = copy.deepcopy(from_item)
                            temp_item2 = (json.loads(copy_item2['extraId']))['item_dict']
                            temp_item2['count'] = 64
                            spawn_item_to_player_inv(temp_item2, player_id, i)
                            temp_item2 = get_player_item(player_id, ItemPosType.INVENTORY, i, True)
                            no_compress_count -= 64
                            args["from_item"] = temp_item2
                            args["to_item"] = to_item
                            notify_to_client(player_id, 'OnItemSwapServerEvent', args)
                        # 更新背包UI
                        cls.update_inventory_ui(player_id, block_name)

                # 已压缩物品生成到背包
                if have_compress_count:

                    # 如果背包槽位无物品，而且之前压缩的物品只有一个，则将此物品生成到该指定槽位
                    if temp_no_compress_count == 0 and len(have_compress_count) == 1:
                        temp_item = copy.deepcopy(from_item)
                        # json字符串 ==》python对象
                        data = json.loads(temp_item['extraId'])
                        # 将存储在extraId中最原始的物品信息赋给last_item
                        last_item = data['item_dict']
                        last_item['count'] = 1
                        tips = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(have_compress_count[-1]) + "§r"
                        last_item['customTips'] = tips
                        data['compress_count'] = have_compress_count[-1]
                        have_compress_count.pop()
                        data.pop('count_data')
                        last_extra_id = json.dumps(data)
                        last_item['extraId'] = last_extra_id
                        spawn_item_to_player_inv(last_item, player_id, to_slot)
                        # 最新的物品数据传送到客户端进行交换
                        last_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                        args["from_item"] = last_item
                        args["to_item"] = to_item
                        notify_to_client(player_id, 'OnItemSwapServerEvent', args)

                    # 如果背包槽位无物品，但之前压缩的物品多于一个，则优先在指定槽位上生成一个，再生成到其他空余槽位
                    elif temp_no_compress_count == 0 and len(have_compress_count) > 1:
                        temp_item = copy.deepcopy(from_item)
                        # json字符串 ==》python对象
                        data = json.loads(temp_item['extraId'])
                        # 将存储在extraId中最原始的物品信息赋给last_item
                        last_item = data['item_dict']
                        last_item['count'] = 1
                        tips = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(have_compress_count[-1]) + "§r"
                        last_item['customTips'] = tips
                        data['compress_count'] = have_compress_count[-1]
                        have_compress_count.pop()
                        data.pop('count_data')
                        last_extra_id = json.dumps(data)
                        last_item['extraId'] = last_extra_id
                        spawn_item_to_player_inv(last_item, player_id, to_slot)
                        # 最新的物品数据传送到客户端进行交换
                        last_item = get_player_item(player_id, ItemPosType.INVENTORY, to_slot, True)
                        args["from_item"] = last_item
                        args["to_item"] = to_item
                        notify_to_client(player_id, 'OnItemSwapServerEvent', args)

                        for i in xrange(36):
                            have_item = get_player_item(player_id, ItemPosType.INVENTORY, i, True)
                            if have_item:
                                continue
                            if len(have_compress_count) == 1:
                                temp_item_1 = copy.deepcopy(from_item)
                                # json字符串 ==》python对象
                                data_1 = json.loads(temp_item_1['extraId'])
                                # 将存储在extraId中最原始的物品信息赋给last_item
                                last_item_1 = data_1['item_dict']
                                last_item_1['count'] = 1
                                tips_1 = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(
                                    have_compress_count[-1]) + "§r"
                                last_item_1['customTips'] = tips_1
                                data_1['compress_count'] = have_compress_count[-1]
                                have_compress_count.pop()
                                data_1.pop('count_data')
                                last_extra_id_1 = json.dumps(data_1)
                                last_item_1['extraId'] = last_extra_id_1
                                spawn_item_to_player_inv(last_item_1, player_id, i)
                                # 最新的物品数据传送到客户端进行交换
                                last_item_1 = get_player_item(player_id, ItemPosType.INVENTORY, i, True)
                                args["from_item"] = last_item_1
                                args["to_item"] = to_item
                                notify_to_client(player_id, 'OnItemSwapServerEvent', args)
                                break
                            if len(have_compress_count) == 0:
                                break
                            temp_item_2 = copy.deepcopy(from_item)
                            # json字符串 ==》python对象
                            data_2 = json.loads(temp_item_2['extraId'])
                            # 将存储在extraId中最原始的物品信息赋给last_item
                            last_item_2 = data['item_dict']
                            last_item_2['count'] = 1
                            tips_2 = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(have_compress_count[-1]) + "§r"
                            last_item_2['customTips'] = tips_2
                            data_2['compress_count'] = have_compress_count[-1]
                            have_compress_count.pop()
                            data_2.pop('count_data')
                            last_extra_id_2 = json.dumps(data_2)
                            last_item_2['extraId'] = last_extra_id_2
                            spawn_item_to_player_inv(last_item_2, player_id, i)
                            # 最新的物品数据传送到客户端进行交换
                            last_item_2 = get_player_item(player_id, ItemPosType.INVENTORY, i, True)
                            args["from_item"] = last_item_2
                            args["to_item"] = to_item
                            notify_to_client(player_id, 'OnItemSwapServerEvent', args)

                    # 如果背包槽位有物品，直接将之前压缩的物品生成到其他空余槽位
                    elif temp_no_compress_count != 0 and len(have_compress_count) > 0:
                        for i in xrange(36):
                            has_item = get_player_item(player_id, ItemPosType.INVENTORY, i, True)
                            if has_item:
                                continue
                            if len(have_compress_count) == 0:
                                break
                            temp_item_4 = copy.deepcopy(from_item)
                            # json字符串 ==》python对象
                            data_4 = json.loads(temp_item_4['extraId'])
                            # 将存储在extraId中最原始的物品信息赋给last_item
                            last_item_4 = data_4['item_dict']
                            last_item_4['count'] = 1
                            tips_4 = from_item_detail_text + "\n已压缩数量 " + "§b§o" + str(have_compress_count[-1]) + "§r"
                            last_item_4['customTips'] = tips_4
                            data_4['compress_count'] = have_compress_count[-1]
                            have_compress_count.pop()
                            data_4.pop('count_data')
                            last_extra_id_4 = json.dumps(data_4)
                            last_item_4['extraId'] = last_extra_id_4
                            spawn_item_to_player_inv(last_item_4, player_id, i)
                            # 最新的物品数据传送到客户端进行交换
                            last_item_4 = get_player_item(player_id, ItemPosType.INVENTORY, i, True)
                            args["from_item"] = last_item_4
                            args["to_item"] = to_item
                            notify_to_client(player_id, 'OnItemSwapServerEvent', args)

                    # 更新背包UI
                    cls.update_inventory_ui(player_id, block_name)
                return False

            if take_percent < 1:  # 输入框取出不允许分堆操作
                return False

        args["from_item"] = from_item
        args["to_item"] = to_item
        notify_to_client(player_id, 'OnItemSwapServerEvent', args)
        return False
