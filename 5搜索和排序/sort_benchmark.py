import random
import time
import statistics
import matplotlib.pyplot as plt
import numpy as np
import os

# 导入排序算法
from bubbleSort import bubbleSort
from quickSort import quickSort
from mergeSort import mergeSort
from shellSort import shellSort

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

def test_sorting_algorithm(algorithm, data):
    """
    测试排序算法的执行时间
    
    参数:
        algorithm: 排序算法函数
        data: 要排序的数据
    
    返回:
        执行时间（秒）
    """
    # 创建数据的副本，避免修改原始数据
    test_data = data.copy()
    
    # 记录开始时间
    start_time = time.time()
    
    # 执行排序
    algorithm(test_data)
    
    # 记录结束时间
    end_time = time.time()
    
    # 返回执行时间
    return end_time - start_time

def run_benchmark():
    """
    运行基准测试并生成报告
    """
    # 测试配置
    list_size = 500
    num_runs = 10
    
    # 生成随机数据
    random_data = generate_random_list(list_size)
    print(f"生成了包含 {list_size} 个随机整数的列表")
    
    # 定义要测试的排序算法
    algorithms = {
        "bubble": bubbleSort,
        "quick": quickSort,
        "merge": mergeSort,
        "shell": shellSort
    }
    
    # 存储测试结果
    results = {}
    
    # 运行测试
    print("\n开始运行基准测试...")
    for name, algorithm in algorithms.items():
        print(f"测试 {name} 排序...")
        times = []
        for i in range(num_runs):
            exec_time = test_sorting_algorithm(algorithm, random_data)
            times.append(exec_time)
        results[name] = times
    
    # 生成报告
    print("\n" + "=" * 80)
    print("排序算法性能基准测试报告")
    print("=" * 80)
    
    # 打印数据表格
    print("\n执行时间统计（单位：秒）:")
    print("-" * 80)
    print(f"{'算法':<10} {'平均时间':<15} {'标准差':<15} {'最快时间':<15} {'最慢时间':<15}")
    print("-" * 80)
    
    # 准备数据用于绘图
    algorithm_names = []
    avg_times = []
    std_times = []
    
    for name, times in results.items():
        avg_time = statistics.mean(times)
        std_time = statistics.stdev(times)
        min_time = min(times)
        max_time = max(times)
        
        algorithm_names.append(name)
        avg_times.append(avg_time)
        std_times.append(std_time)
        
        print(f"{name:<10} {avg_time:<15.6f} {std_time:<15.6f} {min_time:<15.6f} {max_time:<15.6f}")
    
    print("-" * 80)
    
    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    x_pos = np.arange(len(algorithm_names))
    
    plt.bar(x_pos, avg_times, yerr=std_times, align='center', alpha=0.7, ecolor='black', capsize=10)
    plt.xticks(x_pos, algorithm_names)
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Sorting Algorithm Performance Comparison')
    plt.ylim(0, max(avg_times) * 1.2)
    
    # 在柱状图上显示数值
    for i, v in enumerate(avg_times):
        plt.text(i, v + 0.0001, f'{v:.6f}', ha='center')
    
    # 保存图表
    plt.tight_layout()
    # 获取脚本所在目录的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建完整的图片保存路径
    image_path = os.path.join(script_dir, 'sort_benchmark_results.png')
    plt.savefig(image_path)
    print(f"\n性能对比图已保存为 '{image_path}'")
    
    # 分析和建议
    print("\n" + "=" * 80)
    print("性能分析与建议")
    print("=" * 80)
    
    # 排序算法按平均时间排序
    sorted_algorithms = sorted(results.items(), key=lambda x: statistics.mean(x[1]))
    
    print("\n算法性能排名（从快到慢）:")
    for i, (name, times) in enumerate(sorted_algorithms, 1):
        avg_time = statistics.mean(times)
        print(f"{i}. {name} 排序: {avg_time:.6f} 秒")
    
    print("\n时间复杂度分析:")
    print("- 冒泡排序: O(n^2) - 最坏、平均情况")
    print("- 快速排序: O(n^2) - 最坏情况，O(n log n) - 平均情况")
    print("- 归并排序: O(n log n) - 最坏、平均情况")
    print("- 希尔排序: O(n log^2 n) - 平均情况")
    
    print("\n实际应用建议:")
    print("1. 对于小型数据集（n < 1000），希尔排序可能更为高效")
    print("2. 对于大型数据集，快速排序、归并排序或希尔排序是更好的选择")
    print("3. 快速排序在平均情况下表现优异，但最坏情况可能退化为O(n^2)")
    print("4. 归并排序具有稳定的O(n log n)性能，但需要额外的存储空间")
    print("5. 希尔排序在实践中通常比插入排序和冒泡排序快得多")
    
    print("\n测试环境信息:")
    print(f"- 测试数据大小: {list_size} 个随机整数")
    print(f"- 每个算法运行次数: {num_runs}")
    print("- 数据范围: 1-10000")

if __name__ == "__main__":
    run_benchmark()
