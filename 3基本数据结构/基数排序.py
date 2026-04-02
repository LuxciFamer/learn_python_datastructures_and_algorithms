from collections import deque

class RadixSort:
    """
    基数排序实现
    使用1个主桶和10个数位桶（0-9）
    每个桶是一个队列，按照数字到达的先后顺序维持其中的值
    """
    
    def __init__(self):
        """初始化基数排序器"""
        self.main_bucket = deque()  # 主桶
        self.digit_buckets = [deque() for _ in range(10)]  # 10个数位桶（0-9）
    
    def get_max_digits(self, numbers):
        """
        获取数组中最大数的位数
        numbers: 待排序的数字列表
        """
        if not numbers:
            return 0
        max_num = max(numbers)
        return len(str(max_num))
    
    def get_digit(self, number, position):
        """
        获取数字在指定位置的数位值
        number: 数字
        position: 位置（0表示个位，1表示十位，以此类推）
        """
        return (number // (10 ** position)) % 10
    
    def sort(self, numbers):
        """
        执行基数排序
        numbers: 待排序的数字列表
        """
        if not numbers:
            return []
        
        # 将所有数字放入主桶
        for number in numbers:
            self.main_bucket.append(number)
        
        # 确定最大位数
        max_digits = self.get_max_digits(numbers)
        
        # 对每一位进行排序
        for position in range(max_digits):
            # 从主桶中取出所有数字，放入对应的数位桶
            while self.main_bucket:
                number = self.main_bucket.popleft()
                digit = self.get_digit(number, position)
                self.digit_buckets[digit].append(number)
            
            # 将数位桶中的数字依次放回主桶
            for i in range(10):
                while self.digit_buckets[i]:
                    self.main_bucket.append(self.digit_buckets[i].popleft())
        
        # 将主桶中的数字转换为列表并返回
        sorted_numbers = []
        while self.main_bucket:
            sorted_numbers.append(self.main_bucket.popleft())
        
        return sorted_numbers
    
    def sort_with_visualization(self, numbers):
        """
        执行基数排序并可视化过程
        numbers: 待排序的数字列表
        """
        if not numbers:
            print("空列表，无需排序")
            return []
        
        print(f"原始数组: {numbers}")
        
        # 将所有数字放入主桶
        for number in numbers:
            self.main_bucket.append(number)
        
        print(f"初始主桶: {list(self.main_bucket)}")
        
        # 确定最大位数
        max_digits = self.get_max_digits(numbers)
        print(f"最大位数: {max_digits}")
        
        # 对每一位进行排序
        for position in range(max_digits):
            print(f"\n处理第 {position+1} 位（{10**position} 位）:")
            
            # 从主桶中取出所有数字，放入对应的数位桶
            while self.main_bucket:
                number = self.main_bucket.popleft()
                digit = self.get_digit(number, position)
                self.digit_buckets[digit].append(number)
                print(f"  将 {number} 放入 {digit} 号数位桶")
            
            # 打印数位桶状态
            print("  数位桶状态:")
            for i in range(10):
                if self.digit_buckets[i]:
                    print(f"    桶 {i}: {list(self.digit_buckets[i])}")
            
            # 将数位桶中的数字依次放回主桶
            print("  将数位桶中的数字放回主桶:")
            for i in range(10):
                while self.digit_buckets[i]:
                    number = self.digit_buckets[i].popleft()
                    self.main_bucket.append(number)
                    print(f"    从桶 {i} 取出 {number} 放入主桶")
            
            print(f"  主桶状态: {list(self.main_bucket)}")
        
        # 将主桶中的数字转换为列表并返回
        sorted_numbers = []
        while self.main_bucket:
            sorted_numbers.append(self.main_bucket.popleft())
        
        print(f"\n排序结果: {sorted_numbers}")
        return sorted_numbers

# --- 测试代码 ---
if __name__ == "__main__":
    # 测试数据
    test_cases = [
        [534, 667, 123, 456, 987, 321, 789, 654, 345, 234],
        [10, 2, 300, 45, 678, 9, 123, 456, 789, 1000],
        [5, 4, 3, 2, 1],
        [1, 1, 1, 1, 1],
        []
    ]
    
    sorter = RadixSort()
    
    print("=== 测试基数排序 ===")
    for i, test_case in enumerate(test_cases):
        print(f"\n测试用例 {i+1}: {test_case}")
        sorted_result = sorter.sort(test_case)
        print(f"排序结果: {sorted_result}")
        print(f"是否正确: {sorted_result == sorted(test_case)}")
    
    # 可视化排序过程
    print("\n=== 可视化排序过程 ===")
    sorter2 = RadixSort()
    test_data = [534, 667, 123, 456, 987, 321]
    sorter2.sort_with_visualization(test_data)
