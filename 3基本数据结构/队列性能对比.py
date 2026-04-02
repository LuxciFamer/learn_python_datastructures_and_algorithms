import time
from collections import deque

# 基于列表的队列实现
class ListQueue:
    def __init__(self):
        self.items = []
    
    def is_empty(self):
        return len(self.items) == 0
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("队列为空，无法出队")
        return self.items.pop(0)
    
    def size(self):
        return len(self.items)

# 基于deque的队列实现
class DequeQueue:
    def __init__(self):
        self.items = deque()
    
    def is_empty(self):
        return len(self.items) == 0
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("队列为空，无法出队")
        return self.items.popleft()
    
    def size(self):
        return len(self.items)

# 性能测试函数
def test_queue_performance(queue_class, operation, size, repetitions=3):
    """
    测试队列性能
    queue_class: 队列类
    operation: 操作类型 ('enqueue', 'dequeue', 'mixed')
    size: 数据规模
    repetitions: 重复次数
    """
    times = []
    
    for _ in range(repetitions):
        queue = queue_class()
        start_time = time.time()
        
        if operation == 'enqueue':
            # 测试入队操作
            for i in range(size):
                queue.enqueue(i)
        
        elif operation == 'dequeue':
            # 先入队，再测试出队操作
            for i in range(size):
                queue.enqueue(i)
            start_time = time.time()  # 重新计时，只计算出队时间
            for _ in range(size):
                queue.dequeue()
        
        elif operation == 'mixed':
            # 测试混合操作：入队和出队交替
            for i in range(size):
                queue.enqueue(i)
                if i % 2 == 1:  # 每两个元素出队一个
                    queue.dequeue()
        
        end_time = time.time()
        times.append(end_time - start_time)
    
    # 返回平均时间
    return sum(times) / len(times)

# 主测试函数
def main():
    print("队列性能对比实验")
    print("=" * 60)
    
    # 测试数据规模
    sizes = [1000, 5000, 10000, 50000]
    # 测试操作类型
    operations = ['enqueue', 'dequeue', 'mixed']
    
    # 打印表头
    print(f"{'操作类型':<10} {'数据规模':<10} {'ListQueue(秒)':<15} {'DequeQueue(秒)':<15} {'性能提升':<10}")
    print("-" * 60)
    
    # 运行测试
    for operation in operations:
        for size in sizes:
            # 测试基于列表的队列
            list_time = test_queue_performance(ListQueue, operation, size)
            # 测试基于deque的队列
            deque_time = test_queue_performance(DequeQueue, operation, size)
            # 计算性能提升
            speedup = list_time / deque_time if deque_time > 0 else float('inf')
            
            # 打印结果
            print(f"{operation:<10} {size:<10} {list_time:<15.6f} {deque_time:<15.6f} {speedup:<10.2f}x")
        print("-" * 60)
    
    # 总结
    print("\n实验总结:")
    print("1. 基于deque的队列在出队操作上性能显著优于基于列表的队列")
    print("2. 对于入队操作，两种实现性能相近")
    print("3. 数据规模越大，性能差异越明显")
    print("4. deque的popleft()操作时间复杂度为O(1)，而列表的pop(0)为O(n)")

if __name__ == "__main__":
    main()
