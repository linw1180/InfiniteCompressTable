# -*- coding: utf-8 -*-

from mod.common.minecraftEnum import TouchEvent

from infiniteCompressTableScripts.modClient.api import add_timer, notify_to_server, local_player
from infiniteCompressTableScripts.modClient.ui._base_custom_container_ui import BaseCustomContainerUIScreen
from infiniteCompressTableScripts.modClient.utils.ui_utils import get_ui_manager
from infiniteCompressTableScripts.modCommon.utils.log_utils import func_log


class InfiniteCompressTableUIScreen(BaseCustomContainerUIScreen):

    def __init__(self, namespace, name, param):
        super(InfiniteCompressTableUIScreen, self).__init__(namespace, name, param)
        # self.img_eu_anim = '/main_panel/bottom_panel/eu_panel/eu_anim'
        # self.eu_nums_path = '/main_panel/bottom_panel/eu_panel/eu_nums/'
        # self.img_msg = '/main_panel/bottom_panel/img_msg'
        self.paper_doll = '/main_panel/paper_doll'
        self.btn_exit = '/bg_panel/bg/btn_exit'  # 套用
        self.hide_tips_path = '/bg_panel/hide_tips_message'
        self.inv_grid_path = '/main_panel/inv_grid'  # 套用
        self.item_btn_path_prefix = self.inv_grid_path + "/item_btn"

        # self.moying_panle_path = "/main_panel/grid0"

        # self.search_panel_grid_path = "/main_panel/panel0/grid1"

        # self.moying_btn_path_prefix = self.moying_panle_path + "/item_btn"
        # self.page_path = "/bg_panel/bg/panel1"
        # self.search_panel_path = "/main_panel/panel0"
        # self.search_data = {}

        # region custom

        # endregion

        self.box_size = []
        self.text = None
        # self.mGridPath = self.scroll_panel_path + "/scroll_touch/scroll_view/panel/background_and_viewport/scrolling_view_port/scrolling_content"

    @func_log
    def on_ui_create(self):
        super(InfiniteCompressTableUIScreen, self).on_ui_create()
        self.AddTouchEventHandler(self.btn_exit, self.close, {"isSwallow": True})

    @func_log
    def show_ui(self, **kwargs):
        super(InfiniteCompressTableUIScreen, self).show_ui(**kwargs)

    def tick(self):
        super(InfiniteCompressTableUIScreen, self).tick()

    @staticmethod
    def close(args):
        if args['TouchEvent'] == TouchEvent.TouchUp:
            get_ui_manager().pop_ui()

    @func_log
    def update_bag_ui(self, args):

        # 更新背包UI
        for i in xrange(36):
            item_btn_path = self.item_btn_path_prefix + str(i + 1)
            item_dict = args[i]
            self.bag_info[item_btn_path] = {"slot": i, "item": item_dict}
            self.slot_to_path[i] = item_btn_path

        self.refresh_bag_ui()

    def refresh_bag_ui(self):
        # 获取网格的子节点list（网格子节点其实就是按钮，此处获取的就是按钮名list）
        bag_grid_list = self.validate_scroll_grid_path()
        if not bag_grid_list:
            return

        for item_btn in bag_grid_list:
            item_btn_path = self.inv_grid_path + "/" + item_btn
            if item_btn_path not in self.bag_info:
                continue
            # 设置目标槽位Item渲染
            self.set_slot_item_btn(item_btn_path, self.bag_info[item_btn_path]['item'])
            self.register_item_btn_event(item_btn_path)

    def validate_scroll_grid_path(self):
        bag_grid_list = self.GetChildrenName(self.inv_grid_path)
        return bag_grid_list

    def handle_swap(self, button_path):
        if not self.last_selected_path:
            print "there is no last selected button, swap failed!!!"
            return
        self.pages = self.GetBaseUIControl(self.page_text_path).asTextEditBox().GetEditText()
        if not self.pages:
            self.pages = "1"

        if self.pages.isdigit():
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
                "flag": self.last_selected_path,
                'search_data': self.search_data,
                "pages": int(self.pages)
            })
            self.container_state_machine.reset_to_default()

    # @ViewBinder.binding(ViewBinder.BF_EditChanged | ViewBinder.BF_EditFinished)
    # def message_text_edit_box0(self, args):
    #     self.pages = args["Text"]
    #     if not self.pages.isdigit():
    #         self.pages = ""
    #
    #     if self.pages == '0':
    #         self.pages = ""
    #
    #     if args['Finish']:
    #         if self.pages.isdigit():
    #             notify_to_server('OnPageUpdateEvent', {
    #                 "blockName": self.block_name,
    #                 "playerId": local_player,
    #                 "dimensionId": self.dimension,
    #                 "pages": self.pages,
    #                 "state": True
    #             })
    #         else:
    #             notify_to_server('OnPageUpdateEvent', {
    #                 "blockName": self.block_name,
    #                 "playerId": local_player,
    #                 "dimensionId": self.dimension,
    #                 "pages": 1,
    #                 "state": True
    #             })
    #             text = self.GetBaseUIControl(self.page_text_path).asTextEditBox()
    #             text.SetEditText("1")
    #     return ViewRequest.Refresh

    # @ViewBinder.binding(ViewBinder.BF_BindString)
    # def message_content_text_edit_box0(self):
    #     return self.pages

    # @ViewBinder.binding(ViewBinder.BF_EditChanged | ViewBinder.BF_EditFinished)
    # def message_text_edit_box1(self, args):
    #     self.text = args["Text"]
    #     if args['Finish']:
    #         notify_to_server('OnSearchItemEvent', {
    #             "blockName": self.block_name,
    #             "playerId": local_player,
    #             "dimensionId": self.dimension,
    #             "state": True,
    #             "text": self.text
    #         })
    #     return ViewRequest.Refresh

    # @ViewBinder.binding(ViewBinder.BF_BindString)
    # def message_content_text_edit_box1(self):
    #     return self.text

    def on_search_btn_touch(self, args):
        if args['TouchEvent'] == TouchEvent.TouchUp:
            if not self.GetBaseUIControl(self.search_panel_path).GetVisible():
                notify_to_server('OnSearchItemEvent', {
                    "blockName": self.block_name,
                    "playerId": local_player,
                    "dimensionId": self.dimension,
                    "pages": 1,
                    "block_pos": self.block_pos,
                    "state": True
                })
                self.GetBaseUIControl(self.search_panel_path).SetVisible(True)
            else:
                self.GetBaseUIControl(self.search_panel_path).SetVisible(False)

    def on_kind_btn_touch(self, args):
        if args['TouchEvent'] == TouchEvent.TouchUp:
            notify_to_server('OnCategoryItemsEvent', {
                "blockName": self.block_name,
                "playerId": local_player,
                "state": True
            })
            text = self.GetBaseUIControl(self.page_text_path).asTextEditBox()
            self.pages = "1"
            text.SetEditText(self.pages)

    def on_order_btn_touch(self, args):
        if args['TouchEvent'] == TouchEvent.TouchUp:
            notify_to_server('OnSortItemsEvent', {
                "blockName": self.block_name,
                "playerId": local_player,
                "state": True
            })
            text = self.GetBaseUIControl(self.page_text_path).asTextEditBox()
            self.pages = "1"
            text.SetEditText(self.pages)

    def on_page_btn_touch(self, args):
        if args['TouchEvent'] == TouchEvent.TouchUp:
            if not self.GetBaseUIControl(self.page_path).GetVisible():
                notify_to_server('ToGetEnderChestSizeEvent', {
                    "blockName": self.block_name,
                    "playerId": local_player,
                    "dimensionId": self.dimension,
                    "pages": 1,
                    "block_pos": self.block_pos,
                    "state": True
                })
                add_timer(0.2, self.get_grid_list_path)
            else:
                self.GetBaseUIControl(self.page_path).SetVisible(False)

    def get_grid_list_path(self):
        if self.box_size:
            GridList = self.GetChildrenName(self.mGridPath)
            if GridList is None:
                # PC版touch模式和鼠标模式scroll的路径不一致。。。
                self.mGridPath = self.scroll_panel_path + "/scroll_mouse/scroll_view/stack_panel/background_and_viewport/scrolling_view_port/scrolling_content"
                GridList = self.GetChildrenName(self.mGridPath)
                if GridList is None:
                    return
            gridUIControl = self.GetBaseUIControl(self.mGridPath).asGrid()
            gridUIControl.SetGridDimension((1, len(self.box_size)))
            self.GetBaseUIControl(self.page_path).SetVisible(True)

            self.box_size.sort()
            add_timer(0.2, self.show_data)
        else:
            self.GetBaseUIControl(self.page_path).SetVisible(False)

    def show_data(self):
        if not self.GetChildrenName(self.mGridPath):
            return
        self.already_register_item_btn = []
        for index, item in enumerate(self.GetChildrenName(self.mGridPath)):
            self.GetBaseUIControl(self.mGridPath + "/" + item + "/button_label").asLabel().SetText(
                str(self.box_size[int(item.split("button0")[1]) - 1]))
            if item not in self.already_register_item_btn:
                self.AddTouchEventHandler(self.mGridPath + "/button0" + str(index + 1), self.to_page,
                                          {"isSwallow": True})
                self.already_register_item_btn.append(item)

    # def refresh_moying_bag_ui(self):
    #     bag_grid_list = self.validate_moying_bag_grid_path()
    #     if not bag_grid_list:
    #         return
    #     for item_btn in bag_grid_list:
    #         item_btn_path = self.moying_panle_path + "/" + item_btn
    #         if item_btn_path not in self.bag_info:
    #             continue
    #         self.set_slot_item_btn(item_btn_path, self.bag_info[item_btn_path]['item'])
    #         self.register_item_btn_event(item_btn_path)

    # def refresh_search_bag_ui(self):
    #     bag_grid_list = self.GetChildrenName(self.search_panel_grid_path)
    #     if not bag_grid_list:
    #         return
    #     for item_btn in bag_grid_list:
    #         item_btn_path = self.search_panel_grid_path + "/" + item_btn
    #         if item_btn_path not in self.bag_info:
    #             continue
    #         self.set_slot_item_btn(item_btn_path, self.bag_info[item_btn_path]['item'])
    #         self.register_item_btn_event(item_btn_path)

    # def validate_moying_bag_grid_path(self):
    #     bag_grid_list = self.GetChildrenName(self.moying_panle_path)
    #     return bag_grid_list

    # def update_custom_container_ui(self, bag_items):
    #     # 当前保存在玩家身上的数据
    #     for i, item in enumerate(bag_items):
    #         btn = 'item_btn{slot}'.format(slot=i + 1)
    #         btn_path = '{prefix}/{btn}'.format(prefix=self.moying_panle_path, btn=btn)
    #         self.bag_info[btn_path] = {"slot": btn, "item": item}
    #         self.slot_to_path[btn] = btn_path
    #         self.set_slot_item_btn(btn_path, item)
    #         self.register_item_btn_event(btn_path)

    # def update_moying_bag_ui(self, data, state):
    #     for i, item in enumerate(data):
    #         btn = 'item_btn{slot}'.format(slot=i + 1)
    #         btn_path = '{prefix}/{btn}'.format(prefix=self.moying_panle_path, btn=btn)
    #         self.bag_info[btn_path] = {"slot": btn, "item": item}
    #         self.slot_to_path[btn] = btn_path
    #     if not state:
    #         add_timer(0.7, self.refresh_moying_bag_ui)
    #     else:
    #         self.refresh_moying_bag_ui()

    # def update_search_bag_ui(self, data, args):
    #     self.search_data = copy.deepcopy(args)
    #     for i, item in enumerate(data):
    #         btn = 'item_btn{slot}'.format(slot=i + 1)
    #         btn_path = '{prefix}/{btn}'.format(prefix=self.search_panel_grid_path, btn=btn)
    #         self.bag_info[btn_path] = {"slot": btn, "item": item}
    #         self.slot_to_path[btn] = btn_path
    #     self.refresh_search_bag_ui()