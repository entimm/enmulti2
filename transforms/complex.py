import random
import string
import time
from datetime import datetime

from . import transformation


@transformation("Time<->Timestamp", "time_timestamp")
def time_timestamp_transform(v, i, secs):
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
    except ValueError:
        pass

    try:
        # 尝试将 v 解析为时间戳字符串
        timestamp = int(v)
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return ""


@transformation("ReplaceChars", "replace_chars")
def replace_chars_transform(v, i, secs):
    # 获取所有大小写字母和数字的字符串
    chars = string.ascii_lowercase + string.ascii_uppercase
    # 生成替换规则，用字典来存储
    replace_dict = {}
    for char in chars:
        if char.islower():
            replace_char = random.choice(string.ascii_lowercase.replace(char, ''))
        else:
            replace_char = random.choice(string.ascii_uppercase.replace(char, ''))
        replace_dict[char] = replace_char
    # 生成数字替换规则，加入到替换规则字典中
    replace_dict.update({str(i): str(random.randint(1, 9)) for i in range(10)})
    # 调用translate()方法替换字符串中的字符
    return v.translate(str.maketrans(replace_dict))
