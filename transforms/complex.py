import random
import string
import time
from datetime import datetime

from ..registry import transformation


@transformation("Time<->Timestamp", "time_timestamp")
def time_timestamp_transform(v, ctx):
    """
    实现时间字符串和时间戳之间的互转
    如果 v 是一个合法的时间字符串，将其转换成对应的时间戳字符串
    如果 v 是一个合法的时间戳字符串，将其转换成对应的时间字符串
    如果 v 是空字符串，返回当前时间的字符串，格式为 %Y-%m-%d %H:%M:%S
    否则返回空字符串
    """

    if not v:
        # 如果 v 是空字符串，返回当前时间的字符串
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 尝试将 v 解析为时间字符串
        if "." in v:
            dt = datetime.strptime(v, "%Y-%m-%d %H:%M:%S.%f")
        else:
            dt = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        return str(int(time.mktime(dt.timetuple())))
    except (ValueError, OverflowError, OSError):
        pass

    try:
        # 尝试将 v 解析为时间戳字符串
        timestamp = int(v)
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OverflowError, OSError):
        return ""


@transformation("ReplaceChars", "replace_chars")
def replace_chars_transform(v, ctx):
    # 对给定字符集生成一对一的随机映射，保证不映射到自身且无碰撞
    def shuffled_mapping(target):
        pool = list(target)
        random.shuffle(pool)
        return {src: dst for src, dst in zip(target, pool) if src != dst}

    # 生成小写/大写字母和数字的替换规则（保持大小写类别不变）
    replace_dict = {}
    replace_dict.update(shuffled_mapping(string.ascii_lowercase))
    replace_dict.update(shuffled_mapping(string.ascii_uppercase))
    replace_dict.update(shuffled_mapping(string.digits))
    # 调用translate()方法替换字符串中的字符
    return v.translate(str.maketrans(replace_dict))
