from __future__ import annotations

from typing import Any

from 后序表达式计算 import postfix_eval


def _assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message} | actual={actual}, expected={expected}")


def _assert_raises(expr: str, expected_exc: type[BaseException], message: str) -> None:
    try:
        postfix_eval(expr)
        raise AssertionError(f"{message} | expected exception={expected_exc.__name__}")
    except expected_exc:
        pass


def test_fixed_cases() -> None:
    cases = [
        ("4 5 +", 9),
        ("7 8 * 4 +", 60),
        ("9 3 /", 3.0),
        ("1 2 + 3 4 + *", 21),
        ("10 2 8 * + 3 -", 23),
        ("20 5 -", 15),
        ("42", 42),
    ]

    for expr, expected in cases:
        _assert_equal(postfix_eval(expr), expected, f"postfix_eval failed expr={expr}")


def test_exception_cases() -> None:
    _assert_raises("", IndexError, "empty expression should fail")
    _assert_raises("1 +", IndexError, "insufficient operands should fail")
    _assert_raises("2 3 ^", ValueError, "unknown operator should fail")
    _assert_raises("4 0 /", ZeroDivisionError, "division by zero should fail")


def run_all_tests() -> None:
    test_fixed_cases()
    test_exception_cases()
    print("All checks passed: fixed cases and exception checks.")


if __name__ == "__main__":
    run_all_tests()

