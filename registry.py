"""转换注册表：管理所有文本转换的注册与自动发现。

本模块不依赖 sublime 模块，可脱离 Sublime Text 直接运行与测试。
"""

import importlib
import inspect
import os
import pkgutil
import sys
import traceback
from dataclasses import dataclass, field
from typing import Callable, List

from .context import TransformContext

TransformFunc = Callable[..., str]

_REGISTRY: dict = {}
_DISCOVERY_LOG: List[str] = []


def _log(message: str) -> None:
    _DISCOVERY_LOG.append(str(message))


def get_discovery_log() -> List[str]:
    """返回自动发现的诊断日志（用于排查插件加载问题）。"""
    return list(_DISCOVERY_LOG)


@dataclass(frozen=True)
class Transform:
    """一个文本转换的定义。"""

    name: str
    key: str
    func: TransformFunc
    legacy: bool = field(init=False)

    def __post_init__(self):
        param_count = len(inspect.signature(self.func).parameters)
        if param_count == 2:
            # 新式签名 func(v, ctx)
            legacy = False
        elif param_count == 3:
            # 旧式签名 func(v, i, secs)，兼容保留
            legacy = True
        else:
            raise ValueError(f"转换函数 {self.func.__name__} 的参数个数必须是 2 或 3")
        object.__setattr__(self, "legacy", legacy)

    def apply(self, value: str, index: int, selections: List[str], view=None) -> str:
        """执行转换，返回转换后的文本。"""
        if self.legacy:
            return self.func(value, index, selections)
        ctx = TransformContext(index=index, selections=selections, view=view)
        return self.func(value, ctx)


def transformation(name: str, key: str):
    """装饰器：将函数注册为文本转换。

    :param name: 快速面板中显示的转换名称
    :param key: 转换的唯一标识，用于命令传参
    """

    def wrapper(func: TransformFunc) -> TransformFunc:
        if not name or not key:
            raise ValueError(f"转换 {func.__name__} 的 name 和 key 不能为空")
        if key in _REGISTRY:
            raise ValueError(f"转换 key 重复: {key!r}（已注册为 {_REGISTRY[key].name}）")
        _REGISTRY[key] = Transform(name=name, key=key, func=func)
        return func

    return wrapper


def get_transforms() -> List[Transform]:
    """返回全部已注册的转换（按注册顺序），首次调用时自动发现转换模块。"""
    _ensure_discovered()
    return list(_REGISTRY.values())


_IMPLEMENTS = False


def _ensure_discovered():
    """自动导入 transforms 包下的所有模块，触发其中的注册。"""
    global _IMPLEMENTS
    if _IMPLEMENTS:
        return
    _IMPLEMENTS = True

    _log(f"__package__ = {__package__!r}, __name__ = {__name__!r}")
    _log(f"cwd = {os.getcwd()!r}")
    _log(f"sys.path = {list(sys.path)!r}")
    _log(f"sys.modules 中相关键: {sorted(m for m in sys.modules if m == 'enmulti2' or m.startswith('enmulti2.'))}")

    pkg_names = [f"{__package__}.transforms"] if __package__ else []
    pkg_names.append("transforms")
    last_error = None
    for pkg_name in pkg_names:
        _log(f"尝试导入包: {pkg_name}")
        try:
            pkg = importlib.import_module(pkg_name)
        except Exception as e:
            last_error = e
            _log(f"  导入失败: {type(e).__name__}: {e}")
            continue
        _log(f"  导入成功: {pkg!r}")
        _log(f"  __name__ = {pkg.__name__!r}, __path__ = {getattr(pkg, '__path__', None)!r}")
        try:
            modules = [
                f"{pkg.__name__}.{info.name}"
                for info in pkgutil.iter_modules(getattr(pkg, "__path__", []))
            ]
        except Exception as e:
            _log(f"  遍历模块失败: {type(e).__name__}: {e}")
            modules = []
        _log(f"  发现子模块: {modules}")
        for module_name in modules:
            try:
                importlib.import_module(module_name)
                _log(f"  已导入 {module_name}")
            except Exception as e:
                _log(f"  导入 {module_name} 失败: {type(e).__name__}: {e}")
                _log("".join(traceback.format_exception(type(e), e, e.__traceback__)).rstrip())
        _log(f"  当前注册数量: {len(_REGISTRY)}")
        return
    raise ImportError(f"找不到 transforms 包（已尝试: {pkg_names}；最后错误: {last_error}）")