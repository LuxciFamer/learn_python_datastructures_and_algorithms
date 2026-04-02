class Node:
    """
    双向链表节点类
    """
    def __init__(self, data):
        """
        初始化节点
        data: 节点数据
        """
        self.data = data      # 数据域
        self.back = None      # 指向前一个节点的引用
        self.next = None      # 指向后一个节点的引用

class DoublyLinkedList:
    """
    双向链表类
    """
    def __init__(self):
        """
        初始化空的双向链表
        头引用同时指向链表中的第一个节点和最后一个节点
        """
        self.head = None      # 头引用
    
    def is_empty(self):
        """
        判断链表是否为空
        return: 链表是否为空
        """
        return self.head is None
    
    def add_head(self, data):
        """
        在头部添加节点
        data: 要添加的数据
        """
        new_node = Node(data)
        
        if self.is_empty():
            # 空链表，新节点既是头也是尾
            self.head = new_node
        else:
            # 非空链表，将新节点插入到头部
            new_node.next = self.head
            self.head.back = new_node
            self.head = new_node
    
    def add_tail(self, data):
        """
        在尾部添加节点
        data: 要添加的数据
        """
        new_node = Node(data)
        
        if self.is_empty():
            # 空链表，新节点既是头也是尾
            self.head = new_node
        else:
            # 非空链表，找到尾节点并插入
            current = self.head
            while current.next:
                current = current.next
            
            current.next = new_node
            new_node.back = current
    
    def insert(self, position, data):
        """
        在指定位置插入节点
        position: 插入位置（从0开始）
        data: 要添加的数据
        """
        if position < 0:
            raise IndexError("位置不能为负数")
        
        if position == 0:
            # 在头部插入
            self.add_head(data)
            return
        
        new_node = Node(data)
        current = self.head
        
        # 移动到指定位置的前一个节点
        for i in range(position - 1):
            if current is None:
                raise IndexError("位置超出链表长度")
            current = current.next
        
        if current is None:
            raise IndexError("位置超出链表长度")
        
        if current.next is None:
            # 在尾部插入
            current.next = new_node
            new_node.back = current
        else:
            # 在中间插入
            new_node.next = current.next
            new_node.back = current
            current.next.back = new_node
            current.next = new_node
    
    def remove_head(self):
        """
        删除头部节点
        return: 删除的节点数据
        """
        if self.is_empty():
            raise IndexError("链表为空，无法删除")
        
        data = self.head.data
        
        if self.head.next is None:
            # 只有一个节点
            self.head = None
        else:
            # 多个节点
            self.head = self.head.next
            self.head.back = None
        
        return data
    
    def remove_tail(self):
        """
        删除尾部节点
        return: 删除的节点数据
        """
        if self.is_empty():
            raise IndexError("链表为空，无法删除")
        
        current = self.head
        
        # 找到尾节点
        while current.next:
            current = current.next
        
        data = current.data
        
        if current.back is None:
            # 只有一个节点
            self.head = None
        else:
            # 多个节点
            current.back.next = None
        
        return data
    
    def remove_value(self, value):
        """
        删除指定值的节点
        value: 要删除的值
        return: 是否删除成功
        """
        if self.is_empty():
            return False
        
        current = self.head
        
        # 查找值为value的节点
        while current:
            if current.data == value:
                # 找到要删除的节点
                if current.back is None:
                    # 头节点
                    self.remove_head()
                elif current.next is None:
                    # 尾节点
                    self.remove_tail()
                else:
                    # 中间节点
                    current.back.next = current.next
                    current.next.back = current.back
                return True
            current = current.next
        
        return False
    
    def traverse_forward(self):
        """
        正向遍历链表
        return: 遍历结果列表
        """
        result = []
        current = self.head
        
        while current:
            result.append(current.data)
            current = current.next
        
        return result
    
    def traverse_backward(self):
        """
        反向遍历链表
        return: 遍历结果列表
        """
        result = []
        
        if self.is_empty():
            return result
        
        # 找到尾节点
        current = self.head
        while current.next:
            current = current.next
        
        # 从尾节点开始反向遍历
        while current:
            result.append(current.data)
            current = current.back
        
        return result
    
    def find(self, value):
        """
        查找指定值是否存在于链表中
        value: 要查找的值
        return: 是否找到
        """
        current = self.head
        
        while current:
            if current.data == value:
                return True
            current = current.next
        
        return False
    
    def length(self):
        """
        返回链表中节点的个数
        return: 链表长度
        """
        count = 0
        current = self.head
        
        while current:
            count += 1
            current = current.next
        
        return count

# --- 测试代码 ---
if __name__ == "__main__":
    # 创建双向链表
    dll = DoublyLinkedList()
    
    print("=== 测试双向链表 ===")
    
    # 测试判空
    print(f"链表是否为空: {dll.is_empty()}")
    print(f"链表长度: {dll.length()}")
    
    # 测试添加节点
    print("\n测试添加节点:")
    dll.add_head(1)
    dll.add_head(2)
    dll.add_tail(3)
    dll.add_tail(4)
    print(f"正向遍历: {dll.traverse_forward()}")
    print(f"反向遍历: {dll.traverse_backward()}")
    print(f"链表长度: {dll.length()}")
    
    # 测试插入节点
    print("\n测试插入节点:")
    dll.insert(2, 5)
    print(f"在位置2插入5后: {dll.traverse_forward()}")
    dll.insert(0, 6)
    print(f"在位置0插入6后: {dll.traverse_forward()}")
    dll.insert(6, 7)
    print(f"在位置6插入7后: {dll.traverse_forward()}")
    
    # 测试查找
    print("\n测试查找:")
    print(f"查找5: {dll.find(5)}")
    print(f"查找10: {dll.find(10)}")
    
    # 测试删除节点
    print("\n测试删除节点:")
    print(f"删除头部节点: {dll.remove_head()}")
    print(f"删除后正向遍历: {dll.traverse_forward()}")
    print(f"删除尾部节点: {dll.remove_tail()}")
    print(f"删除后正向遍历: {dll.traverse_forward()}")
    print(f"删除值为5的节点: {dll.remove_value(5)}")
    print(f"删除后正向遍历: {dll.traverse_forward()}")
    print(f"删除值为10的节点: {dll.remove_value(10)}")
    print(f"删除后正向遍历: {dll.traverse_forward()}")
    
    # 测试边界情况
    print("\n测试边界情况:")
    print(f"链表长度: {dll.length()}")
    
    # 测试删除所有节点
    while not dll.is_empty():
        dll.remove_head()
    print(f"删除所有节点后，链表是否为空: {dll.is_empty()}")
    print(f"链表长度: {dll.length()}")
    
    # 测试空链表操作
    print("\n测试空链表操作:")
    try:
        dll.remove_head()
    except IndexError as e:
        print(f"空链表删除头部节点错误: {e}")
    
    try:
        dll.remove_tail()
    except IndexError as e:
        print(f"空链表删除尾部节点错误: {e}")
    
    # 测试在空链表中添加节点
    print("\n测试在空链表中添加节点:")
    dll.add_head(10)
    print(f"添加节点10后，正向遍历: {dll.traverse_forward()}")
    print(f"反向遍历: {dll.traverse_backward()}")
