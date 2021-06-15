# -*- coding: utf-8 -*-
from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer
from infiniteCompressTableScripts.modServer.server_block._block import Block
from infiniteCompressTableScripts.modServer.utils.system_utils import logger


class CompressTable(Block):

    @staticmethod
    def player_use_block(args):
        logger.info("=== compress table is using ===")

        player_id = args['playerId']
        block_name = args['blockName']
        pos = (args['x'], args['y'], args['z'])
        dimension = args['dimensionId']

        # 打开UI
        notify_to_client(player_id, 'OpenBlockUI', {
            "block_name": block_name,
            "pos": pos,
            "dimension": dimension,
            # "equipped_items": player.equipped_items.items,
            # "eu": block_entity_data['eu'],
        })
        # add_timer(0.1, cls.update_inventory_ui, player_id, block_name)
