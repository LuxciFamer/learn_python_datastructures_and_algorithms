import time
import sys
import tracemalloc

def fibonacci_recursive(n):
    """
    递归计算斐波那契数列的第n项
    
    Args:
        n (int): 非负整数
    
    Returns:
        int: 斐波那契数列的第n项
    
    Raises:
        ValueError: 当输入为负数时
    """
    # 参数验证
    if not isinstance(n, int):
        raise ValueError("输入必须是整数")
    if n < 0:
        raise ValueError("输入必须是非负整数")
    
    # 边界条件
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # 递归调用
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def fibonacci_iterative(n):
    """
    循环计算斐波那契数列的第n项
    
    Args:
        n (int): 非负整数
    
    Returns:
        int: 斐波那契数列的第n项
    
    Raises:
        ValueError: 当输入为负数时
    """
    # 参数验证
    if not isinstance(n, int):
        raise ValueError("输入必须是整数")
    if n < 0:
        raise ValueError("输入必须是非负整数")
    
    # 边界条件
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    # 循环计算
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def measure_performance(func, n):
    """
    测量函数的执行时间和内存占用
    
    Args:
        func: 要测量的函数
        n: 函数参数
    
    Returns:
        tuple: (执行时间(ms), 内存占用(KB), 计算结果)
    """
    # 测量时间
    start_time = time.time()
    
    # 测量内存
    tracemalloc.start()
    
    # 执行函数
    result = func(n)
    
    # 获取内存使用情况
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 计算执行时间
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # 转换为毫秒
    
    # 内存占用转换为KB
    memory_used = peak / 1024
    
    return execution_time, memory_used, result

def run_tests():
    """
    运行性能测试并生成分析报告
    """
    test_values = [10, 20, 30, 40]
    
    print("斐波那契数列计算性能测试")
    print("=" * 80)
    print(f"{'n':<5} {'递归时间(ms)':<15} {'递归内存(KB)':<15} {'循环时间(ms)':<15} {'循环内存(KB)':<15} {'结果':<10}")
    print("-" * 80)
    
    for n in test_values:
        # 测试递归实现
        recursive_time, recursive_memory, recursive_result = measure_performance(fibonacci_recursive, n)
        
        # 测试循环实现
        iterative_time, iterative_memory, iterative_result = measure_performance(fibonacci_iterative, n)
        
        print(f"{n:<5} {recursive_time:<15.2f} {recursive_memory:<15.2f} {iterative_time:<15.2f} {iterative_memory:<15.2f} {recursive_result:<10}")
    
    print("=" * 80)
    print("性能分析报告:")
    print("1. 时间复杂度:")
    print("   - 递归实现: O(2^n)，因为每个调用都会产生两个子调用")
    print("   - 循环实现: O(n)，因为只需要一次遍历")
    print("2. 空间复杂度:")
    print("   - 递归实现: O(n)，因为递归调用栈的深度为n")
    print("   - 循环实现: O(1)，因为只使用了固定的额外空间")
    print("3. 性能差异原因:")
    print("   - 递归实现存在大量重复计算，导致时间复杂度指数增长")
    print("   - 递归调用会产生额外的栈开销，增加内存使用")
    print("   - 循环实现避免了重复计算，使用常数空间，效率更高")
    print("4. 应用场景建议:")
    print("   - 对于小n值(n < 30)，两种实现都可以使用")
    print("   - 对于大n值，建议使用循环实现或带记忆化的递归实现")
    print("   - 在需要清晰表达算法逻辑的场景，递归实现更易理解")
    print("   - 在性能敏感的场景，循环实现更为合适")

# 运行测试
if __name__ == "__main__":
    run_tests()
