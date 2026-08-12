import ast
import base64
import hashlib
import operator

from ..registry import transformation


_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
    ast.Not: operator.not_,
    ast.Invert: operator.invert,
}

# 仅允许调用这些无副作用的安全内建函数
_SAFE_FUNCS = {
    "len": len,
    "abs": abs,
    "min": min,
    "max": max,
    "round": round,
    "ord": ord,
    "chr": chr,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "format": format,
}

_MAX_POW_EXPONENT = 1000


def _safe_eval(v):
    """安全求值：仅支持字面量、基础算术运算和少量安全内建函数，杜绝任意代码执行"""
    tree = ast.parse(v, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and isinstance(right, (int, float)):
                if abs(right) > _MAX_POW_EXPONENT:
                    raise ValueError("exponent too large")
            op_func = _BIN_OPS.get(type(node.op))
            if op_func is None:
                raise ValueError(f"operator {type(node.op).__name__} not allowed")
            return op_func(left, right)
        if isinstance(node, ast.UnaryOp):
            op_func = _UNARY_OPS.get(type(node.op))
            if op_func is None:
                raise ValueError(f"operator {type(node.op).__name__} not allowed")
            return op_func(evaluate(node.operand))
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in _SAFE_FUNCS:
                raise ValueError("function call not allowed")
            func = _SAFE_FUNCS[node.func.id]
            args = [evaluate(arg) for arg in node.args]
            kwargs = {kw.arg: evaluate(kw.value) for kw in node.keywords}
            return func(*args, **kwargs)
        if isinstance(node, ast.Name):
            if node.id in _SAFE_FUNCS:
                return _SAFE_FUNCS[node.id]
            raise ValueError(f"name {node.id!r} not allowed")
        raise ValueError(f"expression not allowed: {type(node).__name__}")

    return evaluate(tree)


@transformation("MD5", "md5")
def md5_transform(v, ctx):
    """计算字符串 v 的 MD5 哈希值"""
    return hashlib.md5(v.encode()).hexdigest()


@transformation("Reverse", "reverse")
def reverse_transform(v, ctx):
    """翻转字符串 v"""
    return v[::-1]


@transformation("Base64 Encode", "base64_encode")
def base64_encode_transform(v, ctx):
    """对字符串 v 进行 Base64 编码"""
    return base64.b64encode(v.encode()).decode()


@transformation("Base64 Decode", "base64_decode")
def base64_decode_transform(v, ctx):
    """对字符串 v 进行 Base64 解码"""
    return base64.b64decode(v.encode()).decode()


@transformation("Eval", "eval")
def eval_transform(v, ctx):
    """对字符串 v 执行安全求值（仅字面量和基础运算，无法执行任意代码）"""
    try:
        return str(_safe_eval(v))
    except Exception as e:
        return f"Error: {str(e)}"


@transformation("Unicode -> UTF-8", "unicode_to_utf8")
def unicode_to_utf8_transform(v, ctx):
    """将 Unicode 转义编码的字符串 v 转换成普通字符串"""
    if "\\" not in v:
        return v
    try:
        return v.encode('utf-8').decode('unicode_escape')
    except Exception as e:
        return f"Error occurred: {str(e)}"


@transformation("UTF-8 -> Unicode", "utf8_to_unicode")
def utf8_to_unicode_transform(v, ctx):
    """将 UTF-8 字符串 v 转换成 Unicode 转义编码的字符串"""
    try:
        return v.encode('unicode_escape').decode('utf-8')
    except Exception as e:
        return f"Error occurred: {str(e)}"
