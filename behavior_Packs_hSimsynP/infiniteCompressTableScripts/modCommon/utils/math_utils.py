# -*- coding: utf-8 -*-
import heapq
import math
import random

from mod.common.utils.mcmath import Vector3


def get_probability_results(value):
    # type: (float) -> bool
    return random.random() < value


def a_res(samples, n):
    """
    加权随机采样A-Res

    :param samples: [(item, weight), ...]
    :param n: 个数
    :return:
    """
    heap = []  # [(ki, item), ...]
    for sample, weight in samples:
        ui = random.uniform(0, 1)
        ki = ui ** (1.0 / weight) if weight else 0

        if len(heap) < n:
            heapq.heappush(heap, (ki, sample))
        elif ki > heap[0][0]:
            heapq.heappushpop(heap, (ki, sample))

    return [item[1] for item in heap]


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


def get_new_pos(pos, rot, offset, ignore_y=True):
    """
    通过旋转值和相对坐标确定新位置
    :param tuple pos:
    :param tuple rot:
    :param tuple offset:
    :param bool ignore_y:
    :rtype: tuple
    :return:
    """
    # 转轴公式
    import math
    rad = math.radians(rot[1])
    rad_y = math.radians(rot[0])
    sin = math.sin(rad)
    cos = math.cos(rad)
    cos_y = math.cos(rad_y)
    dz = offset[0] * sin + offset[2] * cos
    dx = offset[0] * cos - offset[2] * sin
    dy = offset[1] if ignore_y else offset[1] * cos_y
    return pos[0] + dx, pos[1] + dy, pos[2] + dz


def rot_from_dir(direction):
    """
    根据方向向量获取对应的朝向角度
    :param direction: 单位向量
    :return: 上下俯仰角度和左右旋转角度
    """
    x, y, z = direction
    return math.degrees(math.asin(y)), math.degrees(math.atan2(z, x)) - 90


def tuple_subtract(vec_a, vec_b):
    """
    用于对两个多维的tuple相减
    :param tuple vec_a:
    :param tuple vec_b:
    :return:
    """
    return tuple([v1 - v2 for v1, v2 in zip(vec_a, vec_b)])


def normalize_3d(x, y, z, parm=1.0):
    length = pow(x * x + y * y + z * z, 0.5)
    if length <= 0:
        return 0, 0, 0
    return x * parm / length, y * parm / length, z * parm / length


def cal_pos_distance(pos1, pos2, no_y=False):
    """
    计算两点之间的距离
    :param pos1:
    :param pos2:
    :param no_y: 是否忽视高度
    :return:
    """
    delta_x = pos1[0] - pos2[0]
    delta_y = 0 if no_y else pos1[1] - pos2[1]
    delta_z = pos1[2] - pos2[2]
    dis = delta_x ** 2 + delta_z ** 2 + delta_y ** 2
    return math.sqrt(dis)
