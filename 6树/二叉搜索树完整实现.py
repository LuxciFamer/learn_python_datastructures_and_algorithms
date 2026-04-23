"""
================================================================================
                    二叉搜索树(BST)完整实现 - 含AVL平衡机制
================================================================================

本文件实现了一个功能完整的二叉搜索树数据结构，包含：
1. 基础操作：插入、删除、查找
2. AVL自平衡机制：确保操作时间复杂度为O(log n)
3. 四种遍历方式：前序、中序、后序、层序
4. 辅助功能：高度、节点数、最值、平衡检查等
5. 完整的类型注解和错误处理

二叉搜索树性质：
- 左子树所有节点值 < 根节点值 < 右子树所有节点值
- 中序遍历结果为有序序列

AVL树性质：
- 在BST基础上，任何节点的左右子树高度差不超过1
- 通过旋转操作维持平衡
================================================================================
"""

from typing import Optional, List, Callable, TypeVar, Generic, Iterator, Any
from dataclasses import dataclass
from enum import Enum, auto
from collections import deque
import random
import time

T = TypeVar('T')


# ==============================================================================
# 第一部分：枚举和异常定义
# ==============================================================================

class TraversalType(Enum):
    """遍历类型枚举"""
    PREORDER = auto()      # 前序遍历：根-左-右
    INORDER = auto()       # 中序遍历：左-根-右
    POSTORDER = auto()     # 后序遍历：左-右-根
    LEVEL_ORDER = auto()   # 层序遍历：广度优先


class RotationType(Enum):
    """旋转类型枚举"""
    LEFT = auto()          # 左旋
    RIGHT = auto()         # 右旋
    LEFT_RIGHT = auto()    # 左右旋（先左后右）
    RIGHT_LEFT = auto()    # 右左旋（先右后左）


class BSTError(Exception):
    """二叉搜索树基础异常"""
    pass


class NodeNotFoundError(BSTError):
    """节点未找到异常"""
    pass


class EmptyTreeError(BSTError):
    """空树操作异常"""
    pass


class DuplicateKeyError(BSTError):
    """重复键异常"""
    pass


# ==============================================================================
# 第二部分：节点类定义
# ==============================================================================

@dataclass
class TreeNode(Generic[T]):
    """
    树节点类
    
    使用dataclass简化节点定义，包含：
    - value: 节点存储的值
    - left: 左子节点引用
    - right: 右子节点引用
    - height: 节点高度（用于AVL平衡）
    - parent: 父节点引用（便于某些操作）
    
    内存优化考虑：
    - 使用__slots__可以进一步减少内存占用
    - 对于大规模数据，可考虑使用数组存储节点
    """
    value: T
    left: Optional['TreeNode[T]'] = None
    right: Optional['TreeNode[T]'] = None
    height: int = 1
    parent: Optional['TreeNode[T]'] = None
    
    def __repr__(self) -> str:
        return f"TreeNode({self.value}, h={self.height})"
    
    def update_height(self) -> None:
        """更新节点高度"""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = 1 + max(left_height, right_height)
    
    def get_balance_factor(self) -> int:
        """
        获取平衡因子
        
        平衡因子 = 左子树高度 - 右子树高度
        AVL树要求：|平衡因子| <= 1
        
        Returns:
            平衡因子值
        """
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height
    
    def is_leaf(self) -> bool:
        """判断是否为叶子节点"""
        return self.left is None and self.right is None
    
    def has_one_child(self) -> bool:
        """判断是否只有一个子节点"""
        return (self.left is None) != (self.right is None)
    
    def has_two_children(self) -> bool:
        """判断是否有两个子节点"""
        return self.left is not None and self.right is not None
    
    def get_only_child(self) -> Optional['TreeNode[T]']:
        """获取唯一子节点"""
        if self.left:
            return self.left
        return self.right


# ==============================================================================
# 第三部分：基础二叉搜索树实现
# ==============================================================================

