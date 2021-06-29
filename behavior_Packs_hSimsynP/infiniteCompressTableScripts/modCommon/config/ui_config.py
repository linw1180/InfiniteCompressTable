# -*- coding: utf-8 -*-
from infiniteCompressTableScripts.modCommon.config.block_config import BlockEnum


class UiDefsKey(object):
    COMPRESS_TABLE = BlockEnum.COMPRESS_TABLE
    LIMITED_COMPRESS_TABLE = BlockEnum.LIMITED_COMPRESS_TABLE


UI_DEFS = {
    UiDefsKey.COMPRESS_TABLE: {
        "ui_name": "infinite_compress_table_ui",
        "ui_class_path": "infiniteCompressTableScripts.modClient.ui.infinite_compress_table_ui.InfiniteCompressTableUIScreen",
        "ui_screen_def": "infinite_compress_table_ui.main",
        "paramDict": {"isHud": 0}
    },
    UiDefsKey.LIMITED_COMPRESS_TABLE: {
        "ui_name": "limited_compress_table_ui",
        "ui_class_path": "infiniteCompressTableScripts.modClient.ui.limited_compress_table_ui.LimitedCompressTableUIScreen",
        "ui_screen_def": "limited_compress_table_ui.main",
        "paramDict": {"isHud": 0}
    },
}
