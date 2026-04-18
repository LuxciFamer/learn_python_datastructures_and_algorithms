import random
import time
import statistics
import matplotlib.pyplot as plt
import numpy as np

def insertion_sort(alist, first, last):
    """
    插入排序算法
    
    参数:
        alist: 要排序的列表
        first: 排序范围的起始索引
        last: 排序范围的结束索引
    """
    for i in range(first + 1, last + 1):
        current_value = alist[i]
        position = i
        
        while position > first and alist[position - 1] > current_value:
            alist[position] = alist[position - 1]
            position -= 1
        
        alist[position] = current_value

def partition(alist, first, last):
    """
    分区函数，将列表分为两部分
    
    参数:
        alist: 要分区的列表
        first: 分区范围的起始索引
        last: 分区范围的结束索引
    
    返回值:
        基准元素最终的位置索引
    """
    # 选择第一个元素作为基准值
    pivotvalue = alist[first]
    
    # 左标记：从基准元素的下一个位置开始
    leftmark = first + 1
    # 右标记：从最后一个元素开始
    rightmark = last
    
    # 标记分区是否完成
    done = False
    
    # 分区过程
    while not done:
        # 从左向右找到第一个大于基准的元素
        while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
            leftmark = leftmark + 1
        
        # 从右向左找到第一个小于基准的元素
        while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1
        
        # 如果右标记小于左标记，说明分区完成
        if rightmark < leftmark:
            done = True
        else:
            # 交换左右标记位置的元素
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp
    
    # 将基准元素与右标记位置的元素交换
    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    
    # 返回基准元素的最终位置
    return rightmark

def quick_sort_helper(alist, first, last, threshold):
    """
    快速排序的递归辅助函数，包含插入排序优化
    
    参数:
        alist: 要排序的列表
        first: 当前排序范围的起始索引
        last: 当前排序范围的结束索引
        threshold: 切换到插入排序的阈值
    """
    # 当子列表长度小于阈值时，使用插入排序
    if last - first + 1 <= threshold:
        insertion_sort(alist, first, last)
    elif first < last:
        # 调用partition函数获取分割点
        splitpoint = partition(alist, first, last)
        
        # 递归排序左半部分（小于基准的元素）
        quick_sort_helper(alist, first, splitpoint-1, threshold)
        # 递归排序右半部分（大于基准的元素）
        quick_sort_helper(alist, splitpoint+1, last, threshold)

def quick_sort(alist, threshold=10):
    """
    快速排序主函数，包含插入排序优化
    
    参数:
        alist: 要排序的列表
        threshold: 切换到插入排序的阈值，默认为10
    """
    quick_sort_helper(alist, 0, len(alist)-1, threshold)

def generate_random_list(size, min_val=1, max_val=10000):
    """
    生成指定大小的随机整数列表
    
    参数:
        size: 列表大小
        min_val: 最小值
        max_val: 最大值
    
    返回:
        随机整数列表
    """
    return [random.randint(min_val, max_val) for _ in range(size)]

def test_sorting_algorithm(algorithm, data, threshold=None):
    """
    测试排序算法的执行时间
    
    参数:
        algorithm: 排序算法函数
        data: 要排序的数据
        threshold: 快速排序的阈值参数
    
    返回:
        执行时间（秒）
    """
    # 创建数据的副本，避免修改原始数据
    test_data = data.copy()
    
    # 记录开始时间
    start_time = time.time()
    
    # 执行排序
    if threshold is not None:
        algorithm(test_data, threshold)
    else:
        algorithm(test_data)
    
    # 记录结束时间
    end_time = time.time()
    
    # 返回执行时间
    return end_time - start_time

def run_performance_test():
    """
    运行性能测试，比较不同阈值的快速排序性能
    """
    # 测试配置
    list_size = 10000
    num_runs = 10
    thresholds = [5, 10, 15, 20, 25]
    
    # 生成随机数据
    random_data = generate_random_list(list_size)
    print(f"生成了包含 {list_size} 个随机整数的列表")
    
    # 存储测试结果
    results = {}
    
    # 运行测试
    print("\n开始运行性能测试...")
    for threshold in thresholds:
        print(f"测试阈值为 {threshold} 的快速排序...")
        times = []
        for i in range(num_runs):
            exec_time = test_sorting_algorithm(quick_sort, random_data, threshold)
            times.append(exec_time)
        results[threshold] = times
    
    # 生成报告
    print("\n" + "=" * 80)
    print("快速排序性能测试报告（不同阈值）")
    print("=" * 80)
    
    # 打印数据表格
    print("\n执行时间统计（单位：秒）:")
    print("-" * 80)
    print(f"{'阈值':<10} {'平均时间':<15} {'标准差':<15} {'最快时间':<15} {'最慢时间':<15}")
    print("-" * 80)
    
    # 准备数据用于绘图
    threshold_values = []
    avg_times = []
    std_times = []
    
    for threshold, times in results.items():
        avg_time = statistics.mean(times)
        std_time = statistics.stdev(times)
        min_time = min(times)
        max_time = max(times)
        
        threshold_values.append(threshold)
        avg_times.append(avg_time)
        std_times.append(std_time)
        
        print(f"{threshold:<10} {avg_time:<15.6f} {std_time:<15.6f} {min_time:<15.6f} {max_time:<15.6f}")
    
    print("-" * 80)
    
    # 找到最优阈值
    optimal_threshold = threshold_values[avg_times.index(min(avg_times))]
    print(f"\n最优阈值: {optimal_threshold}，平均执行时间: {min(avg_times):.6f} 秒")
    
    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    x_pos = np.arange(len(threshold_values))
    
    plt.bar(x_pos, avg_times, yerr=std_times, align='center', alpha=0.7, ecolor='black', capsize=10)
    plt.xticks(x_pos, threshold_values)
    plt.xlabel('Threshold Value')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Quicksort Performance with Different Thresholds')
    plt.ylim(0, max(avg_times) * 1.2)
    
    # 在柱状图上显示数值
    for i, v in enumerate(avg_times):
        plt.text(i, v + 0.0001, f'{v:.6f}', ha='center')
    
    # 保存图表
    plt.tight_layout()
    plt.savefig('quicksort_threshold_performance.png')
    print("\n性能对比图已保存为 'quicksort_threshold_performance.png'")
    
    # 分析和建议
    print("\n" + "=" * 80)
    print("性能分析与建议")
    print("=" * 80)
    
    print("\n理论分析:")
    print("1. 对于小型子列表，插入排序比快速排序更高效，因为:")
    print("   - 插入排序的常数因子较小")
    print("   - 避免了递归调用的开销")
    print("   - 对于近乎有序的数据表现更好")
    print("2. 最佳阈值通常在5-25之间，具体取决于硬件和数据特性")
    
    print(f"\n实际测试结果:")
    print(f"- 测试数据大小: {list_size} 个随机整数")
    print(f"- 每个阈值测试次数: {num_runs}")
    print(f"- 最优阈值: {optimal_threshold}")
    print(f"- 最优平均执行时间: {min(avg_times):.6f} 秒")

if __name__ == "__main__":
    # 测试优化后的快速排序
    test_list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    print("原始列表:", test_list)
    quick_sort(test_list, threshold=10)
    print("排序后列表:", test_list)
    
    # 运行性能测试
    run_performance_test()
