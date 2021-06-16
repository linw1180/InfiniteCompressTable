# -*- coding: utf-8 -*-

from infiniteCompressTableScripts.modClient.utils.ui_utils import get_ui_manager
from infiniteCompressTableScripts.modCommon.config.block_config import BlockEnum
from infiniteCompressTableScripts.modCommon.config.ui_config import UI_DEFS
from infiniteCompressTableScripts.modCommon.utils.log_utils import func_log


@func_log
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
	# if 'inventory' in args:
	# 	ui_node.update_bag_ui(args['inventory'])

	# if 'inventory' in args:
	# 	ui_node.update_bag_ui(args['inventory'], args['state'])
	# if 'eu' in args:
	# 	ui_node.update_moying_bag_ui(args['eu'], args['state'])
	# if 'search_item' in args:
	# 	ui_node.update_search_bag_ui(args['search_item'], args)


def on_item_swap(args):
	ui_key = args['block_name']
	ui_data = UI_DEFS.get(ui_key)
	ui_node = get_ui_manager().get_ui_by_push(ui_data)
	if ui_node:
		ui_node.swap_item(args)


def save_box_size(args):
	ui_key = args['block_name']
	ui_data = UI_DEFS.get(ui_key)
	ui_node = get_ui_manager().get_ui_by_push(ui_data)
	ui_node.box_size = args['data']


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
