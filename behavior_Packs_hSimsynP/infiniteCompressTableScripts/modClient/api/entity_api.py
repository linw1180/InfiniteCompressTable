# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()
local_player = clientApi.GetLocalPlayerId()


def set_actor_collision(entity_id, collision):
    """
    设置实体是否可碰撞

    :param entity_id:
    :param collision: bool True:可碰撞  False:不可碰撞
    :return: bool True表示设置成功
    """
    collision_comp = clientApi.GetEngineCompFactory().CreateActorCollidable(entity_id)
    return collision_comp.SetActorCollidable(1 if collision else 0)


def is_render_at_all(entity_id):
    """
    获取实体是否渲染

    :param entity_id:
    :return: bool True表示渲染
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(entity_id)
    return not render_comp.GetNotRenderAtAll()


def set_render_at_all(entity_id, render=False):
    """
    设置是否渲染实体

    :param entity_id:
    :param render: bool False表示不渲染该实体
    :return: bool 设置是否成功
    """
    # 不渲染单个实体 entity_id
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(entity_id)
    return render_comp.SetNotRenderAtAll(not render)


def add_player_render_material(player_id, material_key, material_name):
    """
    增加玩家渲染需要的[材质]
        http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/03-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/06-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%94%9F%E7%89%A9/01-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%BA%E7%A1%80%E7%94%9F%E7%89%A9.html#_3-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%9D%90%E8%B4%A8

    调用该接口后需要调用RebuildPlayerRender才会生效

    :param player_id:
    :param material_key: str 材质key
    :param material_name: str 材质名称
    :return: bool 添加是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerRenderMaterial(material_key, material_name)


def add_player_render_controller(player_id, render_controller_name, condition=''):
    """
    增加玩家[渲染控制器]
        http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/03-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/06-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%94%9F%E7%89%A9/01-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%BA%E7%A1%80%E7%94%9F%E7%89%A9.html#_7-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B2%E6%9F%93%E6%8E%A7%E5%88%B6%E5%99%A8

    调用该接口后需要调用RebuildPlayerRender才会生效

    :param player_id:
    :param render_controller_name: str 渲染控制器名称
    :param condition: str 渲染控制器条件
    :return: bool 添加是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerRenderController(render_controller_name, condition)


def remove_player_render_controller(player_id, render_controller_name):
    """
    删除玩家[渲染控制器]
        http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/03-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/06-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%94%9F%E7%89%A9/01-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%BA%E7%A1%80%E7%94%9F%E7%89%A9.html#_7-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B2%E6%9F%93%E6%8E%A7%E5%88%B6%E5%99%A8

    调用该接口后需要调用RebuildPlayerRender才会生效

    :param player_id:
    :param render_controller_name: str 渲染控制器名称
    :return: bool 删除是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.RemovePlayerRenderController(render_controller_name)


def remove_player_geometry(player_id, geometry_key):
    """
    删除玩家渲染几何体

    调用该接口后需要调用RebuildPlayerRender才会生效

    动画和贴图都是与几何体密切相关的，改变几何体也需要改变动画与贴图

    :param player_id:
    :param geometry_key: str 渲染几何体名称键，如玩家默认几何体default
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.RemovePlayerGeometry(geometry_key)


def add_player_geometry(player_id, geometry_key, geometry_name):
    """
    增加玩家渲染几何体

    调用该接口后需要调用RebuildPlayerRender才会生效

    动画和贴图都是与几何体密切相关的，改变几何体也需要改变动画与贴图

    :param player_id:
    :param geometry_key: str 渲染几何体键，如玩家默认几何体default
    :param geometry_name: str 渲染几何体名称，如玩家默认几何体geometry.humanoid.custom
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerGeometry(geometry_key, geometry_name)


