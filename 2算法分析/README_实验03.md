# 实验03：比较列表与字典的 `del` 操作性能

## 目标
在控制变量条件下，比较不同容器的删除操作耗时，并观察其随规模 `n` 增长的趋势：
- 列表：`del lst[0]`、`del lst[len(lst)//2]`、`del lst[-1]`
- 字典：`del d[k]`

## 实验设计
- 仅改变容器规模 `n`（`2,000 -> 128,000`，按 2 倍递增）
- 每个 `n` 的删除次数按比例设置：`ops = min(max(int(n*0.05), 200), 3000)`
- 固定随机种子 `SEED=20260317`，字典删除键使用预生成采样
- 每个场景重复测量多次取中位数（`REPEATS=7`）
- 测量期间关闭 GC，降低抖动

## 输出指标
- `ns_per_op`：单次删除平均耗时（ns/op）
- `total_ms`：该场景总耗时（ms）
- `log-log slope`：`n` 与 `ns/op` 在双对数坐标下的斜率
- `max/min`：同一场景跨规模波动比值

判定参考：
- 若 `slope` 接近 `0` 且 `max/min` 不大，通常可视为“近似 O(1)”
- 若 `slope` 明显大于 `0`，通常表示随规模增长而变慢（更接近 O(n)）

## 运行
```powershell
python "D:\0_Py_Self\learn_python数据结构与算法\2算法分析\实验3.py"
```

## 输出文件
- 控制台：每个 `n` 与场景的 `ops`、`ns/op`、`total(ms)`
- CSV：`del_complexity_results.csv`

## 结果解读建议
- 重点对比 `list_head/list_middle` 与 `dict_delete` 的斜率差异
- `list_tail` 常接近常数级，常作为列表删除的对照场景
- 若结果抖动明显，可提高 `REPEATS` 或在空闲环境重复运行