class BinarySearchTree(Generic[T]):
    """
    二叉搜索树基础实现
    
    【核心性质】
    对于任意节点N：
    - N的左子树中所有节点的值 < N的值
    - N的右子树中所有节点的值 > N的值
    
    【时间复杂度】
    - 平均情况：查找/插入/删除 O(log n)
    - 最坏情况（退化为链表）：O(n)
    
    【空间复杂度】
    - O(n) 存储n个节点
    
    【应用场景】
    - 数据库索引
    - 符号表实现
    - 范围查询
    - 排序（中序遍历）
    """
    
    def __init__(self, allow_duplicates: bool = False):
        """
        初始化二叉搜索树
        
        Args:
            allow_duplicates: 是否允许重复值
        """
        self._root: Optional[TreeNode[T]] = None
        self._size: int = 0
        self._allow_duplicates = allow_duplicates
        self._compare_count: int = 0
    
    @property
    def size(self) -> int:
        """获取树中节点数量"""
        return self._size
    
    @property
    def is_empty(self) -> bool:
        """判断树是否为空"""
        return self._root is None
    
    @property
    def root(self) -> Optional[TreeNode[T]]:
        """获取根节点"""
        return self._root
    
    def __len__(self) -> int:
        """支持len()函数"""
        return self._size
    
    def __bool__(self) -> bool:
        """支持布尔判断"""
        return self._size > 0
    
    def __contains__(self, value: T) -> bool:
        """支持in操作符"""
        return self.search(value) is not None
    
    def __iter__(self) -> Iterator[T]:
        """支持迭代，默认中序遍历"""
        return iter(self.traverse(TraversalType.INORDER))
    
    def __repr__(self) -> str:
        """树的字符串表示"""
        if self.is_empty:
            return "BinarySearchTree(empty)"
        return f"BinarySearchTree(size={self._size}, height={self.get_height()})"
    
    # =========================================================================
    # 基础操作：查找
    # =========================================================================
    
    def search(self, value: T) -> Optional[TreeNode[T]]:
        """
        查找指定值的节点
        
        查找过程：
        1. 从根节点开始
        2. 如果目标值等于当前节点值，返回当前节点
        3. 如果目标值小于当前节点值，在左子树中继续查找
        4. 如果目标值大于当前节点值，在右子树中继续查找
        5. 如果到达空节点，说明值不存在
        
        时间复杂度：O(log n) 平均，O(n) 最坏
        
        Args:
            value: 要查找的值
            
        Returns:
            找到的节点，如果不存在返回None
        """
        return self._search_recursive(self._root, value)
    
    def _search_recursive(
        self, 
        node: Optional[TreeNode[T]], 
        value: T
    ) -> Optional[TreeNode[T]]:
        """递归查找实现"""
        if node is None:
            return None
        
        self._compare_count += 1
        
        if value == node.value:
            return node
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def search_iterative(self, value: T) -> Optional[TreeNode[T]]:
        """
        迭代方式查找（避免递归栈开销）
        
        对于深度较大的树，迭代方式更安全
        
        Args:
            value: 要查找的值
            
        Returns:
            找到的节点，如果不存在返回None
        """
        current = self._root
        
        while current is not None:
            self._compare_count += 1
            
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        
        return None
    
    def contains(self, value: T) -> bool:
        """判断值是否存在"""
        return self.search(value) is not None
    
    # =========================================================================
    # 基础操作：插入
    # =========================================================================
    
    def insert(self, value: T) -> TreeNode[T]:
        """
        插入新节点
        
        插入过程：
        1. 如果树为空，新节点成为根节点
        2. 从根节点开始比较
        3. 如果值小于当前节点，向左子树移动
        4. 如果值大于当前节点，向右子树移动
        5. 找到空位置后插入新节点
        
        时间复杂度：O(log n) 平均，O(n) 最坏
        
        Args:
            value: 要插入的值
            
        Returns:
            新插入的节点
            
        Raises:
            DuplicateKeyError: 当不允许重复且值已存在时
        """
        if self._root is None:
            self._root = TreeNode(value)
            self._size += 1
            return self._root
        
        return self._insert_recursive(self._root, value)
    
    def _insert_recursive(
        self, 
        node: TreeNode[T], 
        value: T
    ) -> TreeNode[T]:
        """递归插入实现"""
        self._compare_count += 1
        
        if value == node.value:
            if not self._allow_duplicates:
                raise DuplicateKeyError(f"值 {value} 已存在于树中")
            if node.right is None:
                new_node = TreeNode(value, parent=node)
                node.right = new_node
                self._size += 1
                return new_node
            return self._insert_recursive(node.right, value)
        
        if value < node.value:
            if node.left is None:
                new_node = TreeNode(value, parent=node)
                node.left = new_node
                self._size += 1
                return new_node
            return self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                new_node = TreeNode(value, parent=node)
                node.right = new_node
                self._size += 1
                return new_node
            return self._insert_recursive(node.right, value)
    
    def insert_iterative(self, value: T) -> TreeNode[T]:
        """
        迭代方式插入
        
        Args:
            value: 要插入的值
            
        Returns:
            新插入的节点
        """
        if self._root is None:
            self._root = TreeNode(value)
            self._size += 1
            return self._root
        
        current = self._root
        parent = None
        is_left = False
        
        while current is not None:
            parent = current
            self._compare_count += 1
            
            if value == current.value:
                if not self._allow_duplicates:
                    raise DuplicateKeyError(f"值 {value} 已存在")
                current = current.right
                is_left = False
            elif value < current.value:
                current = current.left
                is_left = True
            else:
                current = current.right
                is_left = False
        
        new_node = TreeNode(value, parent=parent)
        
        if is_left:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._size += 1
        return new_node
    
    # =========================================================================
    # 基础操作：删除
    # =========================================================================
    
    def delete(self, value: T) -> bool:
        """
        删除指定值的节点
        
        删除分三种情况：
        
        情况1：删除叶子节点
        - 直接删除，更新父节点引用
        
        情况2：删除只有一个子节点的节点
        - 用子节点替换被删除节点
        
        情况3：删除有两个子节点的节点
        - 找到中序后继（右子树的最小值）
        - 用中序后继的值替换被删除节点的值
        - 删除中序后继节点
        
        时间复杂度：O(log n) 平均，O(n) 最坏
        
        Args:
            value: 要删除的值
            
        Returns:
            删除成功返回True，节点不存在返回False
        """
        node = self.search(value)
        if node is None:
            return False
        
        self._delete_node(node)
        self._size -= 1
        return True
    
    def _delete_node(self, node: TreeNode[T]) -> None:
        """
        删除节点的内部实现
        
        Args:
            node: 要删除的节点
        """
        if node.is_leaf():
            self._delete_leaf(node)
        elif node.has_one_child():
            self._delete_one_child_node(node)
        else:
            self._delete_two_children_node(node)
    
    def _delete_leaf(self, node: TreeNode[T]) -> None:
        """删除叶子节点"""
        if node is self._root:
            self._root = None
        elif node.parent.left is node:
            node.parent.left = None
        else:
            node.parent.right = None
    
    def _delete_one_child_node(self, node: TreeNode[T]) -> None:
        """删除只有一个子节点的节点"""
        child = node.get_only_child()
        
        if node is self._root:
            self._root = child
            if child:
                child.parent = None
        else:
            if node.parent.left is node:
                node.parent.left = child
            else:
                node.parent.right = child
            
            if child:
                child.parent = node.parent
    
    def _delete_two_children_node(self, node: TreeNode[T]) -> None:
        """
        删除有两个子节点的节点
        
        策略：用中序后继替换
        中序后继 = 右子树中的最小节点
        """
        successor = self._find_min_node(node.right)
        node.value = successor.value
        self._delete_node(successor)
    
    def _find_min_node(self, node: Optional[TreeNode[T]]) -> TreeNode[T]:
        """找到子树中的最小节点"""
        if node is None:
            raise EmptyTreeError("无法在空子树中查找最小节点")
        
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def _find_max_node(self, node: Optional[TreeNode[T]]) -> TreeNode[T]:
        """找到子树中的最大节点"""
        if node is None:
            raise EmptyTreeError("无法在空子树中查找最大节点")
        
        current = node
        while current.right is not None:
            current = current.right
        return current
    
    # =========================================================================
    # 最值查询
    # =========================================================================
    
    def find_min(self) -> T:
        """
        查找最小值
        
        最小值在最左边的节点
        
        Returns:
            树中的最小值
            
        Raises:
            EmptyTreeError: 树为空时
        """
        if self.is_empty:
            raise EmptyTreeError("无法在空树中查找最小值")
        
        return self._find_min_node(self._root).value
    
    def find_max(self) -> T:
        """
        查找最大值
        
        最大值在最右边的节点
        
        Returns:
            树中的最大值
            
        Raises:
            EmptyTreeError: 树为空时
        """
        if self.is_empty:
            raise EmptyTreeError("无法在空树中查找最大值")
        
        return self._find_max_node(self._root).value
    
    # =========================================================================
    # 遍历操作
    # =========================================================================
    
    def traverse(self, traversal_type: TraversalType) -> List[T]:
        """
        执行指定类型的遍历
        
        Args:
            traversal_type: 遍历类型
            
        Returns:
            遍历结果列表
        """
        if self.is_empty:
            return []
        
        if traversal_type == TraversalType.PREORDER:
            return self._preorder_traversal()
        elif traversal_type == TraversalType.INORDER:
            return self._inorder_traversal()
        elif traversal_type == TraversalType.POSTORDER:
            return self._postorder_traversal()
        elif traversal_type == TraversalType.LEVEL_ORDER:
            return self._level_order_traversal()
        else:
            raise ValueError(f"未知的遍历类型: {traversal_type}")
    
    def _preorder_traversal(self) -> List[T]:
        """
        前序遍历：根-左-右
        
        应用场景：
        - 复制树结构
        - 前缀表达式
        - 序列化树
        """
        result: List[T] = []
        self._preorder_recursive(self._root, result)
        return result
    
    def _preorder_recursive(
        self, 
        node: Optional[TreeNode[T]], 
        result: List[T]
    ) -> None:
        """前序遍历递归实现"""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def _inorder_traversal(self) -> List[T]:
        """
        中序遍历：左-根-右
        
        应用场景：
        - 获取有序序列
        - 二叉搜索树的排序输出
        - 范围查询
        """
        result: List[T] = []
        self._inorder_recursive(self._root, result)
        return result
    
    def _inorder_recursive(
        self, 
        node: Optional[TreeNode[T]], 
        result: List[T]
    ) -> None:
        """中序遍历递归实现"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def _postorder_traversal(self) -> List[T]:
        """
        后序遍历：左-右-根
        
        应用场景：
        - 删除树（先删子节点再删根）
        - 计算目录大小
        - 后缀表达式
        """
        result: List[T] = []
        self._postorder_recursive(self._root, result)
        return result
    
    def _postorder_recursive(
        self, 
        node: Optional[TreeNode[T]], 
        result: List[T]
    ) -> None:
        """后序遍历递归实现"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def _level_order_traversal(self) -> List[T]:
        """
        层序遍历（广度优先）
        
        应用场景：
        - 按层打印树
        - 查找最近节点
        - 序列化/反序列化
        """
        if self._root is None:
            return []
        
        result: List[T] = []
        queue: deque[TreeNode[T]] = deque([self._root])
        
        while queue:
            node = queue.popleft()
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    
    # =========================================================================
    # 辅助功能
    # =========================================================================
    
    def get_height(self) -> int:
        """
        获取树的高度
        
        高度定义：从根到最远叶子节点的边数
        空树高度为0，单节点树高度为1
        
        Returns:
            树的高度
        """
        return self._get_height_recursive(self._root)
    
    def _get_height_recursive(self, node: Optional[TreeNode[T]]) -> int:
        """递归计算高度"""
        if node is None:
            return 0
        return 1 + max(
            self._get_height_recursive(node.left),
            self._get_height_recursive(node.right)
        )
    
    def get_depth(self, value: T) -> int:
        """
        获取指定值节点的深度
        
        深度定义：从根到该节点的边数
        
        Args:
            value: 目标值
            
        Returns:
            节点深度，如果节点不存在返回-1
        """
        node = self.search(value)
        if node is None:
            return -1
        
        depth = 0
        current = node
        while current.parent:
            depth += 1
            current = current.parent
        
        return depth
    
    def is_balanced(self) -> bool:
        """
        检查树是否平衡
        
        平衡定义：对于每个节点，左右子树高度差不超过1
        
        Returns:
            是否平衡
        """
        return self._check_balanced(self._root) != -1
    
    def _check_balanced(self, node: Optional[TreeNode[T]]) -> int:
        """
        检查平衡并返回高度
        
        Returns:
            子树高度，如果不平衡返回-1
        """
        if node is None:
            return 0
        
        left_height = self._check_balanced(node.left)
        if left_height == -1:
            return -1
        
        right_height = self._check_balanced(node.right)
        if right_height == -1:
            return -1
        
        if abs(left_height - right_height) > 1:
            return -1
        
        return 1 + max(left_height, right_height)
    
    def get_leaf_count(self) -> int:
        """获取叶子节点数量"""
        return self._count_leaves(self._root)
    
    def _count_leaves(self, node: Optional[TreeNode[T]]) -> int:
        """递归计算叶子节点"""
        if node is None:
            return 0
        if node.is_leaf():
            return 1
        return self._count_leaves(node.left) + self._count_leaves(node.right)
    
    def get_node_count_at_level(self, level: int) -> int:
        """
        获取指定层级的节点数量
        
        Args:
            level: 层级（从0开始）
            
        Returns:
            该层级的节点数量
        """
        if level < 0 or self.is_empty:
            return 0
        
        return self._count_nodes_at_level(self._root, level, 0)
    
    def _count_nodes_at_level(
        self, 
        node: Optional[TreeNode[T]], 
        target_level: int, 
        current_level: int
    ) -> int:
        """递归计算指定层级节点数"""
        if node is None:
            return 0
        
        if current_level == target_level:
            return 1
        
        return (
            self._count_nodes_at_level(node.left, target_level, current_level + 1) +
            self._count_nodes_at_level(node.right, target_level, current_level + 1)
        )
    
    def range_query(self, low: T, high: T) -> List[T]:
        """
        范围查询：查找值在[low, high]范围内的所有节点
        
        利用BST性质进行高效查询
        
        Args:
            low: 范围下界
            high: 范围上界
            
        Returns:
            范围内的值列表（有序）
        """
        result: List[T] = []
        self._range_query_recursive(self._root, low, high, result)
        return result
    
    def _range_query_recursive(
        self,
        node: Optional[TreeNode[T]],
        low: T,
        high: T,
        result: List[T]
    ) -> None:
        """范围查询递归实现"""
        if node is None:
            return
        
        if low <= node.value <= high:
            self._range_query_recursive(node.left, low, high, result)
            result.append(node.value)
            self._range_query_recursive(node.right, low, high, result)
        elif node.value < low:
            self._range_query_recursive(node.right, low, high, result)
        else:
            self._range_query_recursive(node.left, low, high, result)
    
    def clear(self) -> None:
        """清空树"""
        self._root = None
        self._size = 0
        self._compare_count = 0
    
    def get_statistics(self) -> dict:
        """获取树的统计信息"""
        return {
            'size': self._size,
            'height': self.get_height(),
            'is_balanced': self.is_balanced(),
            'leaf_count': self.get_leaf_count(),
            'compare_count': self._compare_count
        }


