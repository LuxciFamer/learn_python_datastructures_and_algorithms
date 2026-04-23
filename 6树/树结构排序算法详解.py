"""
================================================================================
                        树结构排序算法详解与实现
================================================================================

本文件系统地介绍并实现多种复杂的树结构排序算法，包括：
1. 二叉搜索树排序 (Binary Search Tree Sort)
2. 堆排序的树实现 (Heap Sort - Tree Implementation)
3. AVL树排序 (AVL Tree Sort - 自平衡二叉搜索树)

每种算法都包含完整的实现代码、原理说明、复杂度分析和测试用例。
================================================================================
"""

import random
import time
from typing import List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


# ==============================================================================
# 第一部分：树结构的基础定义
# ==============================================================================

class TreeNode:
    """
    树节点基础类
    
    树是由节点组成的非线性数据结构，具有以下特点：
    - 每个节点包含数据和指向子节点的引用
    - 树有一个根节点，根节点没有父节点
    - 除根节点外，每个节点有且只有一个父节点
    """
    
    def __init__(self, value: int):
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None
        self.height: int = 1  # 用于AVL树
    
    def __repr__(self):
        return f"TreeNode({self.value})"


class HeapType(Enum):
    MAX_HEAP = "max_heap"
    MIN_HEAP = "min_heap"


# ==============================================================================
# 第二部分：二叉搜索树排序 (Binary Search Tree Sort)
# ==============================================================================

class BinarySearchTree:
    """
    二叉搜索树排序
    
    【算法原理】
    二叉搜索树(BST)是一种特殊的二叉树，具有以下性质：
    1. 左子树所有节点的值小于根节点的值
    2. 右子树所有节点的值大于根节点的值
    3. 左右子树也分别是二叉搜索树
    
    排序过程：
    1. 将所有元素依次插入二叉搜索树
    2. 对树进行中序遍历，得到有序序列
    
    【时间复杂度】
    - 最好情况（平衡树）: O(n log n)
    - 平均情况: O(n log n)
    - 最坏情况（退化为链表）: O(n²)
    
    【空间复杂度】
    - O(n) - 需要存储n个节点
    
    【优缺点】
    优点：
    - 实现简单直观
    - 支持动态插入和删除
    - 可以高效地进行范围查询
    - 中序遍历天然有序
    
    缺点：
    - 最坏情况下退化为链表，效率低下
    - 对输入数据敏感，有序数据会导致性能下降
    - 需要额外的指针空间
    """
    
    def __init__(self):
        self.root: Optional[TreeNode] = None
        self.insert_count = 0
        self.compare_count = 0
    
    def insert(self, value: int) -> None:
        """插入值到二叉搜索树"""
        self.insert_count += 1
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: TreeNode, value: int) -> None:
        """递归插入辅助函数"""
        self.compare_count += 1
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)
    
    def inorder_traversal(self) -> List[int]:
        """中序遍历，返回有序列表"""
        result: List[int] = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[int]) -> None:
        """递归中序遍历辅助函数"""
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def get_height(self) -> int:
        """获取树的高度"""
        return self._get_height_recursive(self.root)
    
    def _get_height_recursive(self, node: Optional[TreeNode]) -> int:
        """递归计算树高度"""
        if node is None:
            return 0
        return 1 + max(
            self._get_height_recursive(node.left),
            self._get_height_recursive(node.right)
        )
    
    def clear(self) -> None:
        """清空树"""
        self.root = None
        self.insert_count = 0
        self.compare_count = 0


def binary_search_tree_sort(arr: List[int]) -> List[int]:
    """
    二叉搜索树排序主函数
    
    Args:
        arr: 待排序的整数列表
        
    Returns:
        排序后的整数列表
    """
    if not arr:
        return []
    
    bst = BinarySearchTree()
    for value in arr:
        bst.insert(value)
    
    return bst.inorder_traversal()


# ==============================================================================
# 第三部分：堆排序的树实现 (Heap Sort - Tree Implementation)
# ==============================================================================

