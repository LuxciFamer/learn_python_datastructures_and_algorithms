class Queue:
    """
    使用列表实现队列抽象数据类型
    将列表的后端作为队列的尾部
    """
    
    def __init__(self):
        """初始化一个空队列"""
        self.items = []
    
    def is_empty(self):
        """检查队列是否为空"""
        return len(self.items) == 0
    
    def enqueue(self, item):
        """在队列尾部添加一个元素"""
        self.items.append(item)
    
    def dequeue(self):
        """从队列头部移除并返回一个元素"""
        if self.is_empty():
            raise IndexError("队列为空，无法出队")
        return self.items.pop(0)
    
    def size(self):
        """返回队列中元素的数量"""
        return len(self.items)
    
    def peek(self):
        """返回队列头部的元素，但不移除它"""
        if self.is_empty():
            raise IndexError("队列为空，无法查看队首元素")
        return self.items[0]
    
    def __str__(self):
        """返回队列的字符串表示"""
        return f"Queue({self.items})"
    
    def __repr__(self):
        """返回队列的官方字符串表示"""
        return f"Queue({self.items})"


# --- 测试代码 ---
if __name__ == "__main__":
    # 创建一个队列
    q = Queue()
    print(f"初始队列: {q}")
    print(f"队列是否为空: {q.is_empty()}")
    
    # 入队操作
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    print(f"入队后: {q}")
    print(f"队列大小: {q.size()}")
    
    # 查看队首元素
    print(f"队首元素: {q.peek()}")
    
    # 出队操作
    print(f"出队元素: {q.dequeue()}")
    print(f"出队后: {q}")
    print(f"队列大小: {q.size()}")
    
    # 继续出队
    print(f"出队元素: {q.dequeue()}")
    print(f"出队后: {q}")
    print(f"队列大小: {q.size()}")
    
    # 测试空队列情况
    print(f"出队元素: {q.dequeue()}")
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
