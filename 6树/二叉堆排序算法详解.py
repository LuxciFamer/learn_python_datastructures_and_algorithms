"""
================================================================================
                        二叉堆排序算法详解与实现
================================================================================

本文件完整实现二叉堆数据结构及其排序算法，包含：
1. 二叉堆的完整数据结构实现
2. 支持自定义比较函数的通用堆
3. 原地排序版本的堆排序（空间复杂度O(1)）
4. 详细的算法原理说明和复杂度分析
5. 完整的测试用例和边界情况处理

二叉堆是一种特殊的完全二叉树，具有以下性质：
- 大顶堆：每个节点的值都大于或等于其子节点的值
- 小顶堆：每个节点的值都小于或等于其子节点的值
================================================================================
"""

from typing import List, Optional, Callable, TypeVar, Generic, Any
from dataclasses import dataclass
import random
import time

T = TypeVar('T')


# ==============================================================================
# 第一部分：二叉堆数据结构基础
# ==============================================================================

class BinaryHeap(Generic[T]):
    """
    通用二叉堆实现
    
    【数据结构设计】
    二叉堆通常使用数组进行存储，因为：
    1. 完全二叉树可以用数组紧凑存储
    2. 父子节点的索引关系简单：
       - 父节点索引: parent(i) = (i - 1) // 2
       - 左子节点索引: left_child(i) = 2 * i + 1
       - 右子节点索引: right_child(i) = 2 * i + 2
    3. 数组存储具有更好的缓存局部性
    
    【时间复杂度】
    - 建堆: O(n)
    - 插入: O(log n)
    - 删除堆顶: O(log n)
    - 获取堆顶: O(1)
    
    【空间复杂度】
    - O(n) 用于存储堆元素
    """
    
    def __init__(
        self, 
        comparator: Optional[Callable[[T, T], bool]] = None,
        is_max_heap: bool = True
    ):
        """
        初始化二叉堆
        
        Args:
            comparator: 自定义比较函数，返回True表示第一个参数应排在堆顶
                       默认为None，使用默认的比较规则
            is_max_heap: 是否为大顶堆，True为大顶堆，False为小顶堆
                        仅在comparator为None时生效
        """
        self._data: List[T] = []
        self._comparator = self._create_comparator(comparator, is_max_heap)
        self._is_max_heap = is_max_heap
        self._operation_count = 0
        
    def _create_comparator(
        self, 
        comparator: Optional[Callable[[T, T], bool]], 
        is_max_heap: bool
    ) -> Callable[[T, T], bool]:
        """
        创建比较函数
        
        比较函数定义了堆的排序规则：
        - 返回True表示第一个参数应该"上升"到堆顶
        - 返回False表示第二个参数应该"上升"到堆顶
        
        Args:
            comparator: 用户提供的自定义比较函数
            is_max_heap: 是否为大顶堆
            
        Returns:
            比较函数
        """
        if comparator is not None:
            return comparator
        
        if is_max_heap:
            return lambda a, b: a > b
        else:
            return lambda a, b: a < b
    
    def parent(self, index: int) -> int:
        """
        获取父节点索引
        
        对于索引为i的节点，其父节点索引为 (i-1) // 2
        
        Args:
            index: 当前节点索引
            
        Returns:
            父节点索引，如果当前节点是根节点则返回-1
        """
        return (index - 1) // 2 if index > 0 else -1
    
    def left_child(self, index: int) -> int:
        """
        获取左子节点索引
        
        对于索引为i的节点，其左子节点索引为 2*i + 1
        
        Args:
            index: 当前节点索引
            
        Returns:
            左子节点索引
        """
        return 2 * index + 1
    
    def right_child(self, index: int) -> int:
        """
        获取右子节点索引
        
        对于索引为i的节点，其右子节点索引为 2*i + 2
        
        Args:
            index: 当前节点索引
            
        Returns:
            右子节点索引
        """
        return 2 * index + 2
    
    def __len__(self) -> int:
        """返回堆中元素个数"""
        return len(self._data)
    
    def __bool__(self) -> bool:
        """堆是否非空"""
        return len(self._data) > 0
    
    def __repr__(self) -> str:
        """堆的字符串表示"""
        heap_type = "大顶堆" if self._is_max_heap else "小顶堆"
        return f"BinaryHeap({heap_type}, size={len(self._data)}, data={self._data})"
    
    def is_empty(self) -> bool:
        """判断堆是否为空"""
        return len(self._data) == 0
    
    def peek(self) -> Optional[T]:
        """
        查看堆顶元素（不删除）
        
        时间复杂度: O(1)
        
        Returns:
            堆顶元素，如果堆为空则返回None
        """
        return self._data[0] if self._data else None
    
    def _swap(self, i: int, j: int) -> None:
        """
        交换堆中两个位置的元素
        
        Args:
            i: 第一个位置的索引
            j: 第二个位置的索引
        """
        self._data[i], self._data[j] = self._data[j], self._data[i]
        self._operation_count += 1
    
    def _sift_up(self, index: int) -> None:
        """
        上浮操作（堆化向上）
        
        当新元素插入到堆底时，需要将其上浮到正确位置。
        上浮过程：
        1. 比较当前节点与其父节点
        2. 如果当前节点应该排在父节点前面，则交换
        3. 重复直到到达根节点或满足堆性质
        
        时间复杂度: O(log n)
        
        Args:
            index: 需要上浮的节点索引
        """
        while index > 0:
            parent_idx = self.parent(index)
            if self._comparator(self._data[index], self._data[parent_idx]):
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                break
    
    def _sift_down(self, index: int, size: Optional[int] = None) -> None:
        """
        下沉操作（堆化向下）
        
        当堆顶元素被移除或替换时，需要将新的堆顶元素下沉到正确位置。
        下沉过程：
        1. 比较当前节点与其两个子节点
        2. 找出应该排在最前面的节点
        3. 如果子节点应该排在前面，则交换
        4. 重复直到到达叶子节点或满足堆性质
        
        时间复杂度: O(log n)
        
        Args:
            index: 需要下沉的节点索引
            size: 堆的有效大小（用于原地排序时限制范围）
        """
        if size is None:
            size = len(self._data)
        
        while True:
            left = self.left_child(index)
            right = self.right_child(index)
            target = index
            
            if left < size and self._comparator(self._data[left], self._data[target]):
                target = left
            
            if right < size and self._comparator(self._data[right], self._data[target]):
                target = right
            
            if target != index:
                self._swap(index, target)
                index = target
            else:
                break
    
    def insert(self, value: T) -> None:
        """
        向堆中插入元素
        
        插入过程：
        1. 将新元素添加到数组末尾
        2. 对新元素执行上浮操作，恢复堆性质
        
        时间复杂度: O(log n)
        
        Args:
            value: 要插入的元素
        """
        self._data.append(value)
        self._sift_up(len(self._data) - 1)
    
    def extract(self) -> Optional[T]:
        """
        移除并返回堆顶元素
        
        移除过程：
        1. 保存堆顶元素
        2. 将堆底元素移到堆顶
        3. 删除堆底元素
        4. 对堆顶元素执行下沉操作，恢复堆性质
        
        时间复杂度: O(log n)
        
        Returns:
            堆顶元素，如果堆为空则返回None
        """
        if not self._data:
            return None
        
        if len(self._data) == 1:
            return self._data.pop()
        
        top = self._data[0]
        self._data[0] = self._data.pop()
        self._sift_down(0)
        
        return top
    
    def build_heap(self, arr: List[T]) -> None:
        """
        从数组构建堆
        
        建堆方法：从最后一个非叶子节点开始，自底向上执行下沉操作
        
        为什么从最后一个非叶子节点开始？
        - 叶子节点本身已经是合法的堆
        - 从下往上处理可以保证每个子树都是合法的堆
        
        为什么时间复杂度是O(n)而不是O(n log n)？
        - 大多数节点在较低层级，下沉距离短
        - 数学证明：总操作次数 = sum(h-i)*2^i，其中h是树高
        - 结果收敛于O(n)
        
        时间复杂度: O(n)
        
        Args:
            arr: 用于构建堆的数组
        """
        self._data = arr.copy()
        n = len(self._data)
        
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)
    
    def replace(self, value: T) -> Optional[T]:
        """
        替换堆顶元素
        
        操作过程：
        1. 保存原堆顶元素
        2. 用新值替换堆顶
        3. 执行下沉操作恢复堆性质
        
        时间复杂度: O(log n)
        
        Args:
            value: 新的堆顶值
            
        Returns:
            原堆顶元素，如果堆为空则返回None
        """
        if not self._data:
            self._data.append(value)
            return None
        
        old_top = self._data[0]
        self._data[0] = value
        self._sift_down(0)
        
        return old_top
    
    def get_data(self) -> List[T]:
        """获取堆数据的副本"""
        return self._data.copy()
    
    def clear(self) -> None:
        """清空堆"""
        self._data.clear()
        self._operation_count = 0


