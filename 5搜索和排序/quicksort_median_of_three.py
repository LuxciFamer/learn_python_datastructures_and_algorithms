import random
import time
import statistics
import matplotlib.pyplot as plt
import numpy as np
import sys

# 增加递归深度限制
sys.setrecursionlimit(1000000)

def partition_original(alist, first, last):
    """
    原始分区函数，使用第一个元素作为基准值
    
    参数:
        alist: 要分区的列表
        first: 分区范围的起始索引
        last: 分区范围的结束索引
    
    返回值:
        基准元素最终的位置索引, 比较次数, 交换次数
    """
    # 选择第一个元素作为基准值
    pivotvalue = alist[first]
    
    # 左标记：从基准元素的下一个位置开始
    leftmark = first + 1
    # 右标记：从最后一个元素开始
    rightmark = last
    
    # 标记分区是否完成
    done = False
    
    # 统计比较和交换次数
    comparisons = 0
    swaps = 0
    
    # 分区过程
    while not done:
        # 从左向右找到第一个大于基准的元素
        while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
            leftmark = leftmark + 1
            comparisons += 1
        comparisons += 1  # 最后一次比较
        
        # 从右向左找到第一个小于基准的元素
        while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1
            comparisons += 1
        comparisons += 1  # 最后一次比较
        
        # 如果右标记小于左标记，说明分区完成
        if rightmark < leftmark:
            done = True
        else:
            # 交换左右标记位置的元素
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp
            swaps += 1
    
    # 将基准元素与右标记位置的元素交换
    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    swaps += 1
    
    # 返回基准元素的最终位置和统计信息
    return rightmark, comparisons, swaps

def median_of_three(alist, first, last):
    """
    三数取中法，选择第一个、中间和最后一个元素的中位数作为基准值
    
    参数:
        alist: 要排序的列表
        first: 起始索引
        last: 结束索引
    
    返回值:
        中位数的索引
    """
    mid = (first + last) // 2
    
    # 对三个元素进行排序
    if alist[first] > alist[mid]:
        alist[first], alist[mid] = alist[mid], alist[first]
    if alist[first] > alist[last]:
        alist[first], alist[last] = alist[last], alist[first]
    if alist[mid] > alist[last]:
        alist[mid], alist[last] = alist[last], alist[mid]
    
    # 将中位数移到倒数第二个位置
    alist[mid], alist[last-1] = alist[last-1], alist[mid]
    return last-1

def partition_median(alist, first, last):
    """
    分区函数，使用三数取中法选择基准值
    
    参数:
        alist: 要分区的列表
        first: 分区范围的起始索引
        last: 分区范围的结束索引
    
    返回值:
        基准元素最终的位置索引, 比较次数, 交换次数
    """
    # 使用三数取中法选择基准值
    pivot_index = median_of_three(alist, first, last)
    pivotvalue = alist[pivot_index]
    
    # 交换基准值到第一个位置
    alist[first], alist[pivot_index] = alist[pivot_index], alist[first]
    
    # 左标记：从基准元素的下一个位置开始
    leftmark = first + 1
    # 右标记：从最后一个元素开始
    rightmark = last
    
    # 标记分区是否完成
    done = False
    
    # 统计比较和交换次数
    comparisons = 3  # 三数取中的三次比较
    swaps = 2  # 三数取中的两次交换
    
    # 分区过程
    while not done:
        # 从左向右找到第一个大于基准的元素
        while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
            leftmark = leftmark + 1
            comparisons += 1
        comparisons += 1  # 最后一次比较
        
        # 从右向左找到第一个小于基准的元素
        while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1
            comparisons += 1
        comparisons += 1  # 最后一次比较
        
        # 如果右标记小于左标记，说明分区完成
        if rightmark < leftmark:
            done = True
        else:
            # 交换左右标记位置的元素
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp
            swaps += 1
    
    # 将基准元素与右标记位置的元素交换
    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    swaps += 1
    
    # 返回基准元素的最终位置和统计信息
    return rightmark, comparisons, swaps

def quick_sort_helper_original(alist, first, last):
    """
    原始快速排序的递归辅助函数
    
    参数:
        alist: 要排序的列表
        first: 当前排序范围的起始索引
        last: 当前排序范围的结束索引
    
    返回值:
        比较次数, 交换次数
    """
    comparisons = 0
    swaps = 0
    
    # 只有当起始索引小于结束索引时才需要排序
    if first < last:
        # 调用partition函数获取分割点
        splitpoint, comp, swap = partition_original(alist, first, last)
        comparisons += comp
        swaps += swap
        
        # 递归排序左半部分（小于基准的元素）
        comp_left, swap_left = quick_sort_helper_original(alist, first, splitpoint-1)
        comparisons += comp_left
        swaps += swap_left
        
        # 递归排序右半部分（大于基准的元素）
        comp_right, swap_right = quick_sort_helper_original(alist, splitpoint+1, last)
        comparisons += comp_right
        swaps += swap_right
    
    return comparisons, swaps

