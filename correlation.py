"""correlation-lite：计算两组数据的 Pearson / Spearman 相关系数并给出解释。

纯标准库实现：
- Pearson：线性相关系数；
- Spearman：对排名后再算 Pearson；
- 自动给出强弱、正负的中文解释。
CSV 输入：两列数值。
"""

from __future__ import annotations

import math


def _validate(x: list[float], y: list[float]) -> None:
    if len(x) != len(y):
        raise ValueError("两组数据长度必须一致")
    if len(x) < 2:
        raise ValueError("至少需要 2 个数据点")


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def pearson(x: list[float], y: list[float]) -> float:
    """Pearson 相关系数。"""
    x = [float(v) for v in x]
    y = [float(v) for v in y]
    _validate(x, y)
    mx, my = mean(x), mean(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    dx = math.sqrt(sum((a - mx) ** 2 for a in x))
    dy = math.sqrt(sum((b - my) ** 2 for b in y))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def _rank(values: list[float]) -> list[float]:
    """按升序排名，同分取平均排名。"""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0  # 1-based 平均排名
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(x: list[float], y: list[float]) -> float:
    """Spearman 秩相关系数。"""
    x = [float(v) for v in x]
    y = [float(v) for v in y]
    _validate(x, y)
    return pearson(_rank(x), _rank(y))


def interpret(r: float) -> str:
    """把相关系数解释成中文描述。"""
    sign = "正" if r > 0 else "负" if r < 0 else ""
    r = abs(r)
    if r < 0.1:
        strength = "几乎无相关"
    elif r < 0.3:
        strength = "弱相关"
    elif r < 0.5:
        strength = "中等相关"
    elif r < 0.7:
        strength = "较强相关"
    else:
        strength = "强相关"
    if not sign:
        return strength
    return f"{sign}{strength}"


def from_csv(text: str, col_x: int = 0, col_y: int = 1,
             has_header: bool = True) -> tuple[list[float], list[float]]:
    """从 CSV 文本读取两列数值。"""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if has_header:
        lines = lines[1:]
    xs: list[float] = []
    ys: list[float] = []
    for ln in lines:
        parts = ln.replace(" ", "").split(",")
        if len(parts) <= max(col_x, col_y):
            continue
        try:
            xs.append(float(parts[col_x]))
            ys.append(float(parts[col_y]))
        except ValueError:
            continue
    return xs, ys
