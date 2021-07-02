# -*- coding: utf-8 -*-

from infiniteCompressTableScripts.modClient.utils.ui_utils import get_ui_manager
from infiniteCompressTableScripts.modCommon.config.block_config import BlockEnum
from infiniteCompressTableScripts.modCommon.config.ui_config import UI_DEFS


def open_block_ui(args):
    ui_key = args['block_name']
    ui_data = UI_DEFS.get(ui_key)
    if get_ui_manager().push_ui(ui_data, **args):
        return


def update_block_ui(args):
    ui_key = args['block_name']
    ui_data = UI_DEFS.get(ui_key)
    ui_node = get_ui_manager().get_ui_by_push(ui_data)
    if not ui_node:
        return
    # 更新背包UI
    if 'inventory' in args:
        ui_node.update_bag_ui(args['inventory'])


def on_item_swap(args):
    ui_key = args['block_name']
    ui_data = UI_DEFS.get(ui_key)
    ui_node = get_ui_manager().get_ui_by_push(ui_data)
    if ui_node:
        ui_node.swap_item(args)


def on_short_time_msg1_show(args):
    ui_key = args['block_name']
    ui_data = UI_DEFS.get(ui_key)
    ui_node = get_ui_manager().get_ui_by_push(ui_data)
    if ui_node:
        ui_node.show_short_time_msg1(args)


def on_item_processed(args):
    ui_key = args['block_name']
    ui_data = UI_DEFS.get(ui_key)
    ui_node = get_ui_manager().get_ui_by_push(ui_data)
    if ui_node:
        ui_node.processed_item(args)


def update_grid(args):
    ui_data = UI_DEFS.get(BlockEnum.COMPRESS_TABLE)
    ui_node = get_ui_manager().get_ui_by_push(ui_data)
    if ui_node:
        ui_node.show_data()
    else:
        ui_data = UI_DEFS.get(BlockEnum.COMPRESS_TABLE)  # FIXME 此处枚举值可能填有限压缩台
        ui_node = get_ui_manager().get_ui_by_push(ui_data)
        if ui_node:
            ui_node.show_data()
