# -*- coding: utf-8 -*-
from mod.common.minecraftEnum import ItemPosType

from infiniteCompressTableScripts.modServer.api import notify_to_client, add_timer, get_player_all_items
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
		print '++++++++++++++++++++++++++++++ inv_items =', inv_items
		notify_to_client(player_id, 'UpdateBlockUI', {
			'block_name': block_name,
			'inventory': inv_items,
		})
