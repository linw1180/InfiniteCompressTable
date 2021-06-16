# -*- coding: utf-8 -*-
from infiniteCompressTableScripts.modCommon.config.block_config import BlockEnum


class UiDefsKey(object):
	COMPRESS_TABLE = BlockEnum.COMPRESS_TABLE


UI_DEFS = {
	UiDefsKey.COMPRESS_TABLE: {
		"ui_name": "compress_table_ui",
		"ui_class_path": "infiniteCompressTableScripts.modClient.ui.compress_table_ui.CompressTableUIScreen",
		"ui_screen_def": "compress_table_ui.main",
		"paramDict": {"isHud": 0}
	},
}
