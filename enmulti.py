"""enmulti2 命令层：文本转换的选择与执行。

旧命令名 ``nice_transform_select2`` / ``nice_transform2`` 已废弃。
"""

import traceback

import sublime
import sublime_plugin

from .registry import get_discovery_log, get_transforms

SETTINGS_FILE = "Enmulti.sublime-settings"


class EnmultiSelectCommand(sublime_plugin.ApplicationCommand):
    """弹出快速面板，选择要执行的转换。"""

    def run(self):
        try:
            transforms = self._enabled_transforms()
        except Exception as e:
            print(f"Enmulti: 初始化失败: {e}")
            traceback.print_exc()
            sublime.status_message(f"Enmulti: 初始化失败: {e}")
            return
        if not transforms:
            print("Enmulti: 注册表为空，自动发现日志:")
            for line in get_discovery_log():
                print(f"  {line}")
            sublime.status_message("Enmulti: 没有可用的转换")
            return
        window = sublime.active_window()
        window.show_quick_panel(
            [t.name for t in transforms],
            lambda index: self._on_selected(window, transforms, index),
            flags=sublime.KEEP_OPEN_ON_FOCUS_LOST,
        )

    def _on_selected(self, window, transforms, index):
        if index >= 0:
            window.run_command("enmulti_apply", {"transform_key": transforms[index].key})

    def _enabled_transforms(self):
        enabled = sublime.load_settings(SETTINGS_FILE).get("enabled_transforms", [])
        if enabled:
            return [t for t in get_transforms() if t.key in enabled]
        return list(get_transforms())


class EnmultiApplyCommand(sublime_plugin.TextCommand):
    """对当前视图的所有选区执行指定转换。"""

    def run(self, edit, transform_key=""):
        transform = next(
            (t for t in get_transforms() if t.key == transform_key), None
        )
        if transform is None:
            sublime.status_message(f"Enmulti: 未知转换 {transform_key}")
            return
        regions = [r for r in self.view.sel()]
        if not regions:
            sublime.status_message("Enmulti: 没有选中文本")
            return
        print(f"Enmulti: 选区数量 = {len(regions)}, regions = {regions}")
        selections = [self.view.substr(r) for r in regions]
        failures = []
        # 从后往前替换：前面的替换会改变文档长度，使后续 region 的旧坐标失效
        for index in range(len(regions) - 1, -1, -1):
            region = regions[index]
            try:
                result = transform.apply(
                    self.view.substr(region), index, selections, self.view
                )
                self.view.replace(edit, region, result)
            except Exception as e:
                failures.append(f"[选区 {index + 1}] {e}")
        if failures:
            self._show_errors(transform, failures)

    def _show_errors(self, transform, failures):
        window = self.view.window()
        panel = window.create_output_panel("enmulti_errors")
        panel.run_command(
            "append",
            {
                "characters": (
                    f"Enmulti: {transform.name} 转换失败 {len(failures)} 处\n"
                    + "\n".join(failures)
                    + "\n"
                )
            },
        )
        window.run_command("show_panel", {"panel": "output.enmulti_errors"})
