# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

level_id = clientApi.GetLevelId()


def set_board_text(board_id, text):
    """
    设置文字面板内容

    :param board_id: int	文字面板id
    :param text: str 文字内容
    :return: bool 是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(clientApi.GetLevelId())
    return text_board_comp.SetText(board_id, text)


def set_board_depth_test(board_id, depth_test=False):
    """
    设置是否开启深度测试, 默认状态下是开启
    
    :param board_id: int 文字面板的id
    :param depth_test: bool True为开启深度测试,False为不开启
    :return: bool 返回是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.SetBoardDepthTest(board_id, depth_test)


def set_board_scale(board_id, scale):
    """
    内容整体缩放

    :param board_id: int 文字面板的id
    :param scale: tuple(float,float) x,y方向上的缩放值,要求值大于0,正常状态下是(1.0,1.0)
    :return: bool 返回是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.SetBoardScale(board_id, scale)


def set_board_background_color(board_id, background_color):
    """
    修改背景颜色

    :param board_id: int 文字面板的id
    :param background_color: tuple(float,float,float,float) 颜色的RGBA值，范围0-1
    :return: bool 返回是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.SetBoardBackgroundColor(board_id, background_color)


def set_board_pos(board_id, pos):
    """
    修改位置

    :param board_id: int 文字面板的id
    :param pos: tuple(float,float,float) 坐标
    :return: bool 返回是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.SetBoardPos(board_id, pos)


def set_board_rot(board_id, rot):
    """
    修改旋转角度, 若设置了文本朝向相机，则旋转角度的修改不会生效

    :param board_id: int 文字面板的id
    :param rot: tuple(float,float,float) 角度(不是弧度)
    :return: bool 返回是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.SetBoardRot(board_id, rot)


def set_board_text_color(board_id, text_color):
    """
    修改字体颜色

    :param board_id: int 文字面板的id
    :param text_color: tuple(float,float,float,float) 颜色的RGBA值，范围0-1
    :return: bool 返回是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.SetBoardTextColor(board_id, text_color)


def set_board_bind_entity(board_id, bind_entity_id, offset=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0)):
    """
    文字面板绑定实体对象

    :param board_id: int 文字面板的id
    :param bind_entity_id: str 绑定entity的Id; 如果为None，则为取消实体绑定, 此时下面参数为世界坐标和旋转
    :param offset: tuple(float,float,float) 相对于实体的偏移量
    :param rot: tuple(float,float,float) 相对于实体的偏移角度
    :return: bool 返回是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.SetBoardBindEntity(board_id, bind_entity_id, offset, rot)


def set_board_face_camera(board_id, face_camera=True):
    """
    设置文字面板的朝向
    
    :param board_id: int 文字面板的id
    :param face_camera: bool 是否始终朝向相机, 默认为True
    :return: bool 返回是否设置成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.SetBoardFaceCamera(board_id, face_camera)


def create_text_board_in_world(text, text_color, board_color=None, face_camera=True):
    """
    创建文字面板
    
    切换维度后会自动隐藏非本维度创建的而且没有绑定实体的文字面板, 回到该维度后会自动重新显示
    
    :param text: str 文字显示内容
    :param text_color: tuple(float,float,float,float) 文字颜色的RGBA值，范围0-1
    :param board_color: tuple(float,float,float,float) 可选参数，默认None，设置为黑色，面板颜色的RGBA值，范围0-1
    :param face_camera: bool 是否始终朝向相机, 默认为True
    :return: int 返回生成的id，如果生成失败，返回None
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.CreateTextBoardInWorld(text, text_color, board_color, face_camera)


def remove_text_board(board_id):
    """
    删除文字面板

    :param board_id: int 创建的时候返回的id
    :return: bool 是否删除成功
    """
    text_board_comp = clientApi.GetEngineCompFactory().CreateTextBoard(level_id)
    return text_board_comp.RemoveTextBoard(board_id)
