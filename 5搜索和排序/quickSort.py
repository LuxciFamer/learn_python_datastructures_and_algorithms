"""
快速排序算法实现

快速排序是一种高效的排序算法，采用分治法策略
它的基本思想是：选择一个基准元素，将列表分为两部分，
小于基准的元素放在左边，大于基准的元素放在右边，
然后递归地对这两部分进行排序
"""

def quickSort(alist):
    """
    快速排序主函数
    
    参数:
        alist: 要排序的列表
    
    工作原理:
        1. 调用辅助函数quickSortHelper开始排序
        2. 初始时，排序范围是整个列表（从索引0到最后一个元素）
    """
    # 调用辅助函数，传入列表、起始索引和结束索引
    quickSortHelper(alist, 0, len(alist)-1)

def quickSortHelper(alist, first, last):
    """
    快速排序的递归辅助函数
    
    参数:
        alist: 要排序的列表
        first: 当前排序范围的起始索引
        last: 当前排序范围的结束索引
    
    工作原理:
        1. 检查当前范围是否有效（起始索引小于结束索引）
        2. 如果有效，调用partition函数进行分区
        3. 递归地对分区后的左半部分进行排序
        4. 递归地对分区后的右半部分进行排序
    """
    # 只有当起始索引小于结束索引时才需要排序
    if first < last:
        # 调用partition函数获取分割点
        # 分割点是基准元素最终的位置
        splitpoint = partition(alist, first, last)
        
        # 递归排序左半部分（小于基准的元素）
        quickSortHelper(alist, first, splitpoint-1)
        # 递归排序右半部分（大于基准的元素）
        quickSortHelper(alist, splitpoint+1, last)

def partition(alist, first, last):
    """
    分区函数，将列表分为两部分
    
    参数:
        alist: 要分区的列表
        first: 分区范围的起始索引
        last: 分区范围的结束索引
    
    返回值:
        基准元素最终的位置索引
    
    工作原理:
        1. 选择第一个元素作为基准
        2. 从左向右找到第一个大于基准的元素
        3. 从右向左找到第一个小于基准的元素
        4. 交换这两个元素
        5. 重复步骤2-4，直到左右标记交叉
        6. 将基准元素与右标记位置的元素交换
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
        # 当左标记不超过右标记且当前元素小于等于基准时，继续向右移动
        while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
            leftmark = leftmark + 1
        
        # 从右向左找到第一个小于基准的元素
        # 当右标记不小于左标记且当前元素大于等于基准时，继续向左移动
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
    # 这样基准元素就位于正确的位置，左边的元素都小于它，右边的元素都大于它
    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    
    # 返回基准元素的最终位置
    return rightmark

# 测试代码
if __name__ == "__main__":
    # 创建一个测试列表
    test_list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    print("原始列表:", test_list)
    
    # 调用快速排序函数
    quickSort(test_list)
    
    # 打印排序后的列表
    print("排序后列表:", test_list)

"""
快速排序算法分析：

1. 时间复杂度：
   - 最佳情况：O(n log n) - 每次分区都将列表均匀分为两部分
   - 平均情况：O(n log n) - 大多数情况下的性能
   - 最坏情况：O(n²) - 当列表已经有序或逆序时
   
2. 空间复杂度：
   - O(log n) - 递归调用栈的深度
   
3. 适用场景：
   - 适用于大型数据集
   - 适用于需要原地排序的场景
   - 适用于对平均性能要求较高的场景
   
4. 注意事项：
   - 对于小规模数据集，插入排序可能更高效
   - 对于几乎有序的数据集，快速排序可能退化为O(n²)时间复杂度
   - 可以通过随机选择基准元素或使用三数取中法来改善最坏情况的性能
   
5. 算法优势：
   - 原地排序，不需要额外的存储空间
   - 平均情况下性能优异
   - 对于大多数实际应用场景表现良好
"""
