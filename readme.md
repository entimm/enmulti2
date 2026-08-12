# enmulti2 多点文本转换

对 Sublime Text 的多选区文本批量执行转换（每个选区独立转换）。

## 使用

- 命令面板 → `Enmulti: 文本转换...`，或快捷键 `super+shift+t`（macOS）
- 在弹出的面板中选择转换类型，所有选区同时被转换
- 转换失败不中断其他选区，错误汇总显示在输出面板
- 命令面板 → `Enmulti: 计算选区...`，或快捷键 `super+shift+c`：先选择统计方式，再对所有选区汇总。支持数字求和、数字平均、文本连接（结果直接复制到剪贴板）；输出面板 + 剪贴板，不修改文档

## 内置转换

| 名称 | key | 说明 |
|---|---|---|
| MD5 | `md5` | MD5 哈希 |
| Reverse | `reverse` | 反转字符串 |
| Base64 Encode / Decode | `base64_encode` / `base64_decode` | Base64 编解码 |
| Eval | `eval` | 安全求值：仅字面量与算术运算，白名单内建函数，无法执行任意代码 |
| Unicode -> UTF-8 | `unicode_to_utf8` | Unicode 转义编码还原为普通字符串 |
| UTF-8 -> Unicode | `utf8_to_unicode` | 普通字符串转成 Unicode 转义编码 |
| Time<->Timestamp | `time_timestamp` | 时间字符串与时间戳互转；空字符串返回当前时间 |
| ReplaceChars | `replace_chars` | 随机字符替换（一对一映射，无碰撞、不映射自身，且保持大小写/数字类别不变） |

## 新增转换

在 `transforms/` 下新建模块（或加进现有模块），用 `@transformation` 装饰即可，无需任何注册代码：

```python
from ..registry import transformation

@transformation("Uppercase", "upper")
def upper_transform(v, ctx):
    """v 为选区原文，ctx 提供 index / selections / view"""
    return v.upper()
```

新式函数签名为 `func(v, ctx)`，旧式 `func(v, i, secs)` 依然兼容（按参数个数自动识别）。

## 新增统计

统计函数对全部选区的文本做汇总，返回一个字符串。在任意模块中用 `@stat` 装饰即可：

```python
from ..stats import stat

@stat("文本连接", "join")
def join_stat(selections):
    """按顺序拼接所有选区的文本"""
    return "".join(selections)
```

函数签名固定为 `func(selections)`，selections 是全部选区的原始文本列表。

## 配置

`Enmulti.sublime-settings` 的 `enabled_transforms` 可限制面板中出现的转换 key 列表，空数组表示全部启用。

## 结构

| 模块 | 职责 |
|---|---|
| `enmulti.py` | 命令层（快速面板、执行、输出面板），依赖 sublime |
| `registry.py` | 转换注册与 transforms 包自动发现 |
| `transforms/` | 内置转换实现（`simple.py` 简单转换、`complex.py` 复杂转换） |
| `stats.py` | 统计方式注册与内置统计 |
| `calc.py` | 数字提取与格式化（纯逻辑） |
| `context.py` | 转换上下文 `TransformContext`（index / selections / view） |

除 `enmulti.py` 外，其余模块不依赖 sublime，可在纯 Python 环境下运行与测试。注册表为空时，命令会在控制台打印自动发现的诊断日志（含 sys.path、包导入尝试），可用于排查插件加载问题。

## 测试

```bash
python3 -m unittest discover -s tests
```

转换逻辑（`registry.py` / `transforms/` / `stats.py` / `calc.py` / `context.py`）不依赖 sublime 模块。
