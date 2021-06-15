# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()


def set_fog_color(color):
    """
    设置雾效颜色
    
    :param color: tuple(float,float,float,float) 颜色RGBA，范围0到1之间，a值主要用于水下效果
    :return: bool 设置是否成功
    """
    fog_comp = clientApi.GetEngineCompFactory().CreateFog(level_id)
    return fog_comp.SetFogColor(color)


def reset_fog_color():
    """
    重置雾效颜色

    :return: bool 设置是否成功
    """
    fog_comp = clientApi.GetEngineCompFactory().CreateFog(level_id)
    return fog_comp.ResetFogColor()


def get_fog_use_color():
    """
    判断当前是否开启设置雾效颜色，该值默认为False，使用mod传入的颜色值后为True

    :return: bool 是否设置
    """
    fog_comp = clientApi.GetEngineCompFactory().CreateFog(level_id)
    return fog_comp.GetUseFogColor()


def get_fog_color():
    """
    获取当前雾效颜色

    :return: tuple(float,float,float,float) 颜色rgba
    """
    fog_comp = clientApi.GetEngineCompFactory().CreateFog(level_id)
    return fog_comp.GetFogColor()


def set_fog_length(start=None, end=None):
    """
    设置雾效范围

    :param start: float 雾效起始距离
    :param end: float 雾效终点范围
    :return: bool 设置是否成功
    """
    fog_comp = clientApi.GetEngineCompFactory().CreateFog(level_id)
    return fog_comp.SetFogLength(start, end)


def get_fog_length():
    """
    获取雾效范围

    :return: tuple(float,float) 雾效起始值与终点值
    """
    fog_comp = clientApi.GetEngineCompFactory().CreateFog(level_id)
    return fog_comp.GetFogLength()


def reset_fog_length():
    """
    重置雾效范围

    :return: bool 设置是否成功
    """
    fog_comp = clientApi.GetEngineCompFactory().CreateFog(level_id)
    return fog_comp.ResetFogLength()


def get_fog_use_length():
    """
    判断当前是否开启设置雾效范围,该值默认为False，使用mod传入的范围值后为True

    :return: bool 是否设置
    """
    fog_comp = clientApi.GetEngineCompFactory().CreateFog(level_id)
    return fog_comp.GetUseFogLength()


def set_show_name(entity_id, show):
    """
    设置生物名字是否按照默认游戏逻辑显示
    
    当设置为True时，生物的名字显示遵循游戏默认的渲染逻辑，即普通生物需要中心点指向生物才显示名字，玩家则是会一直显示名字
    
    :param entity_id:
    :param show: bool True为显示
    :return: bool 返回是否设置成功
    """
    name_comp = clientApi.GetEngineCompFactory().CreateName(entity_id)
    return name_comp.SetShowName(show)


def set_always_show_name(entity_id, show):
    """
    设置生物名字是否一直显示，瞄准点不指向生物时也能显示

    该接口只对普通生物生效，对玩家设置不起作用

    :param entity_id: str 生物id
    :param show: bool True为显示
    :return: bool 返回是否设置成功
    """
    name_comp = clientApi.GetEngineCompFactory().CreateName(entity_id)
    name_comp.SetAlwaysShowName(show)


def set_sky_color(color):
    """
    设置天空颜色
    
    :param color: tuple(float,float,float,float) 颜色RGBA，0到1之间，目前a值暂时没用
    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.SetSkyColor(color)


def reset_sky_color():
    """
    重置天空颜色

    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.ResetSkyColor()


def get_sky_color():
    """
    获取天空颜色

    :return: tuple(float,float,float,float) 颜色RGBA，0到1之间，目前a值暂时没用
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetSkyColor()


def get_use_sky_color():
    """
    判断是否在mod设置了天空颜色

    :return: bool 是否设置
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetUseSkyColor()