def quick_sort_original(alist):
    """
    原始快速排序主函数
    
    参数:
        alist: 要排序的列表
    
    返回值:
        比较次数, 交换次数
    """
    return quick_sort_helper_original(alist, 0, len(alist)-1)

def quick_sort_helper_median(alist, first, last):
    """
    使用三数取中法的快速排序递归辅助函数
    
    参数:
        alist: 要排序的列表
        first: 当前排序范围的起始索引
        last: 当前排序范围的结束索引
    
    返回值:
        比较次数, 交换次数
    """
    comparisons = 0
    swaps = 0
    
    # 只有当起始索引小于结束索引时才需要排序
    if first < last:
        # 调用partition函数获取分割点
        splitpoint, comp, swap = partition_median(alist, first, last)
        comparisons += comp
        swaps += swap
        
        # 递归排序左半部分（小于基准的元素）
        comp_left, swap_left = quick_sort_helper_median(alist, first, splitpoint-1)
        comparisons += comp_left
        swaps += swap_left
        
        # 递归排序右半部分（大于基准的元素）
        comp_right, swap_right = quick_sort_helper_median(alist, splitpoint+1, last)
        comparisons += comp_right
        swaps += swap_right
    
    return comparisons, swaps

def quick_sort_median(alist):
    """
    使用三数取中法的快速排序主函数
    
    参数:
        alist: 要排序的列表
    
    返回值:
        比较次数, 交换次数
    """
    return quick_sort_helper_median(alist, 0, len(alist)-1)

def generate_test_data(size, data_type):
    """
    生成不同类型的测试数据
    
    参数:
        size: 数据大小
        data_type: 数据类型 ('random', 'sorted', 'reversed', 'duplicates')
    
    返回:
        测试数据列表
    """
    if data_type == 'random':
        return [random.randint(1, 10000) for _ in range(size)]
    elif data_type == 'sorted':
        return list(range(size))
    elif data_type == 'reversed':
        return list(range(size, 0, -1))
    elif data_type == 'duplicates':
        # 生成包含重复元素的数据
        data = []
        for i in range(size):
            data.append(random.randint(1, 100))  # 只有100个不同的值
        return data
    else:
        raise ValueError("Invalid data type")

def test_sorting_algorithm(algorithm, data):
    """
    测试排序算法的性能
    
    参数:
        algorithm: 排序算法函数
        data: 要排序的数据
    
    返回:
        执行时间（秒）, 比较次数, 交换次数
    """
    # 创建数据的副本，避免修改原始数据
    test_data = data.copy()
    
    # 记录开始时间
    start_time = time.time()
    
    # 执行排序并获取比较和交换次数
    comparisons, swaps = algorithm(test_data)
    
    # 记录结束时间
    end_time = time.time()
    
    # 返回执行时间和统计信息
    return end_time - start_time, comparisons, swaps

