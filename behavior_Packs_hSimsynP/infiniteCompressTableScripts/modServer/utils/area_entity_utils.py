# -*- coding: utf-8 -*-
import math

from mod.common.utils.mcmath import Vector3

from ..api import *


def entity_filter(entity_id):
    """
    判断entity是否非指定类别

    :param entity_id:
    :return: True：生物；反之False
    """
    entity_type = get_entity_type(entity_id)
    # print "========== Entity Type {} ==========".format(entity_type)
    if entity_type & get_minecraft_enum().EntityType.Mob != get_minecraft_enum().EntityType.Mob:
        return False
    if get_attr_max_value(entity_id, get_minecraft_enum().AttrType.HEALTH) <= 0:
        return False

    return True


def get_nearest_entity(center_entity, targets):
    center_pos = get_entity_pos(center_entity)
    min_distance = 9999
    target_id = None
    for entity_id in targets:
        entity_pos = get_entity_pos(entity_id)
        sqr_distance = Vector3(tuple(center_pos[i] - entity_pos[i] for i in xrange(3))).LengthSquared()

        if sqr_distance < min_distance:
            target_id = entity_id
            min_distance = sqr_distance

    return target_id


def get_vertical_vector(vec):
    # x，z平面上的向量为（0，0）
    if vec[0] == 0 and vec[2] == 0:
        return 0, 0
    if vec[0] == 0:
        x, z = 1, 0
    elif vec[2] == 0:
        x, z = 0, 1
    else:
        length = (vec[0] * vec[0] + vec[2] * vec[2]) ** 0.5
        x, z = vec[2] / length, -vec[0] / length
    return x, z


def get_rect_four_corner(center, v_face, width):
    """
    获取一个不平行于坐标轴的长方体的四个角的坐标（Y坐标高度取center的Y坐标）

    目标长方体的一条边的中心是玩家的位置，方向基于玩家面向

    :param center: tuple 玩家位置
    :param v_face: tuple 玩家面向 (不能是（0,y,0)）
    :param width: float 长方体的宽度
    :return: tuple
    """
    # 先求垂直向量
    x, z = get_vertical_vector(v_face)

    if x == 0 and z == 0:  # x，z平面上的向量为（0，0），默认只有一个中心点
        return []

    x, z = x * width * 0.5, z * width * 0.5
    # 四个点分别是center+vert，center+face+vert，center+face-vert， center-vert，
    return (
        (center[0] + x, center[1], center[2] + z),
        (center[0] + v_face[0] + x, center[1], center[2] + v_face[2] + z),
        (center[0] + v_face[0] - x, center[1], center[2] + v_face[2] - z),
        (center[0] - x, center[1], center[2] - z)
    )


def matrix_intersects(four_corner, point):
    """
    判断一个点是否在一个斜矩形内部（无视Y轴高度）
    :param four_corner: 矩形的四个角，顺序一定要沿着矩形的边
    :type four_corner: tuple
    :param point: 点坐标
    :type point: tuple
    :return:
    :rtype: Bool
    """
    p1, p2, p3, p4 = four_corner

    def get_dot(pos_1, pos_2, p):
        return (pos_2[0] - pos_1[0]) * (p[0] - pos_1[0]) + (pos_2[2] - pos_1[2]) * (p[2] - pos_1[2])

    return get_dot(p1, p2, point) >= 0 and get_dot(p1, p4, point) >= 0 and get_dot(
        p3, p4, point) >= 0 and get_dot(p3, p2, point) >= 0


def cylinder_intersects(center, radius, point):
    """
    判定一个点是否在一个圆柱体内 **无视Y坐标高度**

    :param center: tuple 圆心坐标
    :param radius: float 半径
    :param point: tuple 需要判定的点的坐标
    :return: Bool
    """
    proj_vector = Vector3(point[0] - center[0], 0, point[2] - center[2])  # xoz平面向量投影
    return proj_vector.Length() <= radius


def sector_intersects(center, direction, angle, point):
    """
    判定某个点是否在扇形范围内 **无视Y坐标高度**

    :param center: tuple 圆心坐标
    :param direction: tuple 扇形中心正面的向量
    :param angle: int 扇形夹角值
    :param point: tuple 需要判定的点的坐标
    :return: bool
    """
    proj_vector = Vector3(point[0] - center[0], 0, point[2] - center[2])  # xoz平面向量投影
    sqr_distance = proj_vector.LengthSquared()
    sqr_sector = direction[0] * direction[0] + direction[2] * direction[2]  # 扇形半径的平方

    if sqr_distance > sqr_sector:
        return False
    try:
        cos_angle = math.cos(math.radians(angle * 0.5))  # 扇形半夹角的cos值
        cos_similarity = (proj_vector[0] * direction[0] + proj_vector[2] * direction[2]) / (
                (sqr_distance ** 0.5) * (sqr_sector ** 0.5))  # 向量夹角余弦
    except ZeroDivisionError:
        return False

    if cos_similarity < cos_angle:
        return False
    return True


def get_entity_in_rectangle_area(center_entity, length=3, width=3):
    """
    获取矩形范围内的实体

    :param center_entity:
    :param length:
    :param width: 宽度
    :return:
    """
    possible_targets = get_entities_around(center_entity, max(length, width))
    if center_entity in possible_targets:
        possible_targets.remove(center_entity)
    possible_targets = filter(entity_filter, possible_targets)

    if not possible_targets:
        return []

    center_pos = get_entity_foot_pos(center_entity)
    dir_vector = tuple(i * length for i in get_dir_from_rot(get_entity_rot(center_entity)))

    # 获取命中斜矩形区域的四个角（仅x，z坐标有效）
    rect_corners = get_rect_four_corner(center_pos, dir_vector, width)

    if not rect_corners:
        return []

    for index, entity_id in enumerate(possible_targets):
        entity_pos = get_entity_pos(entity_id)
        if not matrix_intersects(rect_corners, entity_pos):
            possible_targets.remove(entity_id)

    return possible_targets


def get_entity_in_sector_area(center_entity, radius=3, angle=90):
    possible_targets = get_entities_around(center_entity, radius)
    if center_entity in possible_targets:
        possible_targets.remove(center_entity)
    possible_targets = filter(entity_filter, possible_targets)

    if not possible_targets:
        return []

    dir_vector = tuple(i * radius for i in get_dir_from_rot(get_entity_rot(center_entity)))
    if not dir_vector:
        return []

    center_pos = get_entity_foot_pos(center_entity)

    for index, entity_id in enumerate(possible_targets):
        entity_pos = get_entity_pos(entity_id)
        if not sector_intersects(center_pos, dir_vector, angle, entity_pos):
            possible_targets.remove(entity_id)

    return possible_targets


def get_entity_in_circular_area(center_entity, radius=3):
    possible_targets = get_entities_around(center_entity, radius)
    if center_entity in possible_targets:
        possible_targets.remove(center_entity)
    possible_targets = filter(entity_filter, possible_targets)

    if not possible_targets:
        return []
    center_pos = get_entity_foot_pos(center_entity)

    for index, entity_id in enumerate(possible_targets):
        entity_pos = get_entity_pos(entity_id)
        if not cylinder_intersects(center_pos, radius, entity_pos):
            possible_targets.remove(entity_id)

    return possible_targets
