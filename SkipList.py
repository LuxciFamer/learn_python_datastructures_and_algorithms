import random

class Node:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=16):
        self.max_level = max_level
        self.header = Node(None, None, max_level)
        self.level = 0
    
    def random_level(self):
        level = 0
        while random.random() < 0.5 and level < self.max_level:
            level += 1
        return level
    
    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return None
    
    def insert(self, key, value):
        update = [None] * (self.max_level + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        current = current.forward[0]
        if current and current.key == key:
            current.value = value
        else:
            new_level = self.random_level()
            if new_level > self.level:
                for i in range(self.level + 1, new_level + 1):
                    update[i] = self.header
                self.level = new_level
            new_node = Node(key, value, new_level)
            for i in range(new_level + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node
    
    def delete(self, key):
        """删除指定键的节点
        可以假设键存在
        时间复杂度：O(log n)
        """
        update = [None] * (self.max_level + 1)
        current = self.header
        # 找到每个层级中需要更新的节点
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        # 定位到要删除的节点
        current = current.forward[0]
        # 确认节点存在且键匹配
        if current and current.key == key:
            # 更新每个层级的指针
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]
            # 调整跳表的层级
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
    
    def display(self):
        print("跳表结构:")
        for level in range(self.level, -1, -1):
            print(f"Level {level}: ", end="")
            node = self.header.forward[level]
            while node:
                print(f"({node.key}, {node.value}) ", end="")
                node = node.forward[level]
            print()
    
    def contains(self, key):
        """检查键是否存在于映射中
        返回一个布尔值，用于说明键是否存在于映射中
        时间复杂度：O(log n)
        """
        return self.search(key) is not None
    
    def keys(self):
        """返回映射中键的列表
        时间复杂度：O(n)，需要遍历所有节点
        """
        keys_list = []
        node = self.header.forward[0]
        while node:
            keys_list.append(node.key)
            node = node.forward[0]
        return keys_list
    
    def values(self):
        """返回映射中值的列表
        时间复杂度：O(n)，需要遍历所有节点
        """
        values_list = []
        node = self.header.forward[0]
        while node:
            values_list.append(node.value)
            node = node.forward[0]
        return values_list
    
    def __getitem__(self, key):
        """支持使用 [] 操作符访问元素
        时间复杂度：O(log n)
        """
        value = self.search(key)
        if value is None:
            raise KeyError(f"键 {key} 不存在")
        return value
    
    def __setitem__(self, key, value):
        """支持使用 [] 操作符设置元素
        时间复杂度：O(log n)
        """
        self.insert(key, value)

# 测试代码
if __name__ == "__main__":
    sl = SkipList()
    
    # 插入测试数据
    sl.insert(3, "value3")
    sl.insert(6, "value6")
    sl.insert(7, "value7")
    sl.insert(9, "value9")
    sl.insert(12, "value12")
    sl.insert(19, "value19")
    sl.insert(17, "value17")
    sl.insert(26, "value26")
    sl.insert(21, "value21")
    sl.insert(25, "value25")
    
    print("插入后:")
    sl.display()
    
    # 测试删除
    print("\n删除键 19:")
    sl.delete(19)
    sl.display()
    
    print("\n删除键 6:")
    sl.delete(6)
    sl.display()
    
    print("\n删除键 25:")
    sl.delete(25)
    sl.display()
    
    # 测试 contains() 方法
    print("\n测试 contains() 方法:")
    print("是否包含键 3:", sl.contains(3))
    print("是否包含键 6:", sl.contains(6))  # 已删除
    print("是否包含键 25:", sl.contains(25))  # 已删除
    print("是否包含键 100:", sl.contains(100))  # 不存在
    
    # 测试 keys() 方法
    print("\n测试 keys() 方法:")
    print("所有键:", sl.keys())
    
    # 测试 values() 方法
    print("\n测试 values() 方法:")
    print("所有值:", sl.values())
    
    # 测试 __getitem__ 方法
    print("\n测试 __getitem__ 方法:")
    print("sl[3]:", sl[3])
    print("sl[17]:", sl[17])
    print("sl[26]:", sl[26])
    
    # 测试 __setitem__ 方法
    print("\n测试 __setitem__ 方法:")
    sl[3] = "updated_value3"
    print("更新后 sl[3]:", sl[3])
    sl[100] = "new_value100"
    print("新增 sl[100]:", sl[100])
    
    # 显示更新后的跳表
    print("\n更新后的跳表:")
    sl.display()
    print("所有键:", sl.keys())
    print("所有值:", sl.values())
