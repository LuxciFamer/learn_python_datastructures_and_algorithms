from __future__ import annotations

from typing import Iterable, List


def _validate_and_copy(nums: Iterable[int], k: int) -> List[int]:
    arr = list(nums)
    if not arr:
        raise ValueError("nums 不能为空")
    if not 1 <= k <= len(arr):
        raise ValueError(f"k 必须在 1..{len(arr)} 范围内")
    return arr


def select_kth(nums: Iterable[int], k: int) -> int:
    """返回 nums 中第 k 小的元素（k 从 1 开始计数）。

    使用 BFPRT（Median of Medians）选择枢轴，最坏时间复杂度 O(n)。
    该函数不会修改调用者传入的原始序列。
    """
    arr = _validate_and_copy(nums, k)

    return _bfprt_select(arr, k - 1)


def select_kth_by_sort(nums: Iterable[int], k: int) -> int:
    """返回 nums 中第 k 小的元素（排序法，时间复杂度 O(n log n)）。"""
    arr = _validate_and_copy(nums, k)
    return sorted(arr)[k - 1]


def _bfprt_select(arr: List[int], index: int) -> int:
    # 递归终止：只剩一个元素时，它就是答案。
    if len(arr) == 1:
        return arr[0]

    pivot = _median_of_medians(arr)

    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    if index < len(less):
        return _bfprt_select(less, index)

    if index < len(less) + len(equal):
        return pivot

    return _bfprt_select(greater, index - len(less) - len(equal))


def _median_of_medians(arr: List[int]) -> int:
    # 每 5 个分一组，组内排序后取中位数。
    groups = [arr[i : i + 5] for i in range(0, len(arr), 5)]
    medians = [sorted(group)[len(group) // 2] for group in groups]

    # 中位数列表长度 <= 5 时可直接求中位数。
    if len(medians) <= 5:
        return sorted(medians)[len(medians) // 2]

    # 递归求“中位数的中位数”。
    return _bfprt_select(medians, len(medians) // 2)


if __name__ == "__main__":
    data = [23, 5, 17, 9, 42, 1, 30, 17, 8, 15, 3]
    k = 5

    bfprt_result = select_kth(data, k)
    sort_result = select_kth_by_sort(data, k)

    print("原始数据:", data)
    print(f"BFPRT 第 {k} 小元素:", bfprt_result)
    print(f"排序法 第 {k} 小元素:", sort_result)
    print("两种方法是否一致:", bfprt_result == sort_result)