def add_player_texture(player_id, texture_key, texture_path):
    """
    增加玩家渲染贴图

    调用该接口后需要调用RebuildPlayerRender才会生效

    :param player_id:
    :param texture_key: str 贴图键
    :param texture_path: str 贴图路径
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerTexture(texture_key, texture_path)


def add_player_animation(player_id, animation_key, animation_name):
    """
    增加玩家渲染动画

    :param player_id:
    :param animation_key: str 动画键
    :param animation_name: str 动画名称
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerAnimation(animation_key, animation_name)


def add_player_animation_controller(player_id, animation_controller_key, animation_controller_name):
    """
    增加玩家渲染动画控制器

    :param player_id:
    :param animation_controller_key: str 动画控制器键
    :param animation_controller_name: str 动画控制器名称
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerAnimationController(animation_controller_key, animation_controller_name)


def remove_player_animation_controller(player_id, animation_controller_key):
    """
    移除玩家渲染动画控制器

    :param player_id:
    :param animation_controller_key: str 动画控制器键
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.RemovePlayerAnimationController(animation_controller_key)


def add_player_animation_into_state(player_id, animation_controller_name, state_name, animation_name, condition):
    """
    在玩家的动画控制器中的状态添加动画

    :param player_id:
    :param animation_controller_name: str 动画控制器名称，如root（controller.animation.player.root）
    :param state_name: 动画状态名称，如first_person
    :param animation_name: 添加的动画名称或动画控制器名称，如first_person_attack_controller_new
    :param condition: 动画控制表达式，默认为空，如query.mod.index > 0
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerAnimationIntoState(animation_controller_name, state_name, animation_name, condition)


def add_player_particle_effect(player_id, effect_key, effect_name):
    """
    增加玩家特效资源

    :param player_id:
    :param effect_key: str 特效资源Key，如bee.entity.json中的nectar_dripping
    :param effect_name: str 特效资源名称，如minecraft:nectar_drip_particle
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerParticleEffect(effect_key, effect_name)


def add_player_sound_effect(player_id, sound_key, sound_name):
    """
    增加玩家音效资源

    :param player_id:
    :param sound_key: str 音效资源Key
    :param sound_name: str 音效资源名称
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.AddPlayerSoundEffect(sound_key, sound_name)


def rebuild_player_render(player_id):
    """
    重建玩家的数据渲染器

    :param player_id:
    :return: bool 重建是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(player_id)
    return render_comp.RebuildPlayerRender()


def add_actor_render_material(actor_identifier, material_key, material_name):
    """
    增加生物渲染需要的[材质]
        http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/03-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/06-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%94%9F%E7%89%A9/01-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%BA%E7%A1%80%E7%94%9F%E7%89%A9.html#_3-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%9D%90%E8%B4%A8

    调用该接口后需要调用RebuildActorRender才会生效

    :param actor_identifier: str 生物的identifier
    :param material_key: str 材质key
    :param material_name: str 材质名称
    :return: bool 添加是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(local_player)
    return render_comp.AddActorRenderMaterial(actor_identifier, material_key, material_name)


def add_actor_render_controller(actor_identifier, render_controller_name, condition=''):
    """
    增加生物[渲染控制器]
        http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/03-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/06-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%94%9F%E7%89%A9/01-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%BA%E7%A1%80%E7%94%9F%E7%89%A9.html#_7-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B2%E6%9F%93%E6%8E%A7%E5%88%B6%E5%99%A8

    调用该接口后需要调用RebuildActorRender才会生效

    :param actor_identifier: str 生物identifier
    :param render_controller_name: str 渲染控制器名称
    :param condition: str 渲染控制器条件，当该条件成立时，renderControllerName指向的渲染控制器才会生效
    :return: bool 添加是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(level_id)
    return render_comp.AddActorRenderController(actor_identifier, render_controller_name, condition)