def set_sun_rot(rot):
    """
    设置太阳所在角度

    :param rot: tuple(float,float,float) 第一个float表示南北偏移，第三个float表示日升日落。单位为角度
    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.SetSunRot(rot)


def reset_sun_rot():
    """
    重置太阳角度

    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.ResetSunRot()


def get_sun_rot():
    """
    获取太阳角度

    :return: tuple(float,float,float) 第一个float表示南北偏移，第三个float表示日升日落。单位为角度
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetSunRot()


def get_use_sun_rot():
    """
    判断是否在mod设置了太阳角度

    :return: bool 是否设置
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetUseSunRot()


def set_moon_rot(rot):
    """
    设置月亮所在角度

    :param rot: tuple(float,float,float) 第一个float表示南北偏移，第三个float表示月升月落。单位为角度
    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.SetMoonRot(rot)


def reset_moon_rot():
    """
    重置月亮角度

    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.ResetMoonRot()


def get_moon_rot():
    """
    获取月亮角度

    :return: tuple(float,float,float) 第一个float表示南北偏移，第三个float表示月升月落。单位为角度
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetMoonRot()


def get_use_moon_rot():
    """
    判断是否在mod设置了月亮角度

    :return: bool 是否设置
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetUseMoonRot()


def set_ambient_brightness(brightness):
    """
    设置环境光亮度，影响天空亮度，不影响实体与方块光照

    :param brightness: float 范围0到1之间
    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.SetAmbientBrightness(brightness)


def reset_ambient_brightness():
    """
    重置环境光亮度

    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.ResetAmbientBrightness()


def get_ambient_brightness():
    """
    获取环境光亮度，影响天空亮度，不影响实体与方块光照

    :return: float 范围0到1之间
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetAmbientBrightness()


def get_use_ambient_brightness():
    """
    判断是否在mod设置了环境光亮度
    :return: bool 是否设置
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetUseAmbientBrightness()


def set_star_brightness(brightness):
    """
    设置星星亮度，白天也可以显示星星

    :param brightness:
    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.SetStarBrightness(brightness)


def reset_star_brightness():
    """
    重置星星亮度

    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.ResetStarBrightness()


def get_star_brightness():
    """
    获取星星亮度

    :return: float 范围0到1之间
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetStarBrightness()


def get_use_star_brightness():
    """
    判断是否在mod设置了星星亮度

    :return: bool 是否设置
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetUseStarBrightness()


def set_sky_textures(texture_list):
    """
    设置当前维度天空盒贴图，天空盒需要6张贴图

    贴图列表按顺序分别对应世界坐标的 负Z轴方向， 正X轴方向，正Z轴方向，负X轴方向，正Y轴方向，负Y轴方向。 其中正Y轴即为上方（采用右手坐标系）。

    游戏内切dimension的时候会重设天空盒贴图，因此开发者需要监听对应的切换维度事件(DimensionChangeClientEvent)进行贴图的处理。

    :param texture_list: list(str) 需要为6张贴图的路径，路径为从textures目录开始的绝对路径，如果天空盒某个方向不需要设置，则传空字符串
    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.SetSkyTextures(texture_list)


def get_sky_textures():
    """
    获取当前维度天空盒贴图，天空盒共6张贴图

    贴图列表按顺序分别对应世界坐标的 负Z轴方向， 正X轴方向，正Z轴方向，负X轴方向，正Y轴方向，负Y轴方向。 其中正Y轴即为上方（采用右手坐标系）。

    :return: list(str)或None 天空盒贴图列表，该值可能为None
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.GetSkyTextures()


def reset_sky_textures():
    """
    重置当前维度天空盒贴图。如果有使用addon配置贴图则会使用配置的贴图，否则为游戏内默认无贴图的情况

    :return: bool 设置是否成功
    """
    sky_render_comp = clientApi.GetEngineCompFactory().CreateSkyRender(level_id)
    return sky_render_comp.ResetSkyTextures()