# ==============================================================================
# 第四部分：AVL树实现（自平衡二叉搜索树）
# ==============================================================================

class AVLTree(BinarySearchTree[T]):
    """
    AVL树 - 自平衡二叉搜索树
    
    【AVL树性质】
    1. 满足BST的所有性质
    2. 任何节点的左右子树高度差（平衡因子）的绝对值不超过1
    3. 通过旋转操作维持平衡
    
    【平衡因子】
    BF = 左子树高度 - 右子树高度
    - BF > 1: 左子树过高，需要右旋
    - BF < -1: 右子树过高，需要左旋
    
    【四种旋转情况】
    1. LL型（左左）：在左子树的左子树插入 -> 右旋
    2. RR型（右右）：在右子树的右子树插入 -> 左旋
    3. LR型（左右）：在左子树的右子树插入 -> 先左旋后右旋
    4. RL型（右左）：在右子树的左子树插入 -> 先右旋后左旋
    
    【时间复杂度】
    - 查找/插入/删除：O(log n) 保证
    
    【空间复杂度】
    - O(n) 存储节点
    - 每个节点额外存储高度信息
    """
    
    def __init__(self, allow_duplicates: bool = False):
        """初始化AVL树"""
        super().__init__(allow_duplicates)
        self._rotation_count: int = 0
    
    @property
    def rotation_count(self) -> int:
        """获取旋转操作次数"""
        return self._rotation_count
    
    # =========================================================================
    # 重写插入操作
    # =========================================================================
    
    def insert(self, value: T) -> TreeNode[T]:
        """
        插入节点并保持平衡
        
        插入后从插入点向上检查平衡因子，
        如果发现不平衡则进行相应的旋转操作
        
        Args:
            value: 要插入的值
            
        Returns:
            新插入的节点
        """
        self._root = self._insert_avl(self._root, value)
        self._size += 1
        return self.search(value)
    
    def _insert_avl(
        self, 
        node: Optional[TreeNode[T]], 
        value: T
    ) -> TreeNode[T]:
        """AVL插入递归实现"""
        if node is None:
            return TreeNode(value)
        
        self._compare_count += 1
        
        if value < node.value:
            node.left = self._insert_avl(node.left, value)
            if node.left:
                node.left.parent = node
        elif value > node.value:
            node.right = self._insert_avl(node.right, value)
            if node.right:
                node.right.parent = node
        else:
            if not self._allow_duplicates:
                raise DuplicateKeyError(f"值 {value} 已存在")
            node.right = self._insert_avl(node.right, value)
            if node.right:
                node.right.parent = node
        
        node.update_height()
        
        return self._rebalance(node)
    
    # =========================================================================
    # 重写删除操作
    # =========================================================================
    
    def delete(self, value: T) -> bool:
        """
        删除节点并保持平衡
        
        Args:
            value: 要删除的值
            
        Returns:
            删除成功返回True
        """
        if self.search(value) is None:
            return False
        
        self._root = self._delete_avl(self._root, value)
        self._size -= 1
        return True
    
    def _delete_avl(
        self, 
        node: Optional[TreeNode[T]], 
        value: T
    ) -> Optional[TreeNode[T]]:
        """AVL删除递归实现"""
        if node is None:
            return None
        
        self._compare_count += 1
        
        if value < node.value:
            node.left = self._delete_avl(node.left, value)
            if node.left:
                node.left.parent = node
        elif value > node.value:
            node.right = self._delete_avl(node.right, value)
            if node.right:
                node.right.parent = node
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self._find_min_node(node.right)
                node.value = successor.value
                node.right = self._delete_avl(node.right, successor.value)
                if node.right:
                    node.right.parent = node
        
        node.update_height()
        return self._rebalance(node)
    
    # =========================================================================
    # 平衡操作
    # =========================================================================
    
    def _rebalance(self, node: TreeNode[T]) -> TreeNode[T]:
        """
        重新平衡节点
        
        根据平衡因子判断需要进行的旋转类型
        
        Args:
            node: 需要平衡的节点
            
        Returns:
            平衡后的子树根节点
        """
        balance_factor = node.get_balance_factor()
        
        if balance_factor > 1:
            if node.left and node.left.get_balance_factor() >= 0:
                return self._rotate_right(node)
            else:
                return self._rotate_left_right(node)
        
        if balance_factor < -1:
            if node.right and node.right.get_balance_factor() <= 0:
                return self._rotate_left(node)
            else:
                return self._rotate_right_left(node)
        
        return node
    
    def _rotate_left(self, z: TreeNode[T]) -> TreeNode[T]:
        """
        左旋操作
        
        用于RR型不平衡
        
        旋转前：          旋转后：
            z                 y
             \\               / \\
              y     ->      z   T3
             / \\             \\
            T2  T3           T2
        
        Args:
            z: 旋转中心节点
            
        Returns:
            旋转后的新根节点
        """
        self._rotation_count += 1
        
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        if T2:
            T2.parent = z
        
        y.parent = z.parent
        z.parent = y
        
        z.update_height()
        y.update_height()
        
        return y
    
    def _rotate_right(self, z: TreeNode[T]) -> TreeNode[T]:
        """
        右旋操作
        
        用于LL型不平衡
        
        旋转前：          旋转后：
              z             y
             /             / \\
            y       ->    T1  z
           / \\               /
          T1  T2           T2
        
        Args:
            z: 旋转中心节点
            
        Returns:
            旋转后的新根节点
        """
        self._rotation_count += 1
        
        y = z.left
        T2 = y.right
        
        y.right = z
        z.left = T2
        
        if T2:
            T2.parent = z
        
        y.parent = z.parent
        z.parent = y
        
        z.update_height()
        y.update_height()
        
        return y
    
    def _rotate_left_right(self, z: TreeNode[T]) -> TreeNode[T]:
        """
        左右旋（先左旋后右旋）
        
        用于LR型不平衡
        
        Args:
            z: 旋转中心节点
            
        Returns:
            旋转后的新根节点
        """
        z.left = self._rotate_left(z.left)
        if z.left:
            z.left.parent = z
        return self._rotate_right(z)
    
    def _rotate_right_left(self, z: TreeNode[T]) -> TreeNode[T]:
        """
        右左旋（先右旋后左旋）
        
        用于RL型不平衡
        
        Args:
            z: 旋转中心节点
            
        Returns:
            旋转后的新根节点
        """
        z.right = self._rotate_right(z.right)
        if z.right:
            z.right.parent = z
        return self._rotate_left(z)
    
    def get_rotation_type(self, node: TreeNode[T]) -> Optional[RotationType]:
        """
        判断节点需要的旋转类型
        
        Args:
            node: 要检查的节点
            
        Returns:
            需要的旋转类型，如果平衡返回None
        """
        bf = node.get_balance_factor()
        
        if bf > 1:
            if node.left:
                left_bf = node.left.get_balance_factor()
                if left_bf >= 0:
                    return RotationType.RIGHT
                else:
                    return RotationType.LEFT_RIGHT
        elif bf < -1:
            if node.right:
                right_bf = node.right.get_balance_factor()
                if right_bf <= 0:
                    return RotationType.LEFT
                else:
                    return RotationType.RIGHT_LEFT
        
        return None
    
    def get_statistics(self) -> dict:
        """获取AVL树统计信息"""
        stats = super().get_statistics()
        stats['rotation_count'] = self._rotation_count
        stats['is_avl_balanced'] = self.is_balanced()
        return stats


