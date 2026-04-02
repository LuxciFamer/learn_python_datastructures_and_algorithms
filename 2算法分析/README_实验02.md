# 实验02：验证 Python 字典取值与赋值是否近似 O(1)

## 目标
通过控制变量实验，观察 `d[k]`（取值）与 `d[k] = v`（赋值）的单位耗时是否随着字典规模 `n` 增长而基本不变。

## 实验设计
- 仅改变字典长度 `n`（1,000 到 1,024,000，按 2 倍递增）
- 固定每个 `n` 的操作次数 `OPS_PER_N = 200000`
- 固定随机种子，预生成访问键序列
- 使用基线循环扣除 Python 循环与迭代开销
- `set` 场景采用“覆盖已有键”，避免把扩容影响混入核心结论
- 对照组使用 `sum(d.values())` 线性扫描（预期 O(n)）

## 指标与判定
- 主要指标：
  - `get_ns`：取值平均耗时（ns/op）
  - `set_ns`：赋值平均耗时（ns/op）
- 对照指标：
  - `scan_ms`：线性扫描耗时（ms）
- 判定参考：
  - `log-log slope(get)` 和 `log-log slope(set)` 接近 `0`
  - `max/min ratio(get)` 和 `max/min ratio(set)` 接近 `1`
  - `log-log slope(scan)` 接近 `1`

## 运行
```powershell
python "D:\0_Py_Self\learn_python数据结构与算法\2算法分析\实验02.py"
```

## 输出
- 控制台表格：`n`、`get(ns/op)`、`set(ns/op)`、`scan(ms)`
- 判定指标：log-log 斜率与 max/min 比值
- CSV 文件：`dict_complexity_results.csv`

## 说明
该实验是经验验证，不是形式化数学证明。运行结果会受 CPU 频率、系统负载、解释器版本、缓存层级、哈希扰动等因素影响，建议多次运行并观察趋势一致性。

