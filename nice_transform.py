import sublime
import sublime_plugin

from .transforms import *

class NiceTransformSelect2Command(sublime_plugin.ApplicationCommand):
    def run(self):
        # 提取菜单项名称
        options = [name for name, _, _ in MY_TRANSFORMATIONS]
        def on_done(index):
            if index >= 0:
                # 提取转换类型，并执行转换命令
                transform_type = MY_TRANSFORMATIONS[index][1]
                sublime.active_window().run_command(
                    "nice_transform2", {"transform_type": transform_type}
                )
        # 在快速选择面板中显示所有转换选项
        sublime.active_window().show_quick_panel(options, on_done)

class NiceTransform2Command(sublime_plugin.TextCommand):
    def run(self, edit, transform_type=""):
        selected_texts = [self.view.substr(region) for region in self.view.sel()]
        for i, region in enumerate(self.view.sel()):
            text = self.view.substr(region)
            try:
                # 查找对应的转换函数并执行
                transformed_text = next(
                    func(text, i, selected_texts) for _, t, func in MY_TRANSFORMATIONS if t == transform_type
                )
                # 替换选中文本
                self.view.replace(edit, region, transformed_text)
            except StopIteration:
                pass