def remove_actor_render_controller(actor_identifier, render_controller_name):
    """
    删除生物[渲染控制器]
        http://mc.163.com/mcstudio/mc-dev/MCDocs/2-ModSDK%E6%A8%A1%E7%BB%84%E5%BC%80%E5%8F%91/03-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B8%E6%88%8F%E5%86%85%E5%AE%B9/06-%E8%87%AA%E5%AE%9A%E4%B9%89%E7%94%9F%E7%89%A9/01-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%9F%BA%E7%A1%80%E7%94%9F%E7%89%A9.html#_7-%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B8%B2%E6%9F%93%E6%8E%A7%E5%88%B6%E5%99%A8

    调用该接口后需要调用RebuildActorRender才会生效

    :param actor_identifier: str 生物identifier
    :param render_controller_name: str 渲染控制器名称
    :return: bool 删除是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(level_id)
    return render_comp.RemoveActorRenderController(actor_identifier, render_controller_name)


def add_actor_animation(entity_id, actor_identifier, animation_key, animation_name):
    """
    增加生物渲染动画

    :param entity_id:
    :param actor_identifier: 生物的identifier
    :param animation_key: str 动画键
    :param animation_name: str 动画名称
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(entity_id)
    return render_comp.AddActorAnimation(actor_identifier, animation_key, animation_name)


def add_actor_animation_controller(entity_id, actor_identifier, anim_controller_key, anim_controller_name):
    """
    增加生物渲染动画控制器

    :param entity_id:
    :param actor_identifier: 生物的identifier
    :param anim_controller_key: str 动画控制器键
    :param anim_controller_name: str 动画控制器名称
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(entity_id)
    return render_comp.AddActorAnimationController(actor_identifier, anim_controller_key, anim_controller_name)


def remove_actor_animation_controller(entity_id, actor_identifier, animation_controller_key):
    """
    移除生物渲染动画控制器

    :param entity_id:
    :param actor_identifier: 生物的identifier
    :param animation_controller_key: str 动画控制器键
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(entity_id)
    return render_comp.RemoveActorAnimationController(actor_identifier, animation_controller_key)


def add_actor_script_animate(entity_id, actor_identifier, animation_controller_name, condition, auto_replace=False):
    """
    在生物的客户端实体定义（minecraft:client_entity）json中的scripts/animate节点添加动画/动画控制器

    :param entity_id: str
    :param actor_identifier: str 实体identifier
    :param animation_controller_name: str 动画/动画控制器名称，如look_at_target
    :param condition: str 动画/动画控制器控制表达式，默认为空，如query.mod.index > 0
    :param auto_replace: bool 是否覆盖已存在的动画/动画控制器，默认值为False
    :return:
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(entity_id)
    return render_comp.AddActorScriptAnimate(actor_identifier, animation_controller_name, condition, auto_replace)


def add_actor_particle_effect(actor_identifier, effect_key, effect_name):
    """
    增加生物特效资源

    :param actor_identifier :
    :param effect_key: str 特效资源Key，如bee.entity.json中的nectar_dripping
    :param effect_name: str 特效资源名称，如minecraft:nectar_drip_particle
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(level_id)
    return render_comp.AddActorParticleEffect(actor_identifier, effect_key, effect_name)


def add_actor_sound_effect(actor_identifier, sound_key, sound_name):
    """
    增加生物特效资源

    目前只支持在动作(animation)中播放音效，不支持在动作控制器(animation controller)中播放音效。

    :param actor_identifier :
    :param sound_key: str 音效资源Key
    :param sound_name: str 音效资源名称
    :return: bool 是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(level_id)
    return render_comp.AddActorSoundEffect(actor_identifier, sound_key, sound_name)


def rebuild_actor_render(actor_identifier):
    """
    重建生物的数据渲染器（该接口不支持玩家，玩家请使用RebuildPlayerRender）
    
    :param actor_identifier: str 实体identifier
    :return: bool 重建是否成功
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(level_id)
    return render_comp.RebuildActorRender(actor_identifier)


