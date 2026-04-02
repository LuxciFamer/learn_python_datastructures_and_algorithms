from __future__ import annotations

import random
from typing import Callable, Iterable

from 计算01 import select_kth, select_kth_by_sort


Solver = Callable[[Iterable[int], int], int]


def _assert_equal(actual: int, expected: int, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message} | actual={actual}, expected={expected}")


def test_fixed_cases() -> None:
    cases = [
        ([5], 1),
        ([3, 1, 2], 1),
        ([3, 1, 2], 3),
        ([4, 4, 4, 4], 2),
        ([-5, -1, -3, 2, 0], 4),
        ([1, 2, 3, 4, 5], 2),
        ([5, 4, 3, 2, 1], 4),
        ([23, 5, 17, 9, 42, 1, 30, 17, 8, 15, 3], 5),
    ]

    for nums, k in cases:
        expected = sorted(nums)[k - 1]
        _assert_equal(select_kth(nums, k), expected, f"BFPRT failed nums={nums}, k={k}")
        _assert_equal(
            select_kth_by_sort(nums, k),
            expected,
            f"Sort method failed nums={nums}, k={k}",
        )


def test_random_cases(trials: int = 2000, max_n: int = 150) -> None:
    for _ in range(trials):
        n = random.randint(1, max_n)
        nums = [random.randint(-10000, 10000) for _ in range(n)]
        k = random.randint(1, n)

        expected = sorted(nums)[k - 1]
        _assert_equal(select_kth(nums, k), expected, f"BFPRT random failed k={k}")
        _assert_equal(select_kth_by_sort(nums, k), expected, f"Sort random failed k={k}")


def test_exceptions() -> None:
    bad_calls = [
        ([], 1),
        ([1, 2, 3], 0),
        ([1, 2, 3], 4),
    ]

    for nums, k in bad_calls:
        for solver in (select_kth, select_kth_by_sort):
            try:
                solver(nums, k)
                raise AssertionError(f"{solver.__name__} should raise ValueError for nums={nums}, k={k}")
            except ValueError:
                pass


def run_all_tests() -> None:
    random.seed(20260325)
    test_fixed_cases()
    test_random_cases()
    test_exceptions()
    print("All checks passed: fixed cases, random cross-check, and exception checks.")


if __name__ == "__main__":
    run_all_tests()

