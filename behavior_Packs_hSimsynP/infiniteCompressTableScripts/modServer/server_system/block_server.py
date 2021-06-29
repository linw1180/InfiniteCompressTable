# -*- coding: utf-8 -*-
from infiniteCompressTableScripts.modCommon.config.block_config import BlockEnum
from infiniteCompressTableScripts.modServer.server_block.compress_table import CompressTable
from infiniteCompressTableScripts.modServer.server_block.limited_compress_table import LimitedCompressTable

BLOCK_SERVER_MAPPING = {
    BlockEnum.COMPRESS_TABLE: CompressTable,
    BlockEnum.LIMITED_COMPRESS_TABLE: LimitedCompressTable
}


def player_use_block(args):
    if args['blockName'] in BLOCK_SERVER_MAPPING:
        BLOCK_SERVER_MAPPING[args['blockName']].player_use_block(args)


def use_item_on_block(args):
    """
    如果对自定义方块使用物品时拦截物品使用，防止操作时误操作放置物品

    :param args:
    :return:
    """
    block_name = args["blockName"]
    if block_name == "xl:block_compress_table":
        args["ret"] = True
