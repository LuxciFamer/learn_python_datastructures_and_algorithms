import csv
import gc
import math
import random
import statistics
import time
from pathlib import Path


SEED = 20260317
OPS_PER_N = 200_000
REPEATS = 5
SIZES = [1_000 * (2 ** i) for i in range(0, 11)]  # 1,000 -> 1,024,000
CSV_PATH = Path(__file__).with_name("dict_complexity_results.csv")


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


def measure_get_per_op_ns(dct, keys):
    def with_get():
        sink = 0
        for k in keys:
            sink += dct[k]
        return sink

    t_get = median_timing_ns(with_get)
    return t_get / len(keys)


def measure_set_per_op_ns(dct, keys):
    def with_set():
        for k in keys:
            dct[k] = 1

    t_set = median_timing_ns(with_set)
    return t_set / len(keys)


def measure_scan_ms(dct):
    def scan():
        return sum(dct.values())

    return median_timing_ns(scan) / 1_000_000


def log_log_slope(xs, ys):
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mean_x = statistics.fmean(lx)
    mean_y = statistics.fmean(ly)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(lx, ly))
    den = sum((x - mean_x) ** 2 for x in lx)
    return num / den if den else float("nan")


def run_experiment():
    random.seed(SEED)
    rows = []

    for n in SIZES:
        dct = {i: i for i in range(n)}
        keys = [random.randrange(n) for _ in range(OPS_PER_N)]

        get_ns = measure_get_per_op_ns(dct, keys)
        set_ns = measure_set_per_op_ns(dct, keys)
        scan_ms = measure_scan_ms(dct)

        rows.append(
            {
                "n": n,
                "get_ns": get_ns,
                "set_ns": set_ns,
                "scan_ms": scan_ms,
            }
        )

    return rows


def print_report(rows):
    print("n\tget(ns/op)\tset(ns/op)\tscan(ms)")
    for r in rows:
        print(f"{r['n']}\t{r['get_ns']:.2f}\t\t{r['set_ns']:.2f}\t\t{r['scan_ms']:.3f}")

    ns = [r["n"] for r in rows]
    get_series = [r["get_ns"] for r in rows]
    set_series = [r["set_ns"] for r in rows]
    scan_series = [r["scan_ms"] for r in rows]

    print("\n判定指标:")
    print(f"log-log slope (get):  {log_log_slope(ns, get_series):.4f}")
    print(f"log-log slope (set):  {log_log_slope(ns, set_series):.4f}")
    print(f"log-log slope (scan): {log_log_slope(ns, scan_series):.4f}")
    print(f"max/min ratio (get):  {max(get_series) / min(get_series):.3f}")
    print(f"max/min ratio (set):  {max(set_series) / min(set_series):.3f}")


def write_csv(rows):
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "get_ns", "set_ns", "scan_ms"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    result_rows = run_experiment()
    print_report(result_rows)
    write_csv(result_rows)
    print(f"\nCSV 已写入: {CSV_PATH}")


