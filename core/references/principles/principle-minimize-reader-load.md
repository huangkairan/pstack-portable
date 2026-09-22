# 同时减少层次和隐藏状态

适用：审查代码时统计追踪层数与读者需记住的可变状态，合并无压缩价值的转发层，缩小状态作用域。

审查代码时统计追踪层数与读者需记住的可变状态，合并无压缩价值的转发层，缩小状态作用域。

边界：平铺文件也可能隐藏大量全局状态；它并非一味反对深模块。关联 guard-the-context-window。

[上游原文](https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/pstack/skills/principle-minimize-reader-load/SKILL.md#L7-L23)
