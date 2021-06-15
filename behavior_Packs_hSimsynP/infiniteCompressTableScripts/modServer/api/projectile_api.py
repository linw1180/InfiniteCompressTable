# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

level_id = serverApi.GetLevelId()


def get_source_entity_id(projectile_id):
    """
    获取抛射物发射者实体id

    :param projectile_id: 抛射物id
    :return: str 抛射物发射者实体id
    """
    bullet_attr_comp = serverApi.GetEngineCompFactory().CreateBulletAttributes(projectile_id)
    return bullet_attr_comp.GetSourceEntityId()


def create_projectile_entity(spawner_id, entity_identifier, param=None):
    """
    创建抛射物（直接发射）

    :param spawner_id: str 创建者Id
    :param entity_identifier: str 创建抛射物的类别，如minecraft:snowball
    :param param: dict 抛射物参数，默认为None
        position: tuple(float,float,float) 初始位置
        direction: tuple(float,float,float) 初始朝向
        power: float 投掷的力量值
        gravity: float 抛射物重力因子，默认为json配置中的值
        damage: float 抛射物伤害值，默认为json配置中的值
        targetId: str 抛射物目标（指定了target之后，会和潜影贝生物发射的跟踪导弹的那个投掷物是一个效果），默认不指定
        isDamageOwner: bool 对创建者是否造成伤害，默认不造成伤害
    :return: str 创建抛射物的Id，失败时为“-1”
    """
    projectile_comp = serverApi.GetEngineCompFactory().CreateProjectile(level_id)
    return projectile_comp.CreateProjectileEntity(spawner_id, entity_identifier, param)