def change_armor_textures(armor_identifier, textures_dict, icon):
    """
    重建生物的数据渲染器（该接口不支持玩家，玩家请使用RebuildPlayerRender）

    无法跟物品的贴图动画同时使用

    有一定性能消耗，不建议频繁调用

    :param armor_identifier: str 盔甲标识符，格式[namespace:name:auxvalue]，auxvalue默认为0
    :param textures_dict: dict 场景中目标贴图的映射表，格式可参考"definitions/attachables/diamond_helmet.json"配置
    :param icon: str 盔甲UI图标的贴图, 为None或者""的话表示不修改UI上的图标
    :return: bool 修改是否成功（因为采用延迟加载，此处返回成功不代表参数中的贴图路径正确，路径错误会导致渲染时贴图丢失显示异常）
    """
    render_comp = clientApi.GetEngineCompFactory().CreateActorRender(level_id)
    return render_comp.ChangeArmorTextures(armor_identifier, textures_dict, icon)


def get_projectile_aux_value(entity_id):
    """
    获取射出的弓箭或投掷出的药水的附加值

    :param entity_id:
    :return: int 具体数值见wiki的“箭”及“药水”页面
    """
    aux_comp = clientApi.GetEngineCompFactory().CreateAuxValue(entity_id)
    return aux_comp.GetAuxValue()


def set_brightness(entity_id, brightness):
    """
    设置实体的亮度

    目前只支持修改替换了骨骼模型的实体亮度，使用游戏原生模型的实体暂不予支持。

    :param entity_id:
    :param brightness: float
        0：纯黑
        1：正常亮度
        2-14：较亮甚至纯白
        >14：通常为纯白，即使数值改变也没有明显变化
    :return: bool True:设置成功  False:设置失败
    """
    bright_comp = clientApi.GetEngineCompFactory().CreateBrightness(entity_id)
    return bright_comp.SetBrightness(brightness)


def get_engine_type(entity_id):
    """
    获取实体类型

    :param entity_id:
    :return: int 详见[EntityType]枚举
    """
    engine_type_comp = clientApi.GetEngineCompFactory().CreateEngineType(entity_id)
    return engine_type_comp.GetEngineType()


def get_engine_type_str(entity_id):
    """
    获取实体在游戏中的类型id的str

    微软自定义实体只能通过engineTypeStr获取类型

    :param entity_id:
    :return: str 实体类型的string描述
    """
    engine_type_comp = clientApi.GetEngineCompFactory().CreateEngineType(entity_id)
    return engine_type_comp.GetEngineTypeStr()


def set_health_bar_color(entity_id, front, back):
    """
    设置血条的颜色及背景色
    
    必须用game组件设置ShowHealthBar时才能显示血条！！
    
    :param entity_id: 
    :param front: tuple(float,float,float,float) 血条颜色的RGBA值，范围0-1
    :param back: tuple(float,float,float,float) 背景颜色的RGBA值，范围0-1
    :return: 
    """
    health_comp = clientApi.GetEngineCompFactory().CreateHealth(entity_id)
    return health_comp.SetColor(front, back)


def show_entity_health_bar(entity_id, show=False):
    """
    设置某个entity是否显示血条，默认为显示

    必须用game组件设置ShowHealthBar时才能显示血条！！

    :param entity_id:
    :param show: bool 设置是否显示
    :return:
    """
    health_comp = clientApi.GetEngineCompFactory().CreateHealth(entity_id)
    return health_comp.ShowHealth(show)


def register_update_attr_func(entity_id, param_name, func):
    """
    注册属性值变换时的回调函数，当属性变化时会调用该函数

    回调函数需要接受一个参数，参数是dict，具体数据示例：{'oldValue': 0, 'newValue': 1, 'entityId': ’-433231231231‘}

    :param entity_id:
    :param param_name: str 监听的属性名称
    :param func: function 监听的回调函数
    :return:
    """
    mod_attr_comp = clientApi.GetEngineCompFactory().CreateModAttr(entity_id)
    mod_attr_comp.RegisterUpdateFunc(param_name, func)


def cancel_update_attr_func(entity_id, param_name, func):
    """
    反注册属性值变换时的回调函数

    需要传注册时的 **同一个函数** 作为参数

    :param entity_id:
    :param param_name: str 监听的属性名称
    :param func: function 监听的回调函数
    :return:
    """
    mod_attr_comp = clientApi.GetEngineCompFactory().CreateModAttr(entity_id)
    mod_attr_comp.UnRegisterUpdateFunc(param_name, func)


