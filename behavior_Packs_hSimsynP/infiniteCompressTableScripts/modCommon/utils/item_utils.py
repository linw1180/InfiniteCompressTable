# -*- coding: utf-8 -*-
import json


def is_same_item(item1, item2):
    """
    判断是否为同一item

    :param item1:
    :param item2:
    :return: 只有itemName和auxValue均相同才返回True
    """
    if not item1 or not item2:
        return False
    if item1.get("itemName", "item1") != item2.get("itemName", "item2"):
        return False
    if item1.get("auxValue") != item2.get("auxValue"):
        return False
    if item1.get("userData") != item2.get("userData"):
        return False
    if item1.get("durability") != item2.get("durability"):
        return False
    return True


def get_item_extra_id(item_dict):
    """
    获取物品的extra_id字典

    :param item_dict: 物品字典
    :return: 物品的extra_id字典
    """
    if not item_dict or not item_dict.get("extraId"):
        return None

    try:
        extra_id = json.loads(item_dict.get("extraId"))
    except (TypeError, ValueError):
        return None

    return extra_id