class HeapTree:
    """
    堆排序的树实现
    
    【算法原理】
    堆是一种特殊的完全二叉树，具有以下性质：
    1. 大顶堆：每个节点的值都大于或等于其子节点的值
    2. 小顶堆：每个节点的值都小于或等于其子节点的值
    3. 堆是一棵完全二叉树，可以用数组高效存储
    
    排序过程（以大顶堆为例）：
    1. 将无序数组构建成大顶堆
    2. 将堆顶元素（最大值）与末尾元素交换
    3. 对剩余元素重新调整为堆
    4. 重复步骤2-3，直到所有元素有序
    
    【时间复杂度】
    - 最好情况: O(n log n)
    - 平均情况: O(n log n)
    - 最坏情况: O(n log n)
    
    【空间复杂度】
    - O(1) - 原地排序，仅需常数额外空间
    
    【优缺点】
    优点：
    - 时间复杂度稳定为O(n log n)
    - 原地排序，空间效率高
    - 适合处理大数据量
    - 对输入数据不敏感
    
    缺点：
    - 不稳定排序（相同元素的相对位置可能改变）
    - 无法利用数据的初始有序性
    - 随机访问效率不如数组实现的堆
    """
    
    def __init__(self, heap_type: HeapType = HeapType.MAX_HEAP):
        self.heap_type = heap_type
        self.data: List[int] = []
        self.compare_count = 0
        self.swap_count = 0
    
    def parent(self, index: int) -> int:
        """获取父节点索引"""
        return (index - 1) // 2
    
    def left_child(self, index: int) -> int:
        """获取左子节点索引"""
        return 2 * index + 1
    
    def right_child(self, index: int) -> int:
        """获取右子节点索引"""
        return 2 * index + 2
    
    def compare(self, a: int, b: int) -> bool:
        """比较函数，根据堆类型返回比较结果"""
        self.compare_count += 1
        if self.heap_type == HeapType.MAX_HEAP:
            return a > b
        else:
            return a < b
    
    def build_heap(self, arr: List[int]) -> None:
        """从数组构建堆"""
        self.data = arr.copy()
        n = len(self.data)
        
        # 从最后一个非叶子节点开始，自底向上调整
        for i in range(n // 2 - 1, -1, -1):
            self._heapify_down(i, n)
    
    def _heapify_down(self, index: int, size: int) -> None:
        """向下调整堆（堆化）"""
        target = index
        left = self.left_child(index)
        right = self.right_child(index)
        
        if left < size and self.compare(self.data[left], self.data[target]):
            target = left
        
        if right < size and self.compare(self.data[right], self.data[target]):
            target = right
        
        if target != index:
            self.data[index], self.data[target] = self.data[target], self.data[index]
            self.swap_count += 1
            self._heapify_down(target, size)
    
    def sort(self) -> List[int]:
        """堆排序主过程"""
        n = len(self.data)
        
        # 依次将堆顶元素与末尾元素交换，然后调整堆
        for i in range(n - 1, 0, -1):
            self.data[0], self.data[i] = self.data[i], self.data[0]
            self.swap_count += 1
            self._heapify_down(0, i)
        
        return self.data.copy()
    
    def get_tree_representation(self) -> str:
        """获取树的字符串表示（层序遍历）"""
        if not self.data:
            return "Empty Heap"
        
        result = []
        level = 0
        index = 0
        n = len(self.data)
        
        while index < n:
            level_size = 2 ** level
            level_nodes = []
            for _ in range(level_size):
                if index < n:
                    level_nodes.append(str(self.data[index]))
                    index += 1
                else:
                    break
            result.append("  " * (len(self.data) // (2 ** level)) + " ".join(level_nodes))
            level += 1
        
        return "\n".join(result)


def heap_sort(arr: List[int], ascending: bool = True) -> List[int]:
    """
    堆排序主函数
    
    Args:
        arr: 待排序的整数列表
        ascending: 是否升序排列（默认True）
        
    Returns:
        排序后的整数列表
    """
    if not arr:
        return []
    
    heap_type = HeapType.MAX_HEAP if ascending else HeapType.MIN_HEAP
    heap = HeapTree(heap_type)
    heap.build_heap(arr)
    return heap.sort()


# ==============================================================================
# 第四部分：AVL树排序 (AVL Tree Sort - 自平衡二叉搜索树)
# ==============================================================================

class AVLTree:
    """
    AVL树排序
    
    【算法原理】
    AVL树是最早发明的自平衡二叉搜索树，具有以下性质：
    1. 满足二叉搜索树的所有性质
    2. 任何节点的左右子树高度差的绝对值不超过1
    3. 通过旋转操作保持平衡
    
    平衡因子 = 左子树高度 - 右子树高度
    
    四种旋转情况：
    1. LL型（左左）：右旋
    2. RR型（右右）：左旋
    3. LR型（左右）：先左旋后右旋
    4. RL型（右左）：先右旋后左旋
    
    【时间复杂度】
    - 最好情况: O(n log n)
    - 平均情况: O(n log n)
    - 最坏情况: O(n log n) - 保证平衡
    
    【空间复杂度】
    - O(n) - 需要存储n个节点
    
    【优缺点】
    优点：
    - 保证O(n log n)的时间复杂度
    - 不会退化为链表
    - 适合频繁插入删除的场景
    - 查找效率稳定
    
    缺点：
    - 实现复杂，需要维护平衡
    - 插入和删除需要额外的旋转操作
    - 常数因子较大
    - 需要存储高度信息
    """
    
    def __init__(self):
        self.root: Optional[TreeNode] = None
        self.rotation_count = 0
        self.compare_count = 0
    
    def get_height(self, node: Optional[TreeNode]) -> int:
        """获取节点高度"""
        if node is None:
            return 0
        return node.height
    
    def get_balance(self, node: Optional[TreeNode]) -> int:
        """获取平衡因子"""
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node: TreeNode) -> None:
        """更新节点高度"""
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
    
    def right_rotate(self, y: TreeNode) -> TreeNode:
        """右旋操作"""
        self.rotation_count += 1
        x = y.left
        T2 = x.right
        
        x.right = y
        y.left = T2
        
        self.update_height(y)
        self.update_height(x)
        
        return x
    
    def left_rotate(self, x: TreeNode) -> TreeNode:
        """左旋操作"""
        self.rotation_count += 1
        y = x.right
        T2 = y.left
        
        y.left = x
        x.right = T2
        
        self.update_height(x)
        self.update_height(y)
        
        return y
    
    def insert(self, value: int) -> None:
        """插入值到AVL树"""
        self.root = self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node: Optional[TreeNode], value: int) -> TreeNode:
        """递归插入并保持平衡"""
        if node is None:
            return TreeNode(value)
        
        self.compare_count += 1
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        else:
            node.right = self._insert_recursive(node.right, value)
        
        self.update_height(node)
        
        balance = self.get_balance(node)
        
        # LL型
        if balance > 1 and value < node.left.value:
            return self.right_rotate(node)
        
        # RR型
        if balance < -1 and value > node.right.value:
            return self.left_rotate(node)
        
        # LR型
        if balance > 1 and value > node.left.value:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # RL型
        if balance < -1 and value < node.right.value:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node
    
    def inorder_traversal(self) -> List[int]:
        """中序遍历"""
        result: List[int] = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[TreeNode], result: List[int]) -> None:
        """递归中序遍历"""
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def clear(self) -> None:
        """清空树"""
        self.root = None
        self.rotation_count = 0
        self.compare_count = 0


