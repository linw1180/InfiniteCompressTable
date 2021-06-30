# -*- coding: utf-8 -*-
import json

import mod.client.extraClientApi as clientApi
from mod.common.minecraftEnum import TouchEvent

from ._base_ui import BaseUI
from .. import get_ui_manager
from ..api import get_item_basic_info, get_item_formatted_hover_text, notify_to_server, local_player, \
    get_item_hover_name, add_timer
from ..utils.container_interaction_state_utils import ButtonEventType, NodeId, ContainerInteractionStateMachine
from ..utils.fly_image_utils import FlyImage
from ...modCommon.config.custom_container_config import DOUBLE_CLICK_INTERVAL, FLY_ANIMATION_DURATION, \
    LIMITED_COMPRESS_TABLE_ITEM_DETAIL_ALPHA
from ...modCommon.utils.item_utils import is_same_item
from ...modCommon.utils.log_utils import func_log

ViewBinder = clientApi.GetViewBinderCls()


def get_durability_ratio(item_dict):
    """
    计算耐久度比例

    :param item_dict:
    :return:
    """
    basic_info = get_item_basic_info(item_dict.get("itemName", ""), item_dict.get("auxValue", 0))
    if basic_info:
        current_durability = item_dict.get("durability")
        if current_durability is None:
            return 1
        max_durability = basic_info.get("maxDurability", 0)
        if max_durability != 0:
            return current_durability * 1.0 / max_durability
    return 1


