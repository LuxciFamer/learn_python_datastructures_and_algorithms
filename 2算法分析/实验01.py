import csv
import gc
import math
import random
import statistics
import timeit
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Point:
    n: int
    index_hmt_ns: float
    index_random_ns: float
    scan_ms: float


def geometric_sizes(start=1_000, stop=1_000_000, factor=2):
    sizes = []
    n = start
    while n <= stop:
        sizes.append(n)
        n *= factor
    if sizes[-1] != stop:
        sizes.append(stop)
    return sorted(set(sizes))


def linear_regression_slope_loglog(xs, ys):
    log_x = [math.log(x) for x in xs]
    log_y = [math.log(y) for y in ys]
    mx = statistics.mean(log_x)
    my = statistics.mean(log_y)

    numerator = sum((x - mx) * (y - my) for x, y in zip(log_x, log_y))
    denominator = sum((x - mx) ** 2 for x in log_x)
    return numerator / denominator if denominator else float("nan")


def _loop_overhead(indices):
    x = 0
    for i in indices:
        x ^= (i & 1)
    return x


def _index_access(lst, indices):
    x = 0
    for i in indices:
        x ^= (lst[i] & 1)
    return x


def _loop_overhead_fixed(accesses):
    x = 0
    for i in range(accesses):
        x ^= (i & 1)
    return x


def _index_access_fixed(lst, idx, accesses):
    x = 0
    for i in range(accesses):
        x ^= ((lst[idx] + i) & 1)
    return x


def measure_index_time_ns(lst, indices, repeat=7):
    timer_overhead = timeit.Timer(lambda: _loop_overhead(indices))
    timer_index = timeit.Timer(lambda: _index_access(lst, indices))

    overhead_samples = timer_overhead.repeat(repeat=repeat, number=1)
    index_samples = timer_index.repeat(repeat=repeat, number=1)

    overhead = min(overhead_samples)
    index_total = min(index_samples)
    net = max(index_total - overhead, 0.0)
    return net / len(indices) * 1e9


def measure_fixed_index_time_ns(lst, idx, accesses=500_000, repeat=7):
    timer_overhead = timeit.Timer(lambda: _loop_overhead_fixed(accesses))
    timer_index = timeit.Timer(lambda: _index_access_fixed(lst, idx, accesses))

    overhead_samples = timer_overhead.repeat(repeat=repeat, number=1)
    index_samples = timer_index.repeat(repeat=repeat, number=1)

    overhead = min(overhead_samples)
    index_total = min(index_samples)
    net = max(index_total - overhead, 0.0)
    return net / accesses * 1e9


def measure_linear_scan_ms(lst, repeat=5):
    timer_scan = timeit.Timer(lambda: sum(lst))
    samples = timer_scan.repeat(repeat=repeat, number=1)
    return min(samples) * 1e3


def run_experiment(
    start=1_000,
    stop=1_000_000,
    random_accesses_per_n=200_000,
    fixed_accesses_per_n=500_000,
    seed=42,
):
    rng = random.Random(seed)
    points = []

    for n in geometric_sizes(start=start, stop=stop, factor=2):
        lst = list(range(n))
        indices = [rng.randrange(n) for _ in range(random_accesses_per_n)]

        # Head/Middle/Tail access is used as the primary O(1) indicator.
        head_ns = measure_fixed_index_time_ns(lst, 0, accesses=fixed_accesses_per_n)
        mid_ns = measure_fixed_index_time_ns(lst, n // 2, accesses=fixed_accesses_per_n)
        tail_ns = measure_fixed_index_time_ns(lst, n - 1, accesses=fixed_accesses_per_n)
        hmt_ns = statistics.mean([head_ns, mid_ns, tail_ns])

        random_ns = measure_index_time_ns(lst, indices)
        scan_ms = measure_linear_scan_ms(lst)
        points.append(
            Point(
                n=n,
                index_hmt_ns=hmt_ns,
                index_random_ns=random_ns,
                scan_ms=scan_ms,
            )
        )

    return points


def write_csv(points, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "index_hmt_ns", "index_random_ns", "scan_time_ms"])
        for p in points:
            writer.writerow(
                [p.n, f"{p.index_hmt_ns:.4f}", f"{p.index_random_ns:.4f}", f"{p.scan_ms:.4f}"]
            )


def evaluate(points):
    ns = [p.n for p in points]
    index_hmt = [p.index_hmt_ns for p in points]
    index_random = [p.index_random_ns for p in points]
    scan_times = [p.scan_ms for p in points]

    slope_index_hmt = linear_regression_slope_loglog(ns, index_hmt)
    slope_index_random = linear_regression_slope_loglog(ns, index_random)
    slope_scan = linear_regression_slope_loglog(ns, scan_times)

    ratio_hmt = max(index_hmt) / min(index_hmt)
    looks_constant = abs(slope_index_hmt) <= 0.10 and ratio_hmt <= 2.0

    return {
        "slope_index_hmt": slope_index_hmt,
        "slope_index_random": slope_index_random,
        "slope_scan": slope_scan,
        "ratio_hmt": ratio_hmt,
        "looks_constant": looks_constant,
    }


def print_report(points, metrics):
    print("Experiment: Python list indexing complexity")
    print("Control variables:")
    print("- Fixed RNG seed and fixed accesses_per_n")
    print("- GC disabled during measurements")
    print("- Compare indexing with loop-overhead baseline")
    print("- Add linear scan as O(n) contrast")
    print()
    print(f"{'n':>10} {'hmt(ns)':>12} {'random(ns)':>12} {'scan(ms)':>12}")
    print("-" * 52)
    for p in points:
        print(f"{p.n:>10} {p.index_hmt_ns:>12.3f} {p.index_random_ns:>12.3f} {p.scan_ms:>12.3f}")

    print("\nlog-log slope (index h/m/t):", f"{metrics['slope_index_hmt']:.3f}")
    print("log-log slope (index random):", f"{metrics['slope_index_random']:.3f}")
    print("log-log slope (scan) :", f"{metrics['slope_scan']:.3f}")
    print("max/min h/m/t ratio   :", f"{metrics['ratio_hmt']:.3f}")

    if metrics["looks_constant"]:
        print("Conclusion: fixed-position indexing is approximately O(1) in this range.")
    else:
        print("Conclusion: result is noisy or outside threshold; rerun with larger fixed_accesses_per_n.")


def main():
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        points = run_experiment(
            start=1_000,
            stop=1_000_000,
            random_accesses_per_n=200_000,
            fixed_accesses_per_n=500_000,
        )
    finally:
        if gc_was_enabled:
            gc.enable()

    metrics = evaluate(points)
    print_report(points, metrics)

    out_csv = Path(__file__).with_name("index_complexity_results.csv")
    write_csv(points, out_csv)
    print(f"\nCSV saved to: {out_csv}")


if __name__ == "__main__":
    main()