def avl_tree_sort(arr: List[int]) -> List[int]:
    """
    AVL树排序主函数
    
    Args:
        arr: 待排序的整数列表
        
    Returns:
        排序后的整数列表
    """
    if not arr:
        return []
    
    avl = AVLTree()
    for value in arr:
        avl.insert(value)
    
    return avl.inorder_traversal()


# ==============================================================================
# 第五部分：算法对比与测试框架
# ==============================================================================

@dataclass
class SortResult:
    """排序结果数据类"""
    algorithm_name: str
    sorted_data: List[int]
    time_elapsed: float
    comparisons: int
    swaps_or_rotations: int
    tree_height: int
    is_correct: bool


class TreeSortComparator:
    """
    树排序算法对比器
    
    提供统一的测试框架，用于比较不同树排序算法的性能
    """
    
    def __init__(self):
        self.results: List[SortResult] = []
    
    def generate_test_data(self, size: int, data_type: str) -> List[int]:
        """
        生成不同类型的测试数据
        
        Args:
            size: 数据大小
            data_type: 数据类型 ('random', 'sorted', 'reverse', 'nearly_sorted')
            
        Returns:
            生成的测试数据列表
        """
        if data_type == 'random':
            return [random.randint(1, size * 10) for _ in range(size)]
        elif data_type == 'sorted':
            return list(range(1, size + 1))
        elif data_type == 'reverse':
            return list(range(size, 0, -1))
        elif data_type == 'nearly_sorted':
            arr = list(range(1, size + 1))
            # 随机交换一些元素
            swap_count = size // 10
            for _ in range(swap_count):
                i, j = random.randint(0, size - 1), random.randint(0, size - 1)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        else:
            return [random.randint(1, size * 10) for _ in range(size)]
    
    def test_algorithm(
        self, 
        name: str, 
        sort_func: Callable[[List[int]], List[int]], 
        data: List[int]
    ) -> SortResult:
        """
        测试单个排序算法
        
        Args:
            name: 算法名称
            sort_func: 排序函数
            data: 测试数据
            
        Returns:
            排序结果
        """
        data_copy = data.copy()
        
        start_time = time.perf_counter()
        sorted_data = sort_func(data_copy)
        end_time = time.perf_counter()
        
        is_correct = self._verify_sorted(sorted_data)
        
        return SortResult(
            algorithm_name=name,
            sorted_data=sorted_data,
            time_elapsed=end_time - start_time,
            comparisons=0,
            swaps_or_rotations=0,
            tree_height=0,
            is_correct=is_correct
        )
    
    def _verify_sorted(self, arr: List[int]) -> bool:
        """验证数组是否已排序"""
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    
    def compare_all_algorithms(self, data: List[int], data_type: str) -> None:
        """
        对比所有树排序算法
        
        Args:
            data: 测试数据
            data_type: 数据类型描述
        """
        print(f"\n{'='*70}")
        print(f"测试数据类型: {data_type}, 数据量: {len(data)}")
        print(f"{'='*70}")
        
        algorithms = [
            ("二叉搜索树排序", binary_search_tree_sort),
            ("堆排序(树实现)", heap_sort),
            ("AVL树排序", avl_tree_sort),
        ]
        
        results = []
        for name, func in algorithms:
            result = self.test_algorithm(name, func, data)
            results.append(result)
            self._print_result(result)
        
        self._print_comparison_table(results)
    
    def _print_result(self, result: SortResult) -> None:
        """打印单个结果"""
        status = "[OK] 正确" if result.is_correct else "[X] 错误"
        print(f"\n{result.algorithm_name}:")
        print(f"  状态: {status}")
        print(f"  耗时: {result.time_elapsed:.6f} 秒")
        if len(result.sorted_data) <= 20:
            print(f"  结果: {result.sorted_data}")
        else:
            print(f"  结果(前10个): {result.sorted_data[:10]}...")
    
    def _print_comparison_table(self, results: List[SortResult]) -> None:
        """打印对比表格"""
        print(f"\n{'-'*70}")
        print("性能对比表:")
        print(f"{'-'*70}")
        print(f"{'算法名称':<20} {'耗时(秒)':<15} {'正确性':<10}")
        print(f"{'-'*70}")
        
        for result in sorted(results, key=lambda x: x.time_elapsed):
            status = "[OK]" if result.is_correct else "[X]"
            print(f"{result.algorithm_name:<20} {result.time_elapsed:<15.6f} {status:<10}")


