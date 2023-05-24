import base64
import hashlib

from . import transformation


@transformation("MD5", "md5")
def md5_transform(v, i, secs):
    """计算字符串 v 的 MD5 哈希值"""
    return hashlib.md5(v.encode()).hexdigest()


@transformation("Reverse", "reverse")
def reverse_transform(v, i, secs):
    """翻转字符串 v"""
    return v[::-1]


@transformation("Base64 Encode", "base64_encode")
def base64_encode_transform(v, i, secs):
    """对字符串 v 进行 Base64 编码"""
    return base64.b64encode(v.encode()).decode()


@transformation("Base64 Decode", "base64_decode")
def base64_decode_transform(v, i, secs):
    """对字符串 v 进行 Base64 解码"""
    return base64.b64decode(v.encode()).decode()


@transformation("Eval", "eval")
def eval_transform(v, i, secs):
    """对字符串 v 执行 eval 操作"""
    try:
        return str(eval(v))
    except Exception as e:
        return f"Error: {str(e)}"


@transformation("Unicode -> UTF-8", "unicode_to_utf8")
def unicode_to_utf8_transform(v, i, secs):
    """将 Unicode 编码的字符串 v 转换成 UTF-8 编码的字符串"""
    try:
        return v.encode('utf-8').decode('unicode_escape')
    except Exception as e:
        return f"Error occurred: {str(e)}"


@transformation("UTF-8 -> Unicode", "utf8_to_unicode")
def utf8_to_unicode_transform(v, i, secs):
    """将 UTF-8 编码的字符串 v 转换成 Unicode 编码的字符串"""
    try:
        return v.encode('unicode_escape').decode('utf-8')
    except Exception as e:
        return f"Error occurred: {str(e)}"
