class ArrayList:
    def __init__(self):
        self.items = []
    
    def __len__(self):
        return len(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
    def __setitem__(self, index, value):
        self.items[index] = value
    
    def __str__(self):
        return str(self.items)
    
    def append(self, value):
        self.items.append(value)
    
    def insert(self, index, value):
        self.items.insert(index, value)
    
    def __delitem__(self, index):
        """删除列表中给定位置上的元素
        时间复杂度：O(n)，因为删除元素后需要移动后面的元素
        """
        del self.items[index]
    
    def pop(self, index=None):
        """实现弹出方法，包括带参数和不带参数两个版本
        时间复杂度：
        - 不带参数（默认弹出最后一个元素）：O(1)
        - 带参数（弹出指定位置元素）：O(n)，因为需要移动后面的元素
        """
        if index is None:
            return self.items.pop()
        else:
            return self.items.pop(index)
    
    def index(self, value):
        """在 ArrayList 中搜索给定的值
        若找到，返回它在列表中的位置，否则返回-1
        时间复杂度：O(n)，最坏情况下需要遍历整个列表
        """
        try:
            return self.items.index(value)
        except ValueError:
            return -1
    
    def __iter__(self):
        """让 ArrayList 可迭代
        时间复杂度：O(1)，返回迭代器对象
        """
        return iter(self.items)
    
    def __add__(self, other):
        """支持 + 运算，用于连接两个列表
        时间复杂度：O(n)，其中 n 是两个列表的总长度
        """
        if not isinstance(other, ArrayList):
            raise TypeError("只能与 ArrayList 类型进行连接操作")
        result = ArrayList()
        result.items = self.items + other.items
        return result
    
    def __mul__(self, factor):
        """支持 * 运算，用于重复列表元素
        时间复杂度：O(n)，其中 n 是重复后的列表长度
        """
        if not isinstance(factor, int) or factor < 0:
            raise TypeError("重复因子必须是非负整数")
        result = ArrayList()
        result.items = self.items * factor
        return result

# 测试代码
if __name__ == "__main__":
    # 创建 ArrayList 实例
    al = ArrayList()
    
    # 测试 append
    for i in range(5):
        al.append(i)
    print("初始列表:", al)
    
    # 测试 del
    del al[2]
    print("删除索引2后的列表:", al)
    
    # 测试 pop 不带参数
    popped = al.pop()
    print("弹出最后一个元素:", popped)
    print("弹出后的列表:", al)
    
    # 测试 pop 带参数
    popped = al.pop(1)
    print("弹出索引1的元素:", popped)
    print("弹出后的列表:", al)
    
    # 测试 index
    print("元素1的索引:", al.index(1))
    print("元素10的索引:", al.index(10))
    
    # 测试可迭代性
    print("遍历列表:")
    for item in al:
        print(item)
    
    # 测试 + 运算
    al1 = ArrayList()
    for i in range(3):
        al1.append(i)
    al2 = ArrayList()
    for i in range(3, 6):
        al2.append(i)
    al3 = al1 + al2
    print("连接后的列表:", al3)
    
    # 测试 * 运算
    al4 = al1 * 3
    print("重复3次后的列表:", al4)