def print_algorithm_summary():
    """打印算法总结对比表"""
    print("\n" + "="*70)
    print("树排序算法综合对比")
    print("="*70)
    
    print("\n" + "-"*70)
    print("|       算法名称       |  时间复杂度  |  空间复杂度  |   稳定性  |         特点                   |")
    print("-"*70)
    print("| 二叉搜索树排序      | O(n log n)   | O(n)         | 稳定      | 实现简单，但可能退化为链表     |")
    print("| (BST Sort)          | ~ O(n^2)     |              |           | 支持动态操作                   |")
    print("-"*70)
    print("| 堆排序              | O(n log n)   | O(1)         | 不稳定    | 时间复杂度稳定，原地排序       |")
    print("| (Heap Sort)         |              |              |           | 空间效率最高                   |")
    print("-"*70)
    print("| AVL树排序           | O(n log n)   | O(n)         | 稳定      | 保证平衡，性能稳定             |")
    print("| (AVL Tree Sort)     |              |              |           | 实现复杂，适合动态场景         |")
    print("-"*70)
    
    print("\n【选择建议】")
    print("  - 数据量小且需要简单实现 -> 二叉搜索树排序")
    print("  - 数据量大且内存受限 -> 堆排序")
    print("  - 需要稳定的O(n log n)性能 -> AVL树排序")
    print("  - 需要频繁插入删除操作 -> AVL树排序")