def set_mod_attr(entity_id, param_name, param_value):
    """
    设置客户端属性值

    注意：这里设置了只在本地有效，并不会同步到服务端和其他客户端

    :param entity_id:
    :param param_name: str 属性名称，str的名称建议以mod命名为前缀，避免多个mod之间冲突
    :param param_value: any 属性值，支持python基础数据
    :return:
    """
    mod_attr_comp = clientApi.GetEngineCompFactory().CreateModAttr(entity_id)
    mod_attr_comp.SetAttr(param_name, param_value)


def get_mod_attr(entity_id, param_name, default_value=None):
    """
    获取属性值

    defaultValue不传的时候默认为None

    :param entity_id:
    :param param_name: str 属性名称，str的名称建议以mod命名为前缀，避免多个mod之间冲突
    :param default_value: any 属性默认值，属性不存在时返回该默认值，此时属性值依然未设置
    :return: any 返回属性值
    """
    mod_attr_comp = clientApi.GetEngineCompFactory().CreateModAttr(entity_id)
    return mod_attr_comp.GetAttr(param_name, default_value)


def get_entity_pos(entity_id):
    """
    获取实体位置
    
    对于非玩家，获取到的是脚底部位的位置
    
    对于玩家，如果处于行走，站立，游泳，潜行，滑翔状态，获得的位置比脚底位置高1.62，如果处于睡觉状态，获得的位置比最低位置高0.2
    
    :param entity_id: 
    :return: tuple(float,float,float) 实体的坐标
    """
    pos_comp = clientApi.GetEngineCompFactory().CreatePos(entity_id)
    return pos_comp.GetPos()


def get_entity_foot_pos(entity_id):
    """
    获取实体脚所在的位置

    获取实体脚底的位置（除了睡觉时）

    :param entity_id:
    :return: tuple(float,float,float) 位置信息
    """
    pos_comp = clientApi.GetEngineCompFactory().CreatePos(entity_id)
    return pos_comp.GetFootPos()


def register_query_variable(variable_name, default_value):
    """
    注册实体计算节点

    :param variable_name: str 节点名称，必须以"query.mod."开头
    :param default_value: float 默认值
    :return: bool 注册是否成功
    """
    query_variable_comp = clientApi.GetEngineCompFactory().CreateQueryVariable(level_id)
    return query_variable_comp.Register(variable_name, default_value)


def unregister_query_variable(variable_name):
    """
    注销实体计算节点

    :param variable_name: str 节点名称，必须以"query.mod."开头
    :return: bool 注销是否成功
    """
    query_variable_comp = clientApi.GetEngineCompFactory().CreateQueryVariable(level_id)
    return query_variable_comp.UnRegister(variable_name)


def set_query_variable(entity_id, variable_name, value):
    """
    设置某一个实体计算节点的值

    :param entity_id:
    :param variable_name: str 节点名称，必须以"query.mod."开头
    :param value: float 计算节点的值
    :return: bool 设置是否成功
    """
    query_variable_comp = clientApi.GetEngineCompFactory().CreateQueryVariable(entity_id)
    return query_variable_comp.Set(variable_name, value)


def get_query_variable(entity_id, variable_name):
    """
    获取某一个实体计算节点的值，如果不存在返回注册时的默认值
    
    :param entity_id: 
    :param variable_name: str 节点名称，必须以"query.mod."开头
    :return: float 节点的值
    """
    query_variable_comp = clientApi.GetEngineCompFactory().CreateQueryVariable(entity_id)
    return query_variable_comp.Get(variable_name)


def get_molang_value(entity_id, molang_name):
    """
    获取实体moLang变量的值

    因为没有渲染上下文，某些moLang无法通过该种方式获取到正确的值，如query.is_first_person、variable.is_first_person等。

    :param entity_id:
    :param molang_name: str moLang变量名称，如query.can_fly
    :return: float 节点的值，不存在返回None
    """
    query_variable_comp = clientApi.GetEngineCompFactory().CreateQueryVariable(entity_id)
    return query_variable_comp.GetMolangValue(molang_name)


