# correlation-lite

零依赖的**相关性分析小工具**：给定两组数值（CSV 两列或内联成对数据），计算 **Pearson** 与 **Spearman** 相关系数，并自动给出中文强弱/正负解释。纯标准库，无需任何 API。

## 功能简介

- **Pearson**：衡量线性相关程度。
- **Spearman**：秩相关，对单调但非线性关系更稳健。
- 自动解释：强 / 较强 / 中等 / 弱 / 几乎无相关，正/负。
- 内置 CSV 读取，自动跳过表头与脏行。

## 快速开始

```bash
# CSV 两列
python3 cli.py --file data.csv

# 内联数据
python3 cli.py --pairs 1,2 --pairs 2,4 --pairs 3,6 --pairs 4,8
```

输出示例：

```
样本数 n = 4
Pearson  r = 1.0000  -> 正强相关
Spearman ρ = 1.0000  -> 正强相关
```

## 无 API key 如何运行

本项目**完全不需要 API key**，纯本地数学计算。

## 目录说明

```
correlation-lite/
├── correlation.py   # pearson / spearman / interpret / from_csv
├── cli.py         # 命令行入口
├── tests/
│   └── test_correlation.py
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests
```

## License

MIT License，Copyright (c) 2026 ljiang9。
