def factorial(n):
    """
    计算非负整数的阶乘
    
    Args:
        n (int): 非负整数
    
    Returns:
        int: n的阶乘
    
    Raises:
        ValueError: 当输入为负数时
    """
    # 输入验证
    if not isinstance(n, int):
        raise ValueError("输入必须是整数")
    if n < 0:
        raise ValueError("输入必须是非负整数")
    
    # 递归基例
    if n == 0 or n == 1:
        return 1
    
    # 递归调用
    return n * factorial(n - 1)


# 测试函数
if __name__ == "__main__":
    # 测试正常输入
    print(f"0! = {factorial(0)}")  # 应输出 1
    print(f"1! = {factorial(1)}")  # 应输出 1
    print(f"5! = {factorial(5)}")  # 应输出 120
    print(f"10! = {factorial(10)}")  # 应输出 3628800
    
    # 测试负数输入
    try:
        factorial(-1)
    except ValueError as e:
        print(f"错误处理测试: {e}")
    
    # 测试非整数输入
    try:
        factorial(2.5)
    except ValueError as e:
        print(f"错误处理测试: {e}")
