import gc
import statistics
import timeit


def test1(n=1000):
    l = []
    for i in range(n):
        l = l + [i]
    return l


def test2(n=1000):
    l = []
    for i in range(n):
        l.append(i)
    return l


def test3(n=1000):
    return [i for i in range(n)]


def test4(n=1000):
    return list(range(n))


def benchmark(func, n=1000, repeat=5, number=1000):
    """Return timing stats in seconds for func(n)."""
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        timer = timeit.Timer(lambda: func(n))
        samples = timer.repeat(repeat=repeat, number=number)
    finally:
        if gc_was_enabled:
            gc.enable()

    return {
        "name": func.__name__,
        "min": min(samples) / number,
        "mean": statistics.mean(samples) / number,
        "stdev": (statistics.stdev(samples) / number) if len(samples) > 1 else 0.0,
    }


def validate_equivalence(n_small=20):
    expected = list(range(n_small))
    funcs = [test1, test2, test3, test4]
    for func in funcs:
        result = func(n_small)
        if result != expected:
            raise ValueError(f"{func.__name__} result mismatch")


def main():
    n = 1000
    repeat = 7
    number = 1000

    validate_equivalence()

    funcs = [test1, test2, test3, test4]
    results = [benchmark(f, n=n, repeat=repeat, number=number) for f in funcs]
    results.sort(key=lambda x: x["mean"])

    print(f"Benchmark: n={n}, repeat={repeat}, number={number}")
    print("(unit: seconds per call)")
    print("-" * 58)
    print(f"{'Function':<10} {'min':>14} {'mean':>14} {'stdev':>14}")
    print("-" * 58)
    for item in results:
        print(
            f"{item['name']:<10} "
            f"{item['min']:>14.8f} "
            f"{item['mean']:>14.8f} "
            f"{item['stdev']:>14.8f}"
        )


if __name__ == "__main__":
    main()
