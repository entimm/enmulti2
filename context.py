"""转换上下文：透传给转换函数的附加信息。"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TransformContext:
    """当前转换执行的上下文。

    新式转换函数签名：``func(v, ctx)``
    ``v`` 为当前选区的原始文本，``ctx`` 为该选区所处的上下文。
    """

    index: int
    """当前选区在所有选区中的序号（从 0 开始）。"""

    selections: List[str]
    """本次命令触发时所有选区的原始文本快照。"""

    view: Optional[object] = None
    """触发命令的视图对象（仅 Sublime Text 环境下可用）。"""
