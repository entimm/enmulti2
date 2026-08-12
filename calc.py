"""数字提取与格式化（纯逻辑，无 sublime 依赖）。"""

import re
from typing import List

_NUMBER_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?")


def extract_numbers(text: str) -> List[float]:
    """从文本中提取数字，支持负数、小数与千分位逗号。"""
    return [float(m.replace(",", "")) for m in _NUMBER_RE.findall(text)]


def format_number(value: float) -> str:
    """整数省略小数位，其余保留原始精度。"""
    if value == int(value):
        return str(int(value))
    return repr(value)
