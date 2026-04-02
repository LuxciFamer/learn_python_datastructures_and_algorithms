class CircularQueue:
    """
    循环队列实现
    添加操作和移除操作的平均时间复杂度为 O(1)
    仅在扩容时移除操作为 O(n)
    """
    
    def __init__(self, capacity=10):
        """
        初始化循环队列
        capacity: 初始容量
        """
        self.capacity = capacity
        self.items = [None] * capacity
        self.front = 0  # 队首指针
        self.rear = 0   # 队尾指针
        self.size = 0   # 当前元素数量
    
    def is_empty(self):
        """检查队列是否为空"""
        return self.size == 0
    
    def is_full(self):
        """检查队列是否已满"""
        return self.size == self.capacity
    
    def enqueue(self, item):
        """在队列尾部添加一个元素"""
        # 如果队列已满，需要扩容
        if self.is_full():
            self._resize()
        
        # 在队尾添加元素
        self.items[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
    
    def dequeue(self):
        """从队列头部移除并返回一个元素"""
        if self.is_empty():
            raise IndexError("队列为空，无法出队")
        
        # 获取队首元素
        item = self.items[self.front]
        self.items[self.front] = None  # 可选：清空已移除的元素
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        
        # 可选：当队列元素较少时，缩容以节省空间
        # if self.size < self.capacity // 4 and self.capacity > 10:
        #     self._shrink()
        
        return item
    
    def get_size(self):
        """返回队列中元素的数量"""
        return self.size
    
    def peek(self):
        """返回队列头部的元素，但不移除它"""
        if self.is_empty():
            raise IndexError("队列为空，无法查看队首元素")
        return self.items[self.front]
    
    def _resize(self):
        """扩容队列，时间复杂度为 O(n)"""
        new_capacity = self.capacity * 2
        new_items = [None] * new_capacity
        
        # 将原有元素复制到新数组
        for i in range(self.size):
            new_items[i] = self.items[(self.front + i) % self.capacity]
        
        # 更新队列属性
        self.items = new_items
        self.capacity = new_capacity
        self.front = 0
        self.rear = self.size
    
    def _shrink(self):
        """缩容队列，时间复杂度为 O(n)"""
        new_capacity = max(self.capacity // 2, 10)
        new_items = [None] * new_capacity
        
        # 将原有元素复制到新数组
        for i in range(self.size):
            new_items[i] = self.items[(self.front + i) % self.capacity]
        
        # 更新队列属性
        self.items = new_items
        self.capacity = new_capacity
        self.front = 0
        self.rear = self.size
    
    def __str__(self):
        """返回队列的字符串表示"""
        if self.is_empty():
            return "CircularQueue([])"
        
        elements = []
        for i in range(self.size):
            elements.append(str(self.items[(self.front + i) % self.capacity]))
        
        return f"CircularQueue([{', '.join(elements)}])"
    
    def __repr__(self):
        """返回队列的官方字符串表示"""
        return self.__str__()


# --- 测试代码 ---
if __name__ == "__main__":
    # 创建一个循环队列
    q = CircularQueue(capacity=5)
    print(f"初始队列: {q}")
    print(f"队列是否为空: {q.is_empty()}")
    print(f"队列容量: {q.capacity}")
    
    # 入队操作
    for i in range(7):
        q.enqueue(i)
        print(f"入队 {i} 后: {q}")
        print(f"队列大小: {q.get_size()}")
        print(f"队列容量: {q.capacity}")
    
    # 查看队首元素
    print(f"队首元素: {q.peek()}")
    
    # 出队操作
    for _ in range(5):
        item = q.dequeue()
        print(f"出队元素: {item}")
        print(f"出队后: {q}")
        print(f"队列大小: {q.get_size()}")
        print(f"队列容量: {q.capacity}")
    
    # 继续入队
    for i in range(10, 15):
        q.enqueue(i)
        print(f"入队 {i} 后: {q}")
        print(f"队列大小: {q.get_size()}")
        print(f"队列容量: {q.capacity}")
    
    # 测试空队列情况
    while not q.is_empty():
        item = q.dequeue()
        print(f"出队元素: {item}")
        print(f"出队后: {q}")
    
    print(f"队列是否为空: {q.is_empty()}")
    
    # 测试异常
    try:
        q.dequeue()
    except IndexError as e:
        print(f"预期异常: {e}")
    
    try:
        q.peek()
    except IndexError as e:
        print(f"预期异常: {e}")
