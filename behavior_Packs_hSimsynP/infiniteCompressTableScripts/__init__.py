# 未压缩：
#
# item = {'itemId': 20, 'count': 64, 'modItemId': '', 'enchantData': [], 'durability': 0, 'customTips': '', 'extraId': '',
#         'modId': '', 'userData': None, 'isDiggerItem': False, 'itemName': 'minecraft:glass', 'auxValue': 0,
#         'showInHand': True}，
#
#
# 压缩：
#
# item = {'itemId': 20, 'count': 1, 'modItemId': '', 'enchantData': [], 'durability': 0,
#         'customTips': '\xc2\xa7f\xe7\x8e\xbb\xe7\x92\x83\xc2\xa7r\n\xc2\xa79\xc2\xa79\xe5\xbb\xba\xe7\xad\x91\xc2\xa7r\xc2\xa7r\xc2\xa7r\xc2\xa7r\n\xe5\xb7\xb2\xe5\x8e\x8b\xe7\xbc\xa9\xe6\x95\xb0\xe9\x87\x8f \xc2\xa7b\xc2\xa7o64\xc2\xa7r',
#         'extraId': '{"item_dict": {"itemId": 20, "count": 1, "modItemId": "", "enchantData": [], "durability": 0, "customTips": "", "extraId": "", "modId": "", "userData": null, "isDiggerItem": false, "itemName": "minecraft:glass", "auxValue": 0, "showInHand": true}, "compress_count": 64}',
#         'modId': '', 'userData': {'ItemExtraID': {'__type__': 8,
#                                                   '__value__': '{"item_dict": {"itemId": 20, "count": 1, "modItemId": "", "enchantData": [], "durability": 0, "customTips": "", "extraId": "", "modId": "", "userData": null, "isDiggerItem": false, "itemName": "minecraft:glass", "auxValue": 0, "showInHand": true}, "compress_count": 64}'},
#                                   'ItemCustomTips': {'__type__': 8,
#                                                      '__value__': '\xc2\xa7f\xe7\x8e\xbb\xe7\x92\x83\xc2\xa7r\n\xc2\xa79\xc2\xa79\xe5\xbb\xba\xe7\xad\x91\xc2\xa7r\xc2\xa7r\xc2\xa7r\xc2\xa7r\n\xe5\xb7\xb2\xe5\x8e\x8b\xe7\xbc\xa9\xe6\x95\xb0\xe9\x87\x8f \xc2\xa7b\xc2\xa7o64\xc2\xa7r'}},
#         'isDiggerItem': False, 'itemName': 'minecraft:glass', 'auxValue': 0, 'showInHand': True}
#
# 重复压缩：
#
# item = {'itemId': 20, 'count': 1, 'modItemId': '', 'enchantData': [], 'durability': 0,
#         'customTips': '\xc2\xa7f\xe7\x8e\xbb\xe7\x92\x83\xc2\xa7r\n\xc2\xa79\xc2\xa79\xe5\xbb\xba\xe7\xad\x91\xc2\xa7r\xc2\xa7r\xc2\xa7r\xc2\xa7r\n\xe5\xb7\xb2\xe5\x8e\x8b\xe7\xbc\xa9\xe6\x95\xb0\xe9\x87\x8f \xc2\xa7b\xc2\xa7o64\xc2\xa7r',
#         'extraId': '{"item_dict": {"itemId": 20, "count": 1, "modItemId": "", "enchantData": [], "durability": 0, "customTips": "", "extraId": "", "modId": "", "userData": null, "isDiggerItem": false, "itemName": "minecraft:glass", "auxValue": 0, "showInHand": true}, "compress_count": 64}',
#         'modId': '', 'userData': {'ItemExtraID': {'__type__': 8,
#                                                   '__value__': '{"item_dict": {"itemId": 20, "count": 1, "modItemId": "", "enchantData": [], "durability": 0, "customTips": "", "extraId": "", "modId": "", "userData": null, "isDiggerItem": false, "itemName": "minecraft:glass", "auxValue": 0, "showInHand": true}, "compress_count": 64}'},
#                                   'ItemCustomTips': {'__type__': 8,
#                                                      '__value__': '\xc2\xa7f\xe7\x8e\xbb\xe7\x92\x83\xc2\xa7r\n\xc2\xa79\xc2\xa79\xe5\xbb\xba\xe7\xad\x91\xc2\xa7r\xc2\xa7r\xc2\xa7r\xc2\xa7r\n\xe5\xb7\xb2\xe5\x8e\x8b\xe7\xbc\xa9\xe6\x95\xb0\xe9\x87\x8f \xc2\xa7b\xc2\xa7o64\xc2\xa7r'}},
#         'isDiggerItem': False, 'itemName': 'minecraft:glass', 'auxValue': 0, 'showInHand': True}
