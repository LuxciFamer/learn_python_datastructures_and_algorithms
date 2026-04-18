def reverse_list(lst):
    """
    使用递归方式反转列表
    
    Args:
        lst (list): 要反转的列表
    
    Returns:
        list: 反转后的新列表
    """
    # 边界情况：空列表或单元素列表直接返回
    if len(lst) <= 1:
        return lst.copy() if lst else []
    
    # 递归逻辑：将第一个元素放到最后，其余元素递归反转
    return reverse_list(lst[1:]) + [lst[0]]


# 测试函数
if __name__ == "__main__":
    # 测试空列表
    print(f"空列表: {reverse_list([])}")  # 应输出 []
    
    # 测试单元素列表
    print(f"单元素列表: {reverse_list([1])}")  # 应输出 [1]
    
    # 测试多元素列表
    print(f"多元素列表: {reverse_list([1, 2, 3, 4, 5])}")  # 应输出 [5, 4, 3, 2, 1]
    
    # 测试不同数据类型元素的列表
    print(f"不同数据类型: {reverse_list([1, 'a', 3.14, True])}")  # 应输出 [True, 3.14, 'a', 1]
    
    # 验证原列表未被修改
    original = [1, 2, 3]
    reversed_list = reverse_list(original)
    print(f"原列表: {original}")  # 应保持不变
    print(f"反转后: {reversed_list}")  # 应输出 [3, 2, 1]
