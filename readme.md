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
| Unicode <-> UTF-8 | `unicode_to_utf8` / `utf8_to_unicode` | 转义编码互转 |
| Time<->Timestamp | `time_timestamp` | 时间字符串与时间戳互转 |
| ReplaceChars | `replace_chars` | 随机字符替换（一对一映射，无碰撞、不映射自身） |

## 新增转换

在 `transforms/` 下新建模块（或加进现有模块），用 `@transformation` 装饰即可，无需任何注册代码：

```python
from enmulti2.registry import transformation

@transformation("Uppercase", "upper")
def upper_transform(v, ctx):
    """v 为选区原文，ctx 提供 index / selections / view"""
    return v.upper()
```

新式函数签名为 `func(v, ctx)`，旧式 `func(v, i, secs)` 依然兼容。

## 配置

`Enmulti.sublime-settings` 的 `enabled_transforms` 可限制面板中出现的转换 key 列表，空数组表示全部启用。

## 测试

```bash
python3 -m unittest discover -s tests
```

转换逻辑（`registry.py` / `transforms/` / `context.py`）不依赖 sublime 模块，可在纯 Python 环境下运行。
