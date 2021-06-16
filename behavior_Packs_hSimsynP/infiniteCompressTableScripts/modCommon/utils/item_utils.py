# -*- coding: utf-8 -*-
import json

from infiniteCompressTableScripts.modCommon.config.cyber_ware_config import CYBER_WARE_PRICE_CONFIG
from infiniteCompressTableScripts.modCommon.config.model_config import ModelEnum
from infiniteCompressTableScripts.modCommon.config.skill_config import SKILL_PARAM


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


def get_cyber_ware_type_by_item(item_dict):
    """
    通过物品字典获取装备部位

    :param item_dict:
    :return:
    """
    if not item_dict or not item_dict.get('itemName'):
        return

    if item_dict.get('itemName') not in CYBER_WARE_PRICE_CONFIG:
        return

    return item_dict['itemName'][16:17]


def get_cyber_ware_quality_by_item(item_dict):
    """
    通过物品字典获取品质

    :param item_dict:
    :return:
    """
    if not item_dict or not item_dict.get('itemName'):
        return

    if item_dict.get('itemName') not in CYBER_WARE_PRICE_CONFIG:
        return

    return int(item_dict['itemName'].split('_')[-1])


def get_skill_name_by_item(item_dict):
    """
    通过物品字典获取技能

    :param item_dict:
    :return:
    """
    if not item_dict or not item_dict.get('itemName'):
        return

    return item_dict['itemName'][16:-2] if item_dict['itemName'][16:-2] in SKILL_PARAM else None


def get_model_and_texture_by_item(item_dict):
    """
    通过物品字典获取模型名

    :param item_dict:
    :return:
    """
    if not item_dict or not item_dict.get('itemName'):
        return ModelEnum.CYBORG_PLAYER

    if item_dict['itemName'][18:-2] not in ModelEnum.PLAYER_MODEL:
        return ModelEnum.CYBORG_PLAYER

    return item_dict['itemName'][18:]
