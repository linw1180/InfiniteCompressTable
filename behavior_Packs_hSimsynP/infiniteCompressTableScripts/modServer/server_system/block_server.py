# -*- coding: utf-8 -*-
from infiniteCompressTableScripts.modCommon.config.block_config import BlockEnum
from infiniteCompressTableScripts.modServer.server_block.compress_table import CompressTable

BLOCK_SERVER_MAPPING = {
	BlockEnum.COMPRESS_TABLE: CompressTable
}


def player_use_block(args):
	if args['blockName'] in BLOCK_SERVER_MAPPING:
		BLOCK_SERVER_MAPPING[args['blockName']].player_use_block(args)