# ==============================================================================
# 第五部分：可视化工具
# ==============================================================================

class TreeVisualizer:
    """树结构可视化工具"""
    
    @staticmethod
    def print_tree(node: Optional[TreeNode], prefix: str = "", is_left: bool = True) -> None:
        """
        打印树结构
        
        Args:
            node: 根节点
            prefix: 前缀字符串
            is_left: 是否是左子节点
        """
        if node is not None:
            TreeVisualizer.print_tree(
                node.right, 
                prefix + ("|   " if is_left else "    "), 
                False
            )
            balance_info = f" (bf={node.get_balance_factor()})" if hasattr(node, 'get_balance_factor') else ""
            print(prefix + ("\\-- " if is_left else "/-- ") + f"{node.value}{balance_info}")
            TreeVisualizer.print_tree(
                node.left, 
                prefix + ("    " if is_left else "|   "), 
                True
            )
    
    @staticmethod
    def print_tree_horizontal(node: Optional[TreeNode], level: int = 0) -> None:
        """
        水平方向打印树
        
        Args:
            node: 根节点
            level: 当前层级
        """
        if node is None:
            return
        
        TreeVisualizer.print_tree_horizontal(node.right, level + 1)
        print("    " * level + f"-> {node.value}")
        TreeVisualizer.print_tree_horizontal(node.left, level + 1)
    
    @staticmethod
    def get_tree_string(node: Optional[TreeNode]) -> str:
        """获取树的字符串表示"""
        lines: List[str] = []
        TreeVisualizer._build_tree_string(node, "", True, lines)
        return "\n".join(lines)
    
    @staticmethod
    def _build_tree_string(
        node: Optional[TreeNode], 
        prefix: str, 
        is_tail: bool, 
        lines: List[str]
    ) -> None:
        """构建树字符串"""
        if node is None:
            return
        
        lines.append(prefix + ("\\-- " if is_tail else "/-- ") + str(node.value))
        
        children = []
        if node.left:
            children.append(('L', node.left))
        if node.right:
            children.append(('R', node.right))
        
        for i, (_, child) in enumerate(children):
            is_last = i == len(children) - 1
            new_prefix = prefix + ("    " if is_tail else "|   ")
            TreeVisualizer._build_tree_string(child, new_prefix, is_last, lines)


