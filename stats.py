"""选区统计计算（纯逻辑，无 sublime 依赖）。

每个统计函数对全部选区的文本做汇总，返回结果字符串。
"""

import inspect
from dataclasses import dataclass
from typing import Callable, List

from .calc import extract_numbers, format_number

StatFunc = Callable[[List[str]], str]

_REGISTRY: dict = {}


@dataclass(frozen=True)
class Stat:
    """一种选区统计方式。"""

    name: str
    key: str
    func: StatFunc

    def __post_init__(self):
        param_count = len(inspect.signature(self.func).parameters)
        if param_count != 1:
            raise ValueError(f"统计函数 {self.func.__name__} 必须只接受 selections 一个参数")

    def apply(self, selections: List[str]) -> str:
        return self.func(selections)


def stat(name: str, key: str):
    """装饰器：将函数注册为选区统计方式。"""

    def wrapper(func: StatFunc) -> StatFunc:
        if not name or not key:
            raise ValueError(f"统计 {func.__name__} 的 name 和 key 不能为空")
        if key in _REGISTRY:
            raise ValueError(f"统计 key 重复: {key!r}（已注册为 {_REGISTRY[key].name}）")
        _REGISTRY[key] = Stat(name=name, key=key, func=func)
        return func

    return wrapper


def get_stats() -> List[Stat]:
    """返回全部已注册的统计方式（按注册顺序）。"""
    return list(_REGISTRY.values())


def _all_numbers(selections: List[str]) -> List[float]:
    numbers = [n for s in selections for n in extract_numbers(s)]
    if not numbers:
        raise ValueError("选区内没有数字")
    return numbers


@stat("数字求和", "sum")
def sum_stat(selections):
    numbers = _all_numbers(selections)
    return format_number(sum(numbers))


@stat("数字平均", "avg")
def avg_stat(selections):
    numbers = _all_numbers(selections)
    return format_number(sum(numbers) / len(numbers))


@stat("文本连接", "join")
def join_stat(selections):
    """按顺序拼接所有选区的文本，结果可直接复制使用。"""
    return "".join(selections)