# ==============================================================================
# 第六部分：可视化树结构
# ==============================================================================

def print_tree_visual(node: Optional[TreeNode], prefix: str = "", is_left: bool = True) -> None:
    """
    可视化打印树结构
    
    Args:
        node: 树节点
        prefix: 前缀字符串
        is_left: 是否是左子节点
    """
    if node is not None:
        print_tree_visual(node.right, prefix + ("|   " if is_left else "    "), False)
        print(prefix + ("\\-- " if is_left else "/-- ") + str(node.value))
        print_tree_visual(node.left, prefix + ("    " if is_left else "|   "), True)


def demonstrate_tree_structure():
    """演示树结构的构建过程"""
    print("\n" + "="*70)
    print("树结构构建演示")
    print("="*70)
    
    test_data = [50, 30, 70, 20, 40, 60, 80]
    
    print(f"\n插入数据: {test_data}")
    
    print("\n【二叉搜索树构建过程】")
    bst = BinarySearchTree()
    for value in test_data:
        bst.insert(value)
        print(f"  插入 {value} 后，树高度: {bst.get_height()}")
    
    print("\n二叉搜索树结构:")
    print_tree_visual(bst.root)
    
    print("\n【AVL树构建过程】")
    avl = AVLTree()
    for value in test_data:
        avl.insert(value)
        print(f"  插入 {value} 后，树高度: {avl.get_height(avl.root)}, 旋转次数: {avl.rotation_count}")
    
    print("\nAVL树结构:")
    print_tree_visual(avl.root)
    
    print("\n【堆的树结构】")
    heap = HeapTree(HeapType.MAX_HEAP)
    heap.build_heap(test_data)
    print(f"\n大顶堆数组表示: {heap.data}")
    print("\n堆的树形表示:")
    print(heap.get_tree_representation())


# ==============================================================================
# 第七部分：主程序与测试
# ==============================================================================

def main():
    """主程序入口"""
    print("="*70)
    print("               树结构排序算法详解与实现")
    print("="*70)
    
    print_algorithm_summary()
    
    demonstrate_tree_structure()
    
    comparator = TreeSortComparator()
    
    test_configs = [
        (100, 'random', '随机数据'),
        (100, 'sorted', '有序数据'),
        (100, 'reverse', '逆序数据'),
        (100, 'nearly_sorted', '近乎有序数据'),
    ]
    
    print("\n" + "="*70)
    print("                    算法性能测试")
    print("="*70)
    
    for size, data_type, desc in test_configs:
        data = comparator.generate_test_data(size, data_type)
        comparator.compare_all_algorithms(data, desc)
    
    print("\n" + "="*70)
    print("                    小规模数据演示")
    print("="*70)
    
    small_data = [64, 34, 25, 12, 22, 11, 90]
    print(f"\n原始数据: {small_data}")
    
    print(f"\n二叉搜索树排序结果: {binary_search_tree_sort(small_data)}")
    print(f"堆排序结果: {heap_sort(small_data)}")
    print(f"AVL树排序结果: {avl_tree_sort(small_data)}")
    
    print("\n" + "="*70)
    print("                    测试完成")
    print("="*70)


if __name__ == "__main__":
    main()