# ==============================================================================
# 第二部分：原地堆排序实现
# ==============================================================================

class InPlaceHeapSort:
    """
    原地堆排序实现
    
    【算法原理】
    堆排序是一种基于比较的排序算法，利用堆的性质进行排序。
    
    排序过程（升序使用大顶堆）：
    1. 建堆阶段：将无序数组构建成大顶堆，时间复杂度O(n)
    2. 排序阶段：
       a. 将堆顶（最大值）与末尾元素交换
       b. 对剩余元素重新调整为堆
       c. 重复直到所有元素有序
    3. 时间复杂度：O(n log n)
    
    【为什么升序排序使用大顶堆？】
    - 大顶堆的堆顶是最大值
    - 每次将最大值交换到数组末尾
    - 最终数组从小到大排列
    
    【原地排序原理】
    - 堆排序过程中，已排序部分在数组末尾
    - 未排序部分在数组前面，作为堆
    - 不需要额外空间，空间复杂度O(1)
    
    【时间复杂度】
    - 最好情况: O(n log n)
    - 平均情况: O(n log n)
    - 最坏情况: O(n log n)
    
    【空间复杂度】
    - O(1) - 原地排序，仅需常数额外空间
    
    【稳定性】
    - 不稳定排序：相同元素的相对位置可能改变
    
    【优缺点】
    优点：
    - 时间复杂度稳定为O(n log n)
    - 原地排序，空间效率高
    - 对输入数据不敏感
    
    缺点：
    - 不稳定排序
    - 常数因子较大，实际性能可能不如快速排序
    - 无法利用数据的初始有序性
    """
    
    def __init__(self, comparator: Optional[Callable[[Any, Any], bool]] = None):
        """
        初始化堆排序器
        
        Args:
            comparator: 自定义比较函数
        """
        self.comparator = comparator
        self.compare_count = 0
        self.swap_count = 0
    
    def _parent(self, index: int) -> int:
        """获取父节点索引"""
        return (index - 1) // 2
    
    def _left_child(self, index: int) -> int:
        """获取左子节点索引"""
        return 2 * index + 1
    
    def _right_child(self, index: int) -> int:
        """获取右子节点索引"""
        return 2 * index + 2
    
    def _compare(self, a: Any, b: Any, ascending: bool) -> bool:
        """
        比较两个元素
        
        Args:
            a: 第一个元素
            b: 第二个元素
            ascending: 是否升序排序
            
        Returns:
            如果a应该排在b前面返回True
        """
        self.compare_count += 1
        if self.comparator is not None:
            return self.comparator(a, b)
        return a > b if ascending else a < b
    
    def _sift_down(
        self, 
        arr: List[Any], 
        index: int, 
        size: int, 
        ascending: bool
    ) -> None:
        """
        原地下沉操作
        
        Args:
            arr: 待排序数组
            index: 当前节点索引
            size: 堆的有效大小
            ascending: 是否升序排序
        """
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            target = index
            
            if left < size and self._compare(arr[left], arr[target], ascending):
                target = left
            
            if right < size and self._compare(arr[right], arr[target], ascending):
                target = right
            
            if target != index:
                arr[index], arr[target] = arr[target], arr[index]
                self.swap_count += 1
                index = target
            else:
                break
    
    def _build_heap(self, arr: List[Any], size: int, ascending: bool) -> None:
        """
        原地建堆
        
        Args:
            arr: 待排序数组
            size: 数组大小
            ascending: 是否升序排序
        """
        for i in range(size // 2 - 1, -1, -1):
            self._sift_down(arr, i, size, ascending)
    
    def sort(
        self, 
        arr: List[Any], 
        ascending: bool = True,
        in_place: bool = False
    ) -> List[Any]:
        """
        堆排序主函数
        
        Args:
            arr: 待排序数组
            ascending: 是否升序排序（默认True）
            in_place: 是否原地排序（默认False，返回新数组）
            
        Returns:
            排序后的数组
        """
        if not arr:
            return [] if not in_place else arr
        
        if len(arr) == 1:
            return arr.copy() if not in_place else arr
        
        self.compare_count = 0
        self.swap_count = 0
        
        if in_place:
            result = arr
        else:
            result = arr.copy()
        
        n = len(result)
        
        self._build_heap(result, n, ascending)
        
        for i in range(n - 1, 0, -1):
            result[0], result[i] = result[i], result[0]
            self.swap_count += 1
            self._sift_down(result, 0, i, ascending)
        
        return result


def heap_sort(
    arr: List[Any], 
    ascending: bool = True,
    comparator: Optional[Callable[[Any, Any], bool]] = None
) -> List[Any]:
    """
    堆排序便捷函数
    
    使用示例：
    >>> heap_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    
    >>> heap_sort([3, 1, 4, 1, 5, 9, 2, 6], ascending=False)
    [9, 6, 5, 4, 3, 2, 1, 1]
    
    >>> # 自定义比较函数：按字符串长度排序
    >>> heap_sort(['abc', 'a', 'abcd', 'ab'], comparator=lambda a, b: len(a) > len(b))
    ['a', 'ab', 'abc', 'abcd']
    
    Args:
        arr: 待排序数组
        ascending: 是否升序排序
        comparator: 自定义比较函数
        
    Returns:
        排序后的数组
    """
    sorter = InPlaceHeapSort(comparator)
    return sorter.sort(arr, ascending=ascending, in_place=False)


def heap_sort_in_place(
    arr: List[Any], 
    ascending: bool = True,
    comparator: Optional[Callable[[Any, Any], bool]] = None
) -> None:
    """
    原地堆排序便捷函数
    
    直接在原数组上进行排序，不创建新数组，空间复杂度O(1)
    
    使用示例：
    >>> data = [3, 1, 4, 1, 5, 9, 2, 6]
    >>> heap_sort_in_place(data)
    >>> data
    [1, 1, 2, 3, 4, 5, 6, 9]
    
    Args:
        arr: 待排序数组（将被原地修改）
        ascending: 是否升序排序
        comparator: 自定义比较函数
    """
    sorter = InPlaceHeapSort(comparator)
    sorter.sort(arr, ascending=ascending, in_place=True)


# ==============================================================================
# 第三部分：测试框架
# ==============================================================================

@dataclass
class TestResult:
    """测试结果数据类"""
    test_name: str
    input_data: List[Any]
    expected: List[Any]
    actual: List[Any]
    passed: bool
    time_elapsed: float
    error_message: Optional[str] = None


class HeapSortTester:
    """
    堆排序测试类
    
    提供全面的测试用例，验证堆排序在各种场景下的正确性
    """
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.passed_count = 0
        self.failed_count = 0
    
    def run_test(
        self, 
        test_name: str, 
        input_data: List[Any], 
        expected: List[Any],
        ascending: bool = True,
        comparator: Optional[Callable[[Any, Any], bool]] = None
    ) -> TestResult:
        """
        执行单个测试用例
        
        Args:
            test_name: 测试名称
            input_data: 输入数据
            expected: 期望结果
            ascending: 是否升序
            comparator: 自定义比较函数
            
        Returns:
            测试结果
        """
        start_time = time.perf_counter()
        
        try:
            actual = heap_sort(input_data, ascending=ascending, comparator=comparator)
            passed = actual == expected
            error_message = None
        except Exception as e:
            actual = []
            passed = False
            error_message = str(e)
        
        end_time = time.perf_counter()
        
        result = TestResult(
            test_name=test_name,
            input_data=input_data.copy() if input_data else [],
            expected=expected,
            actual=actual,
            passed=passed,
            time_elapsed=end_time - start_time,
            error_message=error_message
        )
        
        self.results.append(result)
        if passed:
            self.passed_count += 1
        else:
            self.failed_count += 1
        
        return result
    
    def test_empty_array(self) -> TestResult:
        """测试空数组"""
        return self.run_test("空数组测试", [], [])
    
    def test_single_element(self) -> TestResult:
        """测试单元素数组"""
        return self.run_test("单元素测试", [42], [42])
    
    def test_two_elements(self) -> TestResult:
        """测试两元素数组"""
        result1 = self.run_test("两元素-无序", [2, 1], [1, 2])
        result2 = self.run_test("两元素-有序", [1, 2], [1, 2])
        return result1
    
    def test_duplicate_elements(self) -> TestResult:
        """测试重复元素"""
        return self.run_test("重复元素测试", [3, 1, 4, 1, 5, 9, 2, 6, 5], [1, 1, 2, 3, 4, 5, 5, 6, 9])
    
    def test_all_same_elements(self) -> TestResult:
        """测试全部相同元素"""
        return self.run_test("全部相同元素测试", [5, 5, 5, 5, 5], [5, 5, 5, 5, 5])
    
    def test_sorted_ascending(self) -> TestResult:
        """测试已升序排列的数组"""
        return self.run_test("已升序数组测试", [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    def test_sorted_descending(self) -> TestResult:
        """测试已降序排列的数组"""
        return self.run_test("已降序数组测试", [9, 8, 7, 6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    def test_random_data(self) -> TestResult:
        """测试随机数据"""
        random.seed(42)
        data = [random.randint(1, 1000) for _ in range(100)]
        expected = sorted(data)
        return self.run_test("随机数据测试(100个元素)", data, expected)
    
    def test_large_random_data(self) -> TestResult:
        """测试大规模随机数据"""
        random.seed(123)
        data = [random.randint(1, 100000) for _ in range(10000)]
        expected = sorted(data)
        return self.run_test("大规模随机数据测试(10000个元素)", data, expected)
    
    def test_negative_numbers(self) -> TestResult:
        """测试负数"""
        return self.run_test("负数测试", [-3, -1, -4, -1, -5, -9, -2, -6], [-9, -6, -5, -4, -3, -2, -1, -1])
    
    def test_mixed_positive_negative(self) -> TestResult:
        """测试正负混合"""
        return self.run_test("正负混合测试", [3, -1, 4, -1, 5, -9, 2, -6], [-9, -6, -1, -1, 2, 3, 4, 5])
    
    def test_descending_order(self) -> TestResult:
        """测试降序排序"""
        return self.run_test("降序排序测试", [3, 1, 4, 1, 5, 9, 2, 6], [9, 6, 5, 4, 3, 2, 1, 1], ascending=False)
    
    def test_custom_comparator_string_length(self) -> TestResult:
        """测试自定义比较函数（字符串长度）"""
        data = ['abc', 'a', 'abcd', 'ab', 'abcde']
        expected = ['a', 'ab', 'abc', 'abcd', 'abcde']
        return self.run_test(
            "自定义比较函数测试(字符串长度)", 
            data, 
            expected, 
            comparator=lambda a, b: len(a) > len(b)
        )
    
    def test_custom_comparator_tuple(self) -> TestResult:
        """测试自定义比较函数（元组第二元素）"""
        data = [(1, 5), (2, 3), (3, 1), (4, 4)]
        expected = [(3, 1), (2, 3), (4, 4), (1, 5)]
        return self.run_test(
            "自定义比较函数测试(元组第二元素)", 
            data, 
            expected, 
            comparator=lambda a, b: a[1] > b[1]
        )
    
    def test_float_numbers(self) -> TestResult:
        """测试浮点数"""
        return self.run_test("浮点数测试", [3.14, 1.41, 2.71, 0.577, 1.732], [0.577, 1.41, 1.732, 2.71, 3.14])
    
    def test_in_place_sort(self) -> bool:
        """测试原地排序"""
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        original_id = id(data)
        heap_sort_in_place(data)
        
        passed = data == [1, 1, 2, 3, 4, 5, 6, 9] and id(data) == original_id
        
        result = TestResult(
            test_name="原地排序测试",
            input_data=[3, 1, 4, 1, 5, 9, 2, 6],
            expected=[1, 1, 2, 3, 4, 5, 6, 9],
            actual=data,
            passed=passed,
            time_elapsed=0
        )
        
        self.results.append(result)
        if passed:
            self.passed_count += 1
        else:
            self.failed_count += 1
        
        return passed
    
    def run_all_tests(self) -> None:
        """运行所有测试"""
        print("="*70)
        print("                    二叉堆排序测试报告")
        print("="*70)
        
        self.test_empty_array()
        self.test_single_element()
        self.test_two_elements()
        self.test_duplicate_elements()
        self.test_all_same_elements()
        self.test_sorted_ascending()
        self.test_sorted_descending()
        self.test_random_data()
        self.test_large_random_data()
        self.test_negative_numbers()
        self.test_mixed_positive_negative()
        self.test_descending_order()
        self.test_custom_comparator_string_length()
        self.test_custom_comparator_tuple()
        self.test_float_numbers()
        self.test_in_place_sort()
        
        self.print_report()
    
    def print_report(self) -> None:
        """打印测试报告"""
        print("\n" + "-"*70)
        print("测试结果详情:")
        print("-"*70)
        
        for result in self.results:
            status = "[PASS]" if result.passed else "[FAIL]"
            print(f"\n{status} {result.test_name}")
            print(f"  耗时: {result.time_elapsed:.6f} 秒")
            
            if not result.passed:
                if result.error_message:
                    print(f"  错误: {result.error_message}")
                else:
                    if len(result.input_data) <= 10:
                        print(f"  输入: {result.input_data}")
                        print(f"  期望: {result.expected}")
                        print(f"  实际: {result.actual}")
                    else:
                        print(f"  输入长度: {len(result.input_data)}")
                        print(f"  期望长度: {len(result.expected)}")
                        print(f"  实际长度: {len(result.actual)}")
        
        print("\n" + "="*70)
        print(f"测试统计: 通过 {self.passed_count}/{len(self.results)}")
        print("="*70)


# ==============================================================================
# 第四部分：BinaryHeap类的额外测试
# ==============================================================================

def test_binary_heap_operations():
    """测试BinaryHeap类的各种操作"""
    print("\n" + "="*70)
    print("                 BinaryHeap类操作测试")
    print("="*70)
    
    print("\n【测试1: 大顶堆基本操作】")
    max_heap = BinaryHeap(is_max_heap=True)
    
    for val in [3, 1, 4, 1, 5, 9, 2, 6]:
        max_heap.insert(val)
        print(f"  插入 {val}, 堆顶: {max_heap.peek()}")
    
    print(f"\n堆大小: {len(max_heap)}")
    print(f"堆数据: {max_heap.get_data()}")
    
    print("\n依次取出堆顶元素:")
    while max_heap:
        top = max_heap.extract()
        print(f"  取出: {top}, 剩余堆顶: {max_heap.peek()}")
    
    print("\n【测试2: 小顶堆基本操作】")
    min_heap = BinaryHeap(is_max_heap=False)
    min_heap.build_heap([3, 1, 4, 1, 5, 9, 2, 6])
    
    print(f"建堆后数据: {min_heap.get_data()}")
    print(f"堆顶（最小值）: {min_heap.peek()}")
    
    print("\n【测试3: 自定义比较函数】")
    str_heap = BinaryHeap(comparator=lambda a, b: len(a) > len(b))
    for s in ['abc', 'a', 'abcd', 'ab', 'abcde']:
        str_heap.insert(s)
    
    print("按字符串长度排序（从长到短）:")
    result = []
    while str_heap:
        result.append(str_heap.extract())
    print(f"  结果: {result}")
    
    print("\n【测试4: replace操作】")
    heap = BinaryHeap(is_max_heap=True)
    heap.build_heap([1, 2, 3, 4, 5])
    print(f"原堆顶: {heap.peek()}")
    old = heap.replace(10)
    print(f"替换后: 旧值={old}, 新堆顶={heap.peek()}")
    
    print("\n【测试5: 边界情况】")
    empty_heap = BinaryHeap()
    print(f"空堆peek: {empty_heap.peek()}")
    print(f"空堆extract: {empty_heap.extract()}")
    print(f"空堆replace(1): {empty_heap.replace(1)}")
    print(f"replace后堆顶: {empty_heap.peek()}")


# ==============================================================================
# 第五部分：性能对比
# ==============================================================================

def performance_comparison():
    """性能对比测试"""
    print("\n" + "="*70)
    print("                    性能对比测试")
    print("="*70)
    
    sizes = [100, 1000, 10000, 100000]
    
    print("\n" + "-"*70)
    print(f"{'数据量':<15} {'堆排序(秒)':<15} {'Python内置排序(秒)':<20} {'比较':<10}")
    print("-"*70)
    
    for size in sizes:
        random.seed(42)
        data = [random.randint(1, size * 10) for _ in range(size)]
        
        start = time.perf_counter()
        heap_sort(data)
        heap_time = time.perf_counter() - start
        
        start = time.perf_counter()
        sorted(data)
        builtin_time = time.perf_counter() - start
        
        ratio = heap_time / builtin_time if builtin_time > 0 else 0
        
        print(f"{size:<15} {heap_time:<15.6f} {builtin_time:<20.6f} {ratio:.2f}x")


# ==============================================================================
# 第六部分：算法可视化
# ==============================================================================

def visualize_heap_process():
    """可视化堆排序过程"""
    print("\n" + "="*70)
    print("                    堆排序过程可视化")
    print("="*70)
    
    data = [4, 10, 3, 5, 1]
    print(f"\n原始数组: {data}")
    
    def print_heap(arr, size=None):
        if size is None:
            size = len(arr)
        if size == 0:
            print("  (空堆)")
            return
        
        levels = []
        level = 0
        index = 0
        
        while index < size:
            level_size = 2 ** level
            level_nodes = arr[index:min(index + level_size, size)]
            levels.append(level_nodes)
            index += level_size
            level += 1
        
        for i, level_nodes in enumerate(levels):
            indent = "  " * (len(levels) - i - 1)
            print(f"{indent}{' '.join(map(str, level_nodes))}")
    
    print("\n建堆过程:")
    heap = BinaryHeap(is_max_heap=True)
    heap.build_heap(data)
    print(f"建堆后数组: {heap.get_data()}")
    print("\n堆结构:")
    print_heap(heap.get_data())
    
    print("\n排序过程:")
    arr = heap.get_data()
    n = len(arr)
    
    for i in range(n - 1, 0, -1):
        print(f"\n步骤 {n - i}: 交换堆顶 {arr[0]} 和 arr[{i}]={arr[i]}")
        arr[0], arr[i] = arr[i], arr[0]
        print(f"  交换后: {arr}")
        print(f"  对前 {i} 个元素进行堆化:")
        
        temp_heap = BinaryHeap(is_max_heap=True)
        temp_heap.build_heap(arr[:i])
        arr[:i] = temp_heap.get_data()
        print(f"  堆化后: {arr}")
    
    print(f"\n最终排序结果: {arr}")


# ==============================================================================
# 第七部分：主程序
# ==============================================================================

def main():
    """主程序入口"""
    print("="*70)
    print("               二叉堆排序算法详解与实现")
    print("="*70)
    
    print("\n【算法概述】")
    print("""
二叉堆是一种特殊的完全二叉树，具有以下特性：
- 大顶堆：每个节点的值 >= 其子节点的值
- 小顶堆：每个节点的值 <= 其子节点的值

堆排序利用堆的性质进行排序：
1. 建堆：O(n)时间将无序数组构建成堆
2. 排序：每次取出堆顶，重新堆化，共n-1次，每次O(log n)
3. 总时间复杂度：O(n log n)
4. 空间复杂度：O(1)（原地排序版本）
""")
    
    tester = HeapSortTester()
    tester.run_all_tests()
    
    test_binary_heap_operations()
    
    visualize_heap_process()
    
    performance_comparison()
    
    print("\n" + "="*70)
    print("                    程序执行完毕")
    print("="*70)


if __name__ == "__main__":
    main()
