class HanoiTower:
    """
    汉诺塔问题解决方案
    使用三个栈来表示三个柱子
    """
    
    def __init__(self, n):
        """
        初始化汉诺塔
        
        Args:
            n: 盘子数量
        """
        self.n = n
        # 初始化三个栈，源栈包含n个盘子，从大到小排列
        self.source = list(range(n, 0, -1))  # 源栈: [n, n-1, ..., 1]
        self.auxiliary = []  # 辅助栈
        self.target = []  # 目标栈
        self.moves = []  # 记录移动步骤
    
    def move_disk(self, source, target, source_name, target_name):
        """
        移动一个盘子
        
        Args:
            source: 源栈
            target: 目标栈
            source_name: 源栈名称
            target_name: 目标栈名称
        """
        if not source:
            return False
        
        # 检查移动是否合法：目标栈为空或目标栈顶盘子大于当前盘子
        if not target or source[-1] < target[-1]:
            disk = source.pop()
            target.append(disk)
            # 记录移动步骤
            self.moves.append((source_name, target_name, disk))
            return True
        return False
    
    def solve_recursive(self, n, source, auxiliary, target, source_name, auxiliary_name, target_name):
        """
        递归解决汉诺塔问题
        
        Args:
            n: 盘子数量
            source: 源栈
            auxiliary: 辅助栈
            target: 目标栈
            source_name: 源栈名称
            auxiliary_name: 辅助栈名称
            target_name: 目标栈名称
        """
        if n == 1:
            # 基础情况：移动一个盘子
            self.move_disk(source, target, source_name, target_name)
            self.print_state()
        else:
            # 步骤1：将n-1个盘子从源栈移动到辅助栈
            self.solve_recursive(n-1, source, target, auxiliary, source_name, target_name, auxiliary_name)
            
            # 步骤2：将第n个盘子从源栈移动到目标栈
            self.move_disk(source, target, source_name, target_name)
            self.print_state()
            
            # 步骤3：将n-1个盘子从辅助栈移动到目标栈
            self.solve_recursive(n-1, auxiliary, source, target, auxiliary_name, source_name, target_name)
    
    def solve(self):
        """
        开始解决汉诺塔问题
        """
        print("初始状态:")
        self.print_state()
        self.solve_recursive(self.n, self.source, self.auxiliary, self.target, "A", "B", "C")
        print("\n移动完成！")
        self.verify_result()
    
    def print_state(self):
        """
        打印当前三个栈的状态
        """
        print(f"A: {self.source}")
        print(f"B: {self.auxiliary}")
        print(f"C: {self.target}")
        print("-")
    
    def verify_result(self):
        """
        验证结果是否正确
        """
        # 检查源栈和辅助栈是否为空
        if not self.source and not self.auxiliary:
            # 检查目标栈是否按从小到大顺序排列
            for i in range(len(self.target) - 1):
                if self.target[i] < self.target[i+1]:
                    print("验证失败：目标栈盘子顺序错误")
                    return
            print("验证成功：所有盘子已正确移动到目标栈")
        else:
            print("验证失败：源栈或辅助栈不为空")
    
    def print_moves(self):
        """
        打印所有移动步骤
        """
        print(f"\n共移动了 {len(self.moves)} 步：")
        for i, (source, target, disk) in enumerate(self.moves, 1):
            print(f"步骤 {i}: 将盘子 {disk} 从 {source} 移动到 {target}")

# 测试汉诺塔问题
if __name__ == "__main__":
    # 测试3个盘子的情况
    print("=== 测试3个盘子的汉诺塔问题 ===")
    hanoi_3 = HanoiTower(3)
    hanoi_3.solve()
    hanoi_3.print_moves()
    
    print("\n" + "="*50 + "\n")
    
    # 测试4个盘子的情况
    print("=== 测试4个盘子的汉诺塔问题 ===")
    hanoi_4 = HanoiTower(4)
    hanoi_4.solve()
    hanoi_4.print_moves()
