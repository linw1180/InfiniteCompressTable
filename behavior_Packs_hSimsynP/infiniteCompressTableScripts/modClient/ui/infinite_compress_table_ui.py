# -*- coding: utf-8 -*-

from infiniteCompressTableScripts.modClient.ui._base_custom_container_ui import BaseCustomContainerUIScreen


class InfiniteCompressTableUIScreen(BaseCustomContainerUIScreen):

    def __init__(self, namespace, name, param):
        super(InfiniteCompressTableUIScreen, self).__init__(namespace, name, param)
        self.inv_grid_path = '/main_panel/inv_grid'  # 套用
        self.item_btn_path_prefix = self.inv_grid_path + "/item_btn"

    def on_ui_create(self):
        super(InfiniteCompressTableUIScreen, self).on_ui_create()

    def show_ui(self, **kwargs):
        super(InfiniteCompressTableUIScreen, self).show_ui(**kwargs)

    def tick(self):
        super(InfiniteCompressTableUIScreen, self).tick()

    def close(self, args):
        super(InfiniteCompressTableUIScreen, self).close(args)

    def update_bag_ui(self, args):
        # 更新背包UI
        for i in xrange(36):
            # 按钮绝对路径 '/main_panel/inv_grid/item_btn31'
            item_btn_path = self.item_btn_path_prefix + str(i + 1)
            # 物品信息字典，槽位无物品则为 None
            item_dict = args[i]
            self.bag_info[item_btn_path] = {"slot": i, "item": item_dict}
            self.slot_to_path[i] = item_btn_path

        self.refresh_bag_ui()

        # 初始化自定义按钮数据
        self.update_custom_container_ui()

    def update_custom_container_ui(self):
        # 初始化两个自定义按钮数据
        from_item_btn_path = self.from_item_button_path
        self.bag_info[from_item_btn_path] = {"slot": 'input_slot', "item": None}
        self.slot_to_path['input_slot'] = from_item_btn_path

        to_item_btn_path = self.to_item_button_path
        self.bag_info[to_item_btn_path] = {"slot": 'output_slot', "item": None}
        self.slot_to_path['output_slot'] = to_item_btn_path

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

    # 先执行
    def handle_swap(self, button_path):
        super(InfiniteCompressTableUIScreen, self).handle_swap(button_path)

    # 后执行
    def swap_item(self, args):
        return super(InfiniteCompressTableUIScreen, self).swap_item(args)