class NewBaseCustomContainerUIScreen(BaseUI):

    def __init__(self, namespace, name, param):
        super(NewBaseCustomContainerUIScreen, self).__init__(namespace, name, param)
        # region 控件路径
        self.main_panel_path = "/main_panel"

        self.progressive_bar_path = self.main_panel_path + "/progressive_bar"  # 按压条

        self.item_detail_panel_path = self.main_panel_path + "/item_detail"  # item_detail物品信息框
        self.item_detail_text_path = self.item_detail_panel_path + "/item_detail_bg/item_detail_text"

        self.fly_img_template_path = self.main_panel_path + "/fly_img_template"  # 飞行动画模板

        # 背包网格相关路径
        # self.inv_grid_path = self.main_panel_path + "/scroll_inv/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"
        self.inv_grid_path = self.main_panel_path + '/inv_grid'
        self.item_btn_path_prefix = self.inv_grid_path + "/item_btn"

        self.custom_container_panel_path = self.main_panel_path + "/armor_panel"  # 自定义槽位面板，用于控制飞行动画位置

        # 新增的自定义按鈕
        self.from_item_button_path = "/input_btn"
        self.to_item_button_path = "/output_btn"

        self.item_name = '/pe_kuang_image/item_name'  # 压缩物品名
        self.msg1 = '/pe_kuang_image/msg1'  # 放入框提示信息
        self.compress_count = '/pe_kuang_image/compress_count'  # 已压缩数量
        self.text_edit_box0 = '/pe_kuang_image/text_edit_box0'  # 待输入的解压缩数量
        self.take_out_btn = '/pe_kuang_image/take_out_btn'  # 取出按钮
        self.msg2 = '/pe_kuang_image/msg2'  # 取出操作提示信息

        self.btn_exit = '/bg_panel/bg/btn_exit'  # 退出按钮

        # endregion

        # region 管理背包数据及各个槽位对应的路径
        self.bag_info = {}
        self.slot_to_path = {}
        self.already_register_item_btn = []
        # endregion

        # region 管理飞行动画相关数据
        self.fly_img_pool = []
        self.fly_img_index = 0
        self.fly_animation_time = 0
        # endregion

        self.item_detail_alpha = 0.0  # 用于渐变显示物品详细信息

        # region 点击状态机
        self.container_state_machine = ContainerInteractionStateMachine()
        self.register_state_machine()
        # endregion

        # region 用于判断点击事件
        self.last_selected_path = None
        self.last_touch_button = None
        self.last_touch_pos = None
        self.touching = False
        self.click_interval = 0
        self.held_time = None
        self.double_click = False
        self.take_percent = 1
        # endregion

        # region 容器方块信息
        self.block_pos = None
        self.dimension = None
        self.block_name = None

    # endregion

    # 注册自定义按钮
    def on_ui_create(self):
        self.AddTouchEventHandler(self.from_item_button_path, self.on_item_btn_touch, {"isSwallow": True})
        self.AddTouchEventHandler(self.to_item_button_path, self.on_item_btn_touch, {"isSwallow": True})
        self.AddTouchEventHandler(self.btn_exit, self.close, {"isSwallow": True})
        self.AddTouchEventHandler(self.take_out_btn, self.on_take_out, {"isSwallow": True})

    def on_take_out(self, args):
        if args['TouchEvent'] == TouchEvent.TouchUp:
            pass

    def close(self, args):
        if args['TouchEvent'] == TouchEvent.TouchUp:
            get_ui_manager().pop_ui()

    # 注册网格中的按钮
    def register_item_btn_event(self, item_btn_path):
        if item_btn_path in self.already_register_item_btn:
            return
        self.AddTouchEventHandler(item_btn_path, self.on_item_btn_touch, {"isSwallow": True})

    def update_bag_ui(self, args):
        pass

    def refresh_bag_ui(self):
        pass

    @func_log
    def handle_swap(self, button_path):
        if not self.last_selected_path:
            print "there is no last selected button, swap failed!!!"
            return
        from_item = self.get_item_by_path(self.last_selected_path)
        to_item = self.get_item_by_path(button_path)
        if from_item:
            from_item_detail_text = get_item_formatted_hover_text(from_item["itemName"], from_item["auxValue"], True,
                                                                  from_item.get("userData"))
        else:
            from_item_detail_text = ''
        if to_item:
            to_item_detail_text = get_item_formatted_hover_text(to_item["itemName"], to_item["auxValue"], True,
                                                                to_item.get("userData"))
        else:
            to_item_detail_text = ''
        notify_to_server('OnItemSwapClientEvent', {
            "block_name": self.block_name,
            "from_slot": self.get_slot_by_path(self.last_selected_path),
            "to_slot": self.get_slot_by_path(button_path),
            "player_id": local_player,
            "from_item": self.get_item_by_path(self.last_selected_path),
            "to_item": self.get_item_by_path(button_path),
            "block_pos": self.block_pos,
            "dimension": self.dimension,
            "take_percent": self.take_percent,
            "from_item_detail_text": from_item_detail_text,
            "to_item_detail_text": to_item_detail_text
        })
        self.container_state_machine.reset_to_default()

    def validate_scroll_grid_path(self):
        bag_grid_list = self.GetChildrenName(self.inv_grid_path)
        if not bag_grid_list:
            # PC版touch模式和鼠标模式scroll的路径不一致。
            # self.inv_grid_path = self.main_panel_path + "/scroll_inv/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content"
            self.inv_grid_path = self.main_panel_path + '/inv_grid'
            self.item_btn_path_prefix = self.inv_grid_path + "/item_btn"
            bag_grid_list = self.GetChildrenName(self.inv_grid_path)
            if not bag_grid_list:
                print "xxxxx Get Bag Grid List Error ! xxxxx"
                return
        return bag_grid_list

    @ViewBinder.binding(ViewBinder.BF_BindFloat, LIMITED_COMPRESS_TABLE_ITEM_DETAIL_ALPHA)
    def on_detail_show(self):
        if self.item_detail_alpha > 1:
            return 1.0
        return self.item_detail_alpha

    def show_item_detail(self, item):
        detail_text = get_item_formatted_hover_text(item["itemName"], item["auxValue"], True, item.get("userData"))
        self.GetBaseUIControl(self.item_detail_text_path).asLabel().SetText(detail_text)
        self.item_detail_alpha = 2.0

    # def InitScreen(self):
    #     self.HideUI(

    # def InitCustomContainerUI(self, args):
    #     """初始化自定义容器的UI，由子类覆写"""
    #     pass

    # 网格按钮点击回调函数
    def on_item_btn_touch(self, args):
        touch_event = args["TouchEvent"]
        touch_pos = args["TouchPosX"], args["TouchPosY"]
        # 触控在按钮范围内弹起时
        if touch_event == TouchEvent.TouchUp:
            if self.double_click:
                self.container_state_machine.receive_event(args["ButtonPath"], ButtonEventType.DoubleClick)
            elif self.held_time and self.held_time < 10:
                self.container_state_machine.receive_event(args["ButtonPath"], ButtonEventType.Clicked)
            else:
                self.container_state_machine.receive_event(args["ButtonPath"], ButtonEventType.Released)
            self.touching = False
            self.held_time = None
            self.click_interval = DOUBLE_CLICK_INTERVAL
        # 按钮按下时
        elif touch_event == TouchEvent.TouchDown:
            item = self.get_item_by_path(args["ButtonPath"])
            if item:
                self.show_item_detail(item)
            if self.click_interval > 0 and self.last_touch_button == args["ButtonPath"]:
                self.double_click = True
                return
            self.double_click = False
            self.touching = True
            self.held_time = 0
            self.last_touch_button = args["ButtonPath"]
            self.last_touch_pos = touch_pos
        # 触控在按钮范围外弹起时
        elif touch_event == TouchEvent.TouchCancel:
            self.on_touch_cancel()
        # 按下后触控移动时
        elif touch_event == TouchEvent.TouchMove:
            self.on_touch_cancel()
        elif touch_event == TouchEvent.TouchMoveIn:
            pass
        elif touch_event == TouchEvent.TouchMoveOut:
            self.container_state_machine.receive_event(self.last_touch_button, ButtonEventType.Released)

    def on_touch_cancel(self):
        self.container_state_machine.receive_event(None, ButtonEventType.Released)

    def handle_idle(self, button_path):
        self.touching = False
        self.click_interval = 0
        self.held_time = None
        self.last_touch_button = None
        self.double_click = False
        self.take_percent = 1
        self.GetBaseUIControl(self.progressive_bar_path).SetVisible(False)
        if self.last_selected_path:
            self.GetBaseUIControl(self.last_selected_path + "/img_selected").SetVisible(False)
            self.last_selected_path = None

    def handle_selected(self, button_path):
        self.last_selected_path = button_path
        self.GetBaseUIControl(self.last_selected_path + "/img_selected").SetVisible(True)

    def handle_un_selected(self, button_path):
        self.container_state_machine.reset_to_default()

    def handle_drop_all(self, button_path):
        if not self.last_selected_path:
            print "there is no last selected button, drop failed!!!"
            return
        notify_to_server('OnItemDropClientEvent', {
            "blockName": self.block_name,
            "playerId": local_player,
            "blockPos": self.block_pos,
            "dimension": self.dimension,
            "slot": self.get_slot_by_path(self.last_selected_path),
            "item": self.get_item_by_path(self.last_selected_path)
        })
        self.container_state_machine.reset_to_default()

    def handle_touch_progressive_select(self, button_path):
        self.handle_selected(button_path)
        panel_x, panel_y = self.GetBaseUIControl(self.main_panel_path).GetPosition()
        progressive_bar = self.GetBaseUIControl(self.progressive_bar_path)
        progressive_bar.SetPosition((self.last_touch_pos[0] - panel_x - 8, self.last_touch_pos[1] - panel_y - 10))
        progressive_bar.SetVisible(True)

    def handle_touch_progressive_complete(self, button_path):
        self.held_time = None

    def handle_touch_progressive_cancel(self, button_path):
        self.container_state_machine.reset_to_default()

    def handle_coalesce(self, button_path):
        if isinstance(self.get_slot_by_path(button_path), str):
            # 非背包栏位禁止合堆
            self.container_state_machine.reset_to_default()
        item_dict = self.get_item_by_path(button_path)
        basic_info = get_item_basic_info(item_dict.get("itemName", ""), item_dict.get("auxValue", 0))

        if basic_info:
            max_size = basic_info.get("maxStackSize")
            if 1 < max_size != item_dict.get("count"):
                for path, bagInfo in self.bag_info.items():
                    if button_path == path or isinstance(self.get_slot_by_path(path), str):
                        continue
                    item = self.get_item_by_path(path)
                    if is_same_item(item, item_dict) and item.get("count") != max_size:
                        self.last_selected_path = path
                        self.handle_swap(button_path)
        self.GetBaseUIControl(button_path + "/img_selected").SetVisible(False)
        self.container_state_machine.reset_to_default()

    def get_bag_item_position(self, item_path):
        """计算背包控件相对于main_panel的位置，用于飞行动画"""
        # pos1 = self.GetBaseUIControl(self.main_panel_path + "/scroll_inv").GetPosition()
        pos1 = self.GetBaseUIControl(self.main_panel_path + '/inv_grid').GetPosition()
        pos2 = self.GetBaseUIControl(item_path).GetPosition()
        return pos1[0] + pos2[0] + 2, pos1[1] + pos2[1] + 2

    def get_custom_container_panel_item_position(self, item_path):
        """计算RightPanel控件相对于ContentPanel的位置，用于飞行动画"""
        pos1 = self.GetBaseUIControl(self.custom_container_panel_path).GetPosition()
        pos2 = self.GetBaseUIControl(item_path).GetPosition()
        return pos1[0] + pos2[0] + 4, pos1[1] + pos2[1] + 4

    def is_custom_container_panel(self, path):
        """判断是否为RightPanel子控件"""
        if path.startswith(self.custom_container_panel_path):
            return True
        return False

    def get_item_position(self, item_path):
        if self.is_custom_container_panel(item_path):
            return self.get_custom_container_panel_item_position(item_path)
        return self.get_bag_item_position(item_path)

    def set_item_at_path(self, item_path, item):
        self.bag_info[item_path]["item"] = item

    def get_item_by_path(self, item_path):
        return self.bag_info[item_path]["item"]

    def get_slot_by_path(self, path):
        return self.bag_info[path]["slot"]

    # 丢弃物品
    # def drop_item(self, slot):
    #     drop_path = self.slot_to_path[slot]
    #     self.set_slot_item_btn(drop_path, None)
    #     self.set_item_at_path(drop_path, None)

    # 交换物品
    @func_log
    def swap_item(self, args):

        from_slot = args["from_slot"]
        to_slot = args["to_slot"]
        from_path = self.slot_to_path[from_slot]
        to_path = self.slot_to_path[to_slot]
        from_item = args["from_item"]
        to_item = args["to_item"]

        # 根据路径获取BaseUIControl实例
        item_name_ctrl = self.GetBaseUIControl(self.item_name).asLabel()
        compress_count_ctrl = self.GetBaseUIControl(self.compress_count).asLabel()

        # 更新飞行动画
        self.fly_animation_time = FLY_ANIMATION_DURATION
        from_pos = self.get_item_position(from_path)
        to_pos = self.get_item_position(to_path)

        self._update_fly_image(from_item, from_pos, to_pos)
        if to_item and not is_same_item(from_item, to_item):
            self._update_fly_image(to_item, to_pos, from_pos)

        self.swap_item_ui(from_path, to_path, from_item, to_item)

        self.set_item_at_path(from_path, to_item)
        self.set_item_at_path(to_path, from_item)

        # 往放入框中放入物品时，输出框中也应该有相同物品数据
        if to_path == '/input_btn':
            to_path = '/output_btn'
            self.swap_item_ui(from_path, to_path, from_item, to_item)
            self.set_item_at_path(from_path, to_item)
            self.set_item_at_path(to_path, from_item)

            # 设置物品名称显示
            item_name_text = get_item_hover_name(from_item['itemName'], from_item['auxValue'], from_item['userData'])
            item_name_ctrl.SetText(item_name_text)
            # 设置已压缩数量显示
            extra_id_dict = json.loads(from_item['extraId'])
            compress_count_text = extra_id_dict['compress_count']
            compress_count_ctrl.SetText(str(compress_count_text))

        # 物品不进行解压缩，取出返还到背包时，输出框物品也相应被取出
        if from_path == '/input_btn':
            from_path = '/output_btn'
            self.swap_item_ui(from_path, to_path, from_item, to_item)
            self.set_item_at_path(from_path, to_item)
            self.set_item_at_path(to_path, from_item)

            # 当放入框物品被放回背包时，重置显示的物品名和已压缩数量
            item_name_ctrl.SetText('')
            compress_count_ctrl.SetText('')

        # TODO 清空物品名和已压缩数量显示时机：放入框没有物品时
        # if from_path == '/input_btn':
        #     from_path = '/output_btn'
        #     self.swap_item_ui(from_path, to_path, from_item, to_item)
        #     self.set_item_at_path(from_path, to_item)
        #     self.set_item_at_path(to_path, from_item)
        # # 恢复默认文本显示
        # # set_label_default()
        #
        # if from_path == '/output_btn':
        #     from_path = '/input_btn'
        #     self.swap_item_ui(from_path, to_path, from_item, to_item)
        #     self.set_item_at_path(from_path, to_item)
        #     self.set_item_at_path(to_path, from_item)
        # # 恢复默认文本显示
        # # set_label_default()

    def _update_fly_image(self, from_item, from_pos, to_pos):
        if not from_item:
            return
        fly_image = self.get_fly_img()
        fly_image.init_pos(from_pos, to_pos)
        self.SetUiItem(fly_image.get_path(), from_item["itemName"], from_item["auxValue"],
                       from_item.get("enchantData", False), from_item.get("userData"))
        img_widget = self.GetBaseUIControl(fly_image.get_path())
        img_widget.SetPosition(from_pos)
        img_widget.SetVisible(True)

    def swap_item_ui(self, from_path, to_path, from_item, to_item):
        self.set_slot_item_btn(from_path, to_item)
        self.set_slot_item_btn(to_path, from_item)

    def set_slot_item_btn(self, path, item):
        """
        设置目标槽位item渲染

        :param path: item_btn控件路径
        :param item: 物品字典
        :return:
        """
        # if path == self.from_item_button_path or path == self.to_item_button_path:
        #     path += '/item_btn'
        item_renderer = self.GetBaseUIControl(path + "/item_renderer")
        if item and item.get("count"):
            # 设置耐久
            self.set_durability_bar(path, item)
            # 设值附魔
            is_enchant = False
            if item.get("enchantData"):
                is_enchant = True
            user_data = item.get("userData")
            self.SetUiItem(path + "/item_renderer", item["itemName"], item["auxValue"], is_enchant, user_data)
            item_renderer.SetVisible(True)

            item_num = self.GetBaseUIControl(path + "/item_renderer/item_num").asLabel()
            if item["count"] > 1:
                item_num.SetText(str(item["count"]))
            else:
                item_num.SetText("")
        else:
            item_renderer.SetVisible(False)
            self.GetBaseUIControl(path + "/durability_bar").SetVisible(False)

    def set_durability_bar(self, path, item):
        """
        设置目标槽位耐久度UI

        :param path:
        :param item:
        :return:
        """
        durability_ratio = get_durability_ratio(item)
        durability_bar = self.GetBaseUIControl(path + "/durability_bar")
        if durability_ratio != 1:
            img_bar = self.GetBaseUIControl(path + "/durability_bar/bar_mask").asImage()
            img_bar.SetSpriteColor((1 - durability_ratio, durability_ratio, 0))
            img_bar.SetSpriteClipRatio(1 - durability_ratio)
            durability_bar.SetVisible(True)
        else:
            durability_bar.SetVisible(False)

    def set_progressive_bar(self):
        """设置长按分堆进度条"""
        if not self.last_touch_button:
            print "set_progressive_bar Error!!! No Last Touch Button!!!"
            return
        item = self.get_item_by_path(self.last_touch_button)
        if not item:
            print "set_progressive_bar Error!!! Try progressive none item!!!"
            return
        self.get_progressive_ratio(item)
        bar_path = self.progressive_bar_path + "/bar_mask"
        self.GetBaseUIControl(bar_path).asImage().SetSpriteClipRatio(1 - self.take_percent)

    def get_progressive_ratio(self, item_dict):
        if self.held_time is None:
            print "Enter Progressive State But The Held Time is None!!!"
            return
        held_time = self.held_time - 10
        if held_time > 20:
            self.take_percent = 1
            return
        total_num = item_dict.get("count")
        take_num = held_time * total_num / 20
        if take_num == 0:
            take_num = 1
            self.held_time = take_num * 20 / total_num + 10
        self.take_percent = take_num * 1.0 / total_num

    # def hide_ui(self):
    #     if self.mIsHide:
    #         return
    #     clientApi.HideHudGUI(False)
    #     clientApi.SetInputMode(0)
    #     clientApi.SetResponse(True)
    #     self.SetVisible(self.main_panel_path, False)
    #     self.mIsHide = True

    def update_custom_container_ui(self):
        """更新自定义容器中内容"""
        pass

    def get_fly_img(self):
        """获取飞行图片控件，优先从控件池里获取"""
        for fly_img in self.fly_img_pool:
            if not fly_img.is_using():
                return fly_img
        new_img_name = "fly_img{0}".format(self.fly_img_index)
        self.fly_img_index += 1
        self.Clone(self.fly_img_template_path, self.main_panel_path, new_img_name)
        new_fly_img = FlyImage("{0}/{1}".format(self.main_panel_path, new_img_name))
        self.fly_img_pool.append(new_fly_img)
        return new_fly_img

    def can_selected(self, button_path, button_event):
        # type: (str,int) -> bool
        # if button_path == self.mDropAreaPath or not button_path:
        if not button_path:
            return False
        item = self.get_item_by_path(button_path)
        if item and button_event == ButtonEventType.Clicked:
            return True
        return False

    def can_un_selected(self, button_path, button_event):
        return button_path == self.last_selected_path and button_event == ButtonEventType.Clicked

    def can_swap(self, button_path, button_event):
        return button_path and button_path != self.last_selected_path and button_event == ButtonEventType.Clicked

    def can_drop(self, button_path, button_event):
        return button_path == '' and self.last_selected_path and button_event == ButtonEventType.Clicked

    def can_progressive_select(self, button_path, button_event):
        if not button_path:
            return False
        item_dict = self.get_item_by_path(button_path)
        if not item_dict or button_event != ButtonEventType.Pressed:
            return False
        basic_info = get_item_basic_info(item_dict.get("itemName", ""), item_dict.get("auxValue", 0))
        if basic_info:
            max_size = basic_info.get("maxStackSize")
            if max_size > 1:
                return True
        return False

    @staticmethod
    def can_progressive_cancel(button_path, button_event):
        return not button_path and button_event == ButtonEventType.Released

    @staticmethod
    def can_progressive_complete(button_path, button_event):
        return button_path and button_event == ButtonEventType.Released

    @staticmethod
    def can_coalesce(button_path, button_event):
        return button_event == ButtonEventType.DoubleClick

    # noinspection DuplicatedCode
    def register_state_machine(self):
        # 注册状态节点
        self.container_state_machine.add_node(NodeId.Idle, self.handle_idle, None, True)
        self.container_state_machine.add_node(NodeId.SelectSlot, self.handle_selected)
        self.container_state_machine.add_node(NodeId.UnSelectSlot, self.handle_un_selected)
        self.container_state_machine.add_node(NodeId.Swap, self.handle_swap)
        self.container_state_machine.add_node(NodeId.DropAll, self.handle_drop_all)
        self.container_state_machine.add_node(NodeId.TouchProgressiveSelect, self.handle_touch_progressive_select)
        self.container_state_machine.add_node(NodeId.TouchProgressiveSelectComplete,
                                              self.handle_touch_progressive_complete)
        self.container_state_machine.add_node(NodeId.TouchProgressiveSelectCancel, self.handle_touch_progressive_cancel)
        self.container_state_machine.add_node(NodeId.Coalesce, self.handle_coalesce)
        # 注册状态转移条件
        self.container_state_machine.add_edge(NodeId.Idle, NodeId.SelectSlot, self.can_selected)
        self.container_state_machine.add_edge(NodeId.SelectSlot, NodeId.UnSelectSlot, self.can_un_selected)
        self.container_state_machine.add_edge(NodeId.SelectSlot, NodeId.Swap, self.can_swap)
        self.container_state_machine.add_edge(NodeId.SelectSlot, NodeId.DropAll, self.can_drop)
        self.container_state_machine.add_edge(NodeId.SelectSlot, NodeId.Coalesce, self.can_coalesce)
        self.container_state_machine.add_edge(NodeId.Idle, NodeId.TouchProgressiveSelect, self.can_progressive_select)
        self.container_state_machine.add_edge(NodeId.TouchProgressiveSelect, NodeId.TouchProgressiveSelectComplete,
                                              self.can_progressive_complete)
        self.container_state_machine.add_edge(NodeId.TouchProgressiveSelect, NodeId.TouchProgressiveSelectCancel,
                                              self.can_progressive_cancel)
        self.container_state_machine.add_edge(NodeId.TouchProgressiveSelectComplete, NodeId.Swap, self.can_swap)
        self.container_state_machine.add_edge(NodeId.TouchProgressiveSelectComplete,
                                              NodeId.TouchProgressiveSelectCancel, self.can_un_selected)

    def show_ui(self, **kwargs):
        if self.last_selected_path:
            self.SetVisible(self.last_selected_path + "/img_selected", False)
            self.last_selected_path = None
        self.dimension = kwargs["dimension"]
        self.block_name = kwargs["block_name"]
        if kwargs.get("pos"):
            self.block_pos = kwargs["pos"]
        else:
            self.block_pos = None
        self.container_state_machine.reset_to_default()

    def tick(self):
        """
        继承自ScreenNode的方法，会被引擎自动调用，1秒钟30帧

        :return:
        """
        # 更新长按分堆
        if self.held_time is not None:
            self.held_time += 1
            if self.held_time == 10:
                self.container_state_machine.receive_event(self.last_touch_button, ButtonEventType.Pressed)
            if self.container_state_machine.get_current_node_id() == NodeId.TouchProgressiveSelect:
                self.set_progressive_bar()
        # 双击间隔
        if self.click_interval > 0:
            self.click_interval -= 1
        # 更新物品详细信息透明度
        if self.item_detail_alpha > 0:
            self.item_detail_alpha -= 0.04
        # 更新飞行动画
        if self.fly_animation_time > 0:
            self.fly_animation_time -= 1
            for fly_img in self.fly_img_pool:
                if fly_img.is_using():
                    img_widget = self.GetBaseUIControl(fly_img.get_path())
                    img_widget.SetPosition(fly_img.update_current_pos())
                    if self.fly_animation_time == 0:
                        fly_img.release()
                        img_widget.SetVisible(False)

    def show_short_time_msg1(self, args):
        """
        短时间展示msg1提示信息
        """
        # 根据路径获取BaseUIControl实例
        msg1_ctrl = self.GetBaseUIControl(self.msg1).asLabel()
        msg1_ctrl.SetText("该物品未压缩")
        # 延迟三秒清空该提示信息
        add_timer(3.0, msg1_ctrl.SetText, '')
