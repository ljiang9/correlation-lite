"""correlation-lite 命令行入口。

用法示例：
    python3 cli.py --file data.csv
    python3 cli.py --pairs 1,2 --pairs 2,4 --pairs 3,5
"""

from __future__ import annotations

import argparse
import sys

from correlation import from_csv, interpret, pearson, spearman


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="correlation-lite",
        description="计算两组数据的 Pearson / Spearman 相关系数",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="CSV 文件（至少两列数值）")
    src.add_argument("--pairs", action="append", help="内联一对 x,y，可重复")
    p.add_argument("--col-x", type=int, default=0)
    p.add_argument("--col-y", type=int, default=1)
    p.add_argument("--no-header", action="store_true", help="CSV 无表头")
    p.add_argument("--method", default="both",
                   choices=["pearson", "spearman", "both"])
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            xs, ys = from_csv(f.read(), args.col_x, args.col_y,
                              has_header=not args.no_header)
    else:
        xs, ys = [], []
        for pair in args.pairs:
            a, b = pair.split(",")
            xs.append(float(a))
            ys.append(float(b))

    print(f"样本数 n = {len(xs)}")
    if args.method in ("pearson", "both"):
        r = pearson(xs, ys)
        print(f"Pearson  r = {r:.4f}  -> {interpret(r)}")
    if args.method in ("spearman", "both"):
        rho = spearman(xs, ys)
        print(f"Spearman ρ = {rho:.4f}  -> {interpret(rho)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
