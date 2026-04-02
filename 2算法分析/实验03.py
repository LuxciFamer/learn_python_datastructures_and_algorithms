import csv
import gc
import math
import random
import statistics
import time
from pathlib import Path


SEED = 20260317
REPEATS = 7
DELETE_RATIO = 0.05
MIN_OPS = 200
MAX_OPS = 3_000
SIZES = [2_000 * (2**i) for i in range(0, 7)]  # 2,000 -> 128,000
CSV_PATH = Path(__file__).with_name("del_complexity_results.csv")


def ops_for_n(n):
	return max(MIN_OPS, min(MAX_OPS, int(n * DELETE_RATIO)))


def median_timing_ns(func, repeats=REPEATS):
	samples = []
	old_gc = gc.isenabled()
	gc.disable()
	try:
		for _ in range(repeats):
			start = time.perf_counter_ns()
			func()
			end = time.perf_counter_ns()
			samples.append(end - start)
	finally:
		if old_gc:
			gc.enable()
	return statistics.median(samples)


def measure_list_head_ns(n, ops):
	def run():
		lst = list(range(n))
		for _ in range(ops):
			del lst[0]

	return median_timing_ns(run)


def measure_list_middle_ns(n, ops):
	def run():
		lst = list(range(n))
		for _ in range(ops):
			del lst[len(lst) // 2]

	return median_timing_ns(run)


def measure_list_tail_ns(n, ops):
	def run():
		lst = list(range(n))
		for _ in range(ops):
			del lst[-1]

	return median_timing_ns(run)


def measure_dict_delete_ns(n, keys_to_delete):
	def run():
		dct = {i: i for i in range(n)}
		for k in keys_to_delete:
			del dct[k]

	return median_timing_ns(run)


def log_log_slope(xs, ys):
	lx = [math.log(x) for x in xs]
	ly = [math.log(y) for y in ys]
	mean_x = statistics.fmean(lx)
	mean_y = statistics.fmean(ly)
	num = sum((x - mean_x) * (y - mean_y) for x, y in zip(lx, ly))
	den = sum((x - mean_x) ** 2 for x in lx)
	return num / den if den else float("nan")


def run_experiment():
	rows = []
	rng = random.Random(SEED)

	for n in SIZES:
		ops = ops_for_n(n)
		keys_to_delete = rng.sample(range(n), ops)

		raw_ns = {
			"list_head": measure_list_head_ns(n, ops),
			"list_middle": measure_list_middle_ns(n, ops),
			"list_tail": measure_list_tail_ns(n, ops),
			"dict_delete": measure_dict_delete_ns(n, keys_to_delete),
		}

		for scenario, total_ns in raw_ns.items():
			rows.append(
				{
					"n": n,
					"scenario": scenario,
					"ops": ops,
					"total_ms": total_ns / 1_000_000,
					"ns_per_op": total_ns / ops,
				}
			)

	return rows


def print_report(rows):
	print("n\tscenario\tops\tns/op\ttotal(ms)")
	for row in rows:
		print(
			f"{row['n']}\t{row['scenario']}\t{row['ops']}\t"
			f"{row['ns_per_op']:.2f}\t{row['total_ms']:.3f}"
		)

	print("\n判定指标:")
	scenarios = sorted({r["scenario"] for r in rows})
	for scenario in scenarios:
		x = [r["n"] for r in rows if r["scenario"] == scenario]
		y = [r["ns_per_op"] for r in rows if r["scenario"] == scenario]
		ratio = max(y) / min(y)
		slope = log_log_slope(x, y)
		print(f"- {scenario:12s} slope={slope:7.4f}  max/min={ratio:6.3f}")


def write_csv(rows):
	with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(
			f, fieldnames=["n", "scenario", "ops", "total_ms", "ns_per_op"]
		)
		writer.writeheader()
		writer.writerows(rows)


if __name__ == "__main__":
	result_rows = run_experiment()
	print_report(result_rows)
	write_csv(result_rows)
	print(f"\nCSV 已写入: {CSV_PATH}")