def get_entity_rot(entity_id):
    """
    获取实体角度
    
    :param entity_id: 
    :return: tuple(float,float) 俯仰角度及绕竖直方向的角度，单位是角度
    """
    rot_comp = clientApi.GetEngineCompFactory().CreateRot(entity_id)
    return rot_comp.GetRot()


def set_entity_rot(rot):
    """
    设置实体的角度

    只能设置local_player，即本地玩家自己

    :param rot: tuple(float,float) 俯仰角度及绕竖直方向的角度，单位是角度
    :return: bool 设置是否成功
    """
    rot_comp = clientApi.GetEngineCompFactory().CreateRot(local_player)
    return rot_comp.SetRot(rot)


def get_body_rot(entity_id):
    """
    支持获取实体的身体角度

    :param entity_id:
    :return: float 身体绕竖直方向的角度，单位是角度，如果没有身体，返回为0
    """
    rot_comp = clientApi.GetEngineCompFactory().CreateRot(entity_id)
    return rot_comp.GetBodyRot()


def lock_local_player_rot(lock=True):
    # type: (bool) -> bool
    """
    在分离摄像机时，锁定本地玩家的头部角度

    * 只能设置local_player，即本地玩家自己
    * 玩家重生、切换维度时会重置头部角度
    * 锁定本地玩家头部角度时第一人称视角下可以旋转镜头，但玩家头部角度不会发生改变，下次切换到第一人称视角时镜头角度仍为锁定时的角度
    * 锁定本地玩家头部角度后，玩家划船时头部角度会尽量靠近锁定时的角度，若无法转到该角度，则会向左或向右看（视哪边距离目标角度更近而定）

    """
    rot_comp = clientApi.GetEngineCompFactory().CreateRot(local_player)
    return rot_comp.LockLocalPlayerRot(lock)


def set_player_look_at_pos(target_pos, pitch_step, yaw_step, block_input=True):
    """
    设置本地玩家看向某个位置

    当本地玩家未与摄像机分离时，调用本接口会导致摄像机一同看向指定位置

    当本地玩家与摄像机分离时，调用本接口将只改变本地玩家模型的朝向
    :param target_pos: tuple(float,float,float) 要看向的目标位置
    :param pitch_step: float 俯仰角方向旋转的角速度（每帧），最小为0.2
    :param yaw_step: float 偏航角方向旋转的角速度（每帧），最小为0.2
    :param block_input: bool 转向目标角度时是否屏蔽玩家操作，默认为True
        True:屏蔽玩家操作，此时玩家无法转向、移动
        False:不屏蔽玩家操作，此时如果玩家有移动、镜头转向操作将会打断通过本接口设置的转向
    :return:
    """
    rot_comp = clientApi.GetEngineCompFactory().CreateRot(local_player)
    return rot_comp.SetPlayerLookAtPos(target_pos, pitch_step, yaw_step, block_input)


def is_in_lava(entity_id):
    """
    获取实体是否在岩浆中

    :param entity_id:
    :return: bool 是否在岩浆中
    """
    attr_comp = clientApi.GetEngineCompFactory().CreateAttr(entity_id)
    return attr_comp.isEntityInLava()


def is_on_ground(entity_id):
    """
    获取实体是否触地

    * 客户端实体刚创建时引擎计算还没完成，此时获取该实体是否着地将返回默认值True，需要延迟一帧进行获取才能获取到正确的数据
    * 生物处于骑乘状态时，如玩家骑在猪身上，也视作触地
    * 只能获取到本地客户端已加载的实体是否触地，若实体在其他维度或未加载（距离本地玩家太远），将获取失败

    :param entity_id:
    :return: bool 是否触地
    """
    attr_comp = clientApi.GetEngineCompFactory().CreateAttr(entity_id)
    return attr_comp.isEntityOnGround()