def run_comparison_test():
    """
    运行对比实验，分析两种基准值选取策略的性能差异
    """
    # 测试配置
    sizes = [1000, 5000, 10000]  # 小规模、中等规模、大规模
    data_types = ['random', 'sorted', 'reversed', 'duplicates']  # 不同类型的测试数据
    num_runs = 5  # 每种配置运行5次
    
    # 存储测试结果
    results = {}
    
    # 运行测试
    print("开始运行对比实验...")
    for size in sizes:
        results[size] = {}
        for data_type in data_types:
            results[size][data_type] = {}
            print(f"测试大小: {size}, 数据类型: {data_type}")
            
            # 生成测试数据
            data = generate_test_data(size, data_type)
            
            # 测试原始快速排序
            original_times = []
            original_comparisons = []
            original_swaps = []
            
            # 测试三数取中法快速排序
            median_times = []
            median_comparisons = []
            median_swaps = []
            
            for i in range(num_runs):
                # 测试原始快速排序
                time_orig, comp_orig, swap_orig = test_sorting_algorithm(quick_sort_original, data)
                original_times.append(time_orig)
                original_comparisons.append(comp_orig)
                original_swaps.append(swap_orig)
                
                # 测试三数取中法快速排序
                time_med, comp_med, swap_med = test_sorting_algorithm(quick_sort_median, data)
                median_times.append(time_med)
                median_comparisons.append(comp_med)
                median_swaps.append(swap_med)
            
            # 计算平均值
            results[size][data_type]['original'] = {
                'time': statistics.mean(original_times),
                'comparisons': statistics.mean(original_comparisons),
                'swaps': statistics.mean(original_swaps)
            }
            
            results[size][data_type]['median'] = {
                'time': statistics.mean(median_times),
                'comparisons': statistics.mean(median_comparisons),
                'swaps': statistics.mean(median_swaps)
            }
    
    # 生成报告
    print("\n" + "=" * 100)
    print("快速排序基准值选取策略对比报告")
    print("=" * 100)
    
    # 打印数据表格
    for size in sizes:
        print(f"\n数组大小: {size}")
        print("-" * 100)
        print(f"{'数据类型':<15} {'策略':<10} {'平均时间(秒)':<15} {'平均比较次数':<15} {'平均交换次数':<15}")
        print("-" * 100)
        
        for data_type in data_types:
            # 原始策略
            orig = results[size][data_type]['original']
            print(f"{data_type:<15} {'原始':<10} {orig['time']:<15.6f} {orig['comparisons']:<15.0f} {orig['swaps']:<15.0f}")
            
            # 三数取中法
            med = results[size][data_type]['median']
            print(f"{data_type:<15} {'三数取中':<10} {med['time']:<15.6f} {med['comparisons']:<15.0f} {med['swaps']:<15.0f}")
        
        print("-" * 100)
    
    # 生成性能对比图
    generate_performance_plots(results)
    
    # 分析和结论
    print("\n" + "=" * 100)
    print("性能分析与结论")
    print("=" * 100)
    
    print("\n分析:")
    print("1. 对于随机数据:")
    print("   - 两种策略的性能差异较小")
    print("   - 三数取中法可能略优，因为它选择了更接近中位数的基准值")
    
    print("\n2. 对于已排序或逆序数据:")
    print("   - 原始策略会退化为O(n^2)时间复杂度")
    print("   - 三数取中法显著优于原始策略，避免了最坏情况")
    
    print("\n3. 对于包含重复元素的数据:")
    print("   - 三数取中法通常表现更好")
    
    print("\n4. 随着数据规模增大:")
    print("   - 两种策略的性能差异更加明显")
    print("   - 三数取中法的优势更加突出")
    
    print("\n结论:")
    print("- 三数取中法是一种有效的基准值选取策略，可以显著提高快速排序在各种输入条件下的性能")
    print("- 特别是对于已排序、逆序或包含重复元素的数据，三数取中法可以避免快速排序的最坏情况")
    print("- 对于随机数据，三数取中法也能提供一定的性能提升")
    print("- 建议在实际应用中使用三数取中法作为快速排序的基准值选取策略")

def generate_performance_plots(results):
    """
    生成性能对比图表
    
    参数:
        results: 测试结果
    """
    # 为每种数据类型生成图表
    data_types = ['random', 'sorted', 'reversed', 'duplicates']
    metrics = ['time', 'comparisons', 'swaps']
    metric_names = {'time': '执行时间 (秒)', 'comparisons': '比较次数', 'swaps': '交换次数'}
    
    for data_type in data_types:
        for metric in metrics:
            plt.figure(figsize=(10, 6))
            
            sizes = list(results.keys())
            original_values = [results[size][data_type]['original'][metric] for size in sizes]
            median_values = [results[size][data_type]['median'][metric] for size in sizes]
            
            plt.plot(sizes, original_values, marker='o', label='原始策略')
            plt.plot(sizes, median_values, marker='s', label='三数取中法')
            
            plt.xlabel('数组大小')
            plt.ylabel(metric_names[metric])
            plt.title(f'{data_type}数据 - {metric_names[metric]}对比')
            plt.legend()
            plt.grid(True)
            
            # 保存图表
            filename = f'quicksort_{data_type}_{metric}.png'
            plt.tight_layout()
            plt.savefig(filename)
            print(f"图表已保存为 '{filename}'")

if __name__ == "__main__":
    # 测试基本功能
    test_list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    print("原始列表:", test_list)
    
    # 测试原始快速排序
    test_list1 = test_list.copy()
    comp1, swap1 = quick_sort_original(test_list1)
    print("原始策略排序后:", test_list1)
    print(f"比较次数: {comp1}, 交换次数: {swap1}")
    
    # 测试三数取中法快速排序
    test_list2 = test_list.copy()
    comp2, swap2 = quick_sort_median(test_list2)
    print("三数取中法排序后:", test_list2)
    print(f"比较次数: {comp2}, 交换次数: {swap2}")
    
    # 运行对比实验
    run_comparison_test()
