# 实验01：验证 Python 列表索引是否为 O(1)

## 目标
通过控制变量实验，观察 `lst[i]` 的单位访问耗时是否随着列表长度 `n` 增长而基本不变。

## 实验设计
- 仅改变列表长度 `n`（从 1,000 到 1,000,000，按 2 倍递增）
- 固定随机种子与每个 `n` 的访问次数
- 使用空循环作为基线，扣除循环本身开销
- 主要指标：头/中/尾固定位置索引（`index_hmt_ns`）
- 参考指标：随机索引（`index_random_ns`，受缓存命中影响更明显）
- 对照组：`sum(lst)` 线性扫描（预期 O(n)）

## O(1) 判定
- `log-log slope (index h/m/t)` 接近 `0`
- `max/min h/m/t ratio` 接近 `1`

## 运行
```powershell
python "D:\0_Py_Self\learn_python数据结构与算法\2算法分析\实验01.py"
```

## 输出
- 控制台表格：`n`、`hmt(ns)`、`random(ns)`、`scan(ms)`
- 判定指标：
  - `log-log slope (index h/m/t)`
  - `log-log slope (index random)`
  - `log-log slope (scan)`
  - `max/min h/m/t ratio`
- CSV 文件：`index_complexity_results.csv`

## 说明
该实验是经验验证，不是形式化数学证明。受 CPU 频率、系统负载、解释器版本、缓存层级等因素影响，建议多次运行并看趋势一致性。