# ==============================================================================
# 第六部分：测试框架
# ==============================================================================

class BSTTester:
    """二叉搜索树测试类"""
    
    def __init__(self):
        self.test_results: List[dict] = []
    
    def run_all_tests(self) -> None:
        """运行所有测试"""
        print("="*70)
        print("              二叉搜索树(BST)完整测试报告")
        print("="*70)
        
        self.test_basic_operations()
        self.test_deletion_cases()
        self.test_traversal_methods()
        self.test_avl_balancing()
        self.test_range_query()
        self.test_edge_cases()
        self.test_performance()
        
        self.print_summary()
    
    def test_basic_operations(self) -> None:
        """测试基础操作"""
        print("\n" + "-"*70)
        print("【测试1：基础操作】")
        print("-"*70)
        
        bst = BinarySearchTree[int]()
        
        print("\n插入测试:")
        for val in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(val)
            print(f"  插入 {val}, 大小: {bst.size}, 高度: {bst.get_height()}")
        
        print(f"\n查找测试:")
        for val in [50, 30, 100]:
            found = bst.contains(val)
            print(f"  查找 {val}: {'找到' if found else '未找到'}")
        
        print(f"\n最值测试:")
        print(f"  最小值: {bst.find_min()}")
        print(f"  最大值: {bst.find_max()}")
        
        print(f"\n统计信息:")
        stats = bst.get_statistics()
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    def test_deletion_cases(self) -> None:
        """测试删除操作的三种情况"""
        print("\n" + "-"*70)
        print("【测试2：删除操作】")
        print("-"*70)
        
        bst = BinarySearchTree[int]()
        values = [50, 30, 70, 20, 40, 60, 80]
        for v in values:
            bst.insert(v)
        
        print("\n初始树结构:")
        TreeVisualizer.print_tree(bst.root)
        
        print("\n情况1: 删除叶子节点 (20)")
        bst.delete(20)
        print(f"  删除后大小: {bst.size}")
        TreeVisualizer.print_tree(bst.root)
        
        print("\n情况2: 删除只有一个子节点的节点 (30)")
        bst.delete(30)
        print(f"  删除后大小: {bst.size}")
        TreeVisualizer.print_tree(bst.root)
        
        print("\n情况3: 删除有两个子节点的节点 (50)")
        bst.delete(50)
        print(f"  删除后大小: {bst.size}")
        TreeVisualizer.print_tree(bst.root)
    
    def test_traversal_methods(self) -> None:
        """测试遍历方法"""
        print("\n" + "-"*70)
        print("【测试3：遍历方法】")
        print("-"*70)
        
        bst = BinarySearchTree[int]()
        for v in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(v)
        
        print("\n树结构:")
        TreeVisualizer.print_tree(bst.root)
        
        print("\n前序遍历 (根-左-右):")
        print(f"  {bst.traverse(TraversalType.PREORDER)}")
        
        print("\n中序遍历 (左-根-右) - 有序序列:")
        print(f"  {bst.traverse(TraversalType.INORDER)}")
        
        print("\n后序遍历 (左-右-根):")
        print(f"  {bst.traverse(TraversalType.POSTORDER)}")
        
        print("\n层序遍历 (广度优先):")
        print(f"  {bst.traverse(TraversalType.LEVEL_ORDER)}")
    
    def test_avl_balancing(self) -> None:
        """测试AVL平衡"""
        print("\n" + "-"*70)
        print("【测试4：AVL平衡机制】")
        print("-"*70)
        
        print("\n普通BST插入有序数据:")
        bst = BinarySearchTree[int]()
        for v in [1, 2, 3, 4, 5, 6, 7]:
            bst.insert(v)
        print(f"  高度: {bst.get_height()} (理论最优: 3)")
        print(f"  是否平衡: {bst.is_balanced()}")
        print("  树结构:")
        TreeVisualizer.print_tree(bst.root)
        
        print("\nAVL树插入相同数据:")
        avl = AVLTree[int]()
        for v in [1, 2, 3, 4, 5, 6, 7]:
            avl.insert(v)
        print(f"  高度: {avl.get_height()}")
        print(f"  是否平衡: {avl.is_balanced()}")
        print(f"  旋转次数: {avl.rotation_count}")
        print("  树结构:")
        TreeVisualizer.print_tree(avl.root)
        
        print("\nAVL树删除测试:")
        print(f"  删除4前高度: {avl.get_height()}")
        avl.delete(4)
        print(f"  删除4后高度: {avl.get_height()}")
        print(f"  是否平衡: {avl.is_balanced()}")
        print("  树结构:")
        TreeVisualizer.print_tree(avl.root)
    
    def test_range_query(self) -> None:
        """测试范围查询"""
        print("\n" + "-"*70)
        print("【测试5：范围查询】")
        print("-"*70)
        
        bst = BinarySearchTree[int]()
        for v in [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]:
            bst.insert(v)
        
        print("\n树内容 (中序):")
        print(f"  {bst.traverse(TraversalType.INORDER)}")
        
        print("\n范围查询 [25, 50]:")
        result = bst.range_query(25, 50)
        print(f"  {result}")
        
        print("\n范围查询 [60, 80]:")
        result = bst.range_query(60, 80)
        print(f"  {result}")
    
    def test_edge_cases(self) -> None:
        """测试边界情况"""
        print("\n" + "-"*70)
        print("【测试6：边界情况】")
        print("-"*70)
        
        print("\n空树测试:")
        bst = BinarySearchTree[int]()
        print(f"  是否为空: {bst.is_empty}")
        print(f"  大小: {bst.size}")
        print(f"  高度: {bst.get_height()}")
        print(f"  是否平衡: {bst.is_balanced()}")
        
        print("\n单节点测试:")
        bst.insert(42)
        print(f"  大小: {bst.size}")
        print(f"  高度: {bst.get_height()}")
        print(f"  最小值: {bst.find_min()}")
        print(f"  最大值: {bst.find_max()}")
        
        print("\n重复值测试 (不允许重复):")
        bst2 = BinarySearchTree[int](allow_duplicates=False)
        bst2.insert(10)
        try:
            bst2.insert(10)
            print("  错误：应该抛出异常")
        except DuplicateKeyError as e:
            print(f"  正确捕获异常: {e}")
        
        print("\n重复值测试 (允许重复):")
        bst3 = BinarySearchTree[int](allow_duplicates=True)
        bst3.insert(10)
        bst3.insert(10)
        print(f"  大小: {bst3.size}")
        print(f"  中序遍历: {bst3.traverse(TraversalType.INORDER)}")
    
    def test_performance(self) -> None:
        """性能测试"""
        print("\n" + "-"*70)
        print("【测试7：性能对比】")
        print("-"*70)
        
        sizes = [50, 100, 200]
        
        print(f"\n{'数据量':<10} {'BST高度':<12} {'AVL高度':<12} {'BST平衡':<10} {'AVL平衡':<10}")
        print("-"*50)
        
        for size in sizes:
            data = list(range(1, size + 1))
            
            bst = BinarySearchTree[int]()
            start = time.perf_counter()
            for v in data:
                bst.insert_iterative(v)
            bst_time = time.perf_counter() - start
            
            avl = AVLTree[int]()
            start = time.perf_counter()
            for v in data:
                avl.insert(v)
            avl_time = time.perf_counter() - start
            
            print(f"{size:<10} {bst.get_height():<12} {avl.get_height():<12} "
                  f"{'是' if bst.is_balanced() else '否':<10} "
                  f"{'是' if avl.is_balanced() else '否':<10}")
    
    def print_summary(self) -> None:
        """打印测试总结"""
        print("\n" + "="*70)
        print("                        测试总结")
        print("="*70)
        print("""
二叉搜索树(BST)核心特性:
1. 中序遍历结果为有序序列
2. 查找/插入/删除平均O(log n)，最坏O(n)
3. 删除操作需处理三种情况

AVL树核心特性:
1. 保证任何节点平衡因子绝对值<=1
2. 通过旋转操作维持平衡
3. 保证所有操作O(log n)

选择建议:
- 数据随机分布 -> 普通BST即可
- 数据有序或接近有序 -> 使用AVL树
- 需要频繁插入删除 -> AVL树更稳定
        """)


# ==============================================================================
# 第七部分：主程序
# ==============================================================================

def main():
    """主程序入口"""
    print("="*70)
    print("           二叉搜索树(BST)完整实现演示")
    print("="*70)
    
    print("""
【数据结构概述】

二叉搜索树(BST)是一种特殊的二叉树，具有以下性质：
- 左子树所有节点值 < 根节点值 < 右子树所有节点值
- 中序遍历结果为有序序列

AVL树是自平衡的BST：
- 任何节点的左右子树高度差不超过1
- 通过旋转操作维持平衡
- 保证O(log n)的操作时间复杂度
""")
    
    tester = BSTTester()
    tester.run_all_tests()
    
    print("\n" + "="*70)
    print("                    程序执行完毕")
    print("="*70)


if __name__ == "__main__":
    main()
