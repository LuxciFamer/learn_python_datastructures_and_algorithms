def min_edit_distance(word1, word2):
    """
    计算两个单词之间的最小编辑距离
    
    Args:
        word1: 第一个单词
        word2: 第二个单词
    
    Returns:
        int: 最小编辑代价
    """
    m, n = len(word1), len(word2)
    
    # 创建动态规划表
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 边界条件
    # 当第二个单词为空时，需要删除第一个单词的所有字符
    for i in range(1, m + 1):
        dp[i][0] = i * 20
    
    # 当第一个单词为空时，需要插入第二个单词的所有字符
    for j in range(1, n + 1):
        dp[0][j] = j * 20
    
    # 填充动态规划表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                # 字符相同，可以选择复制操作
                dp[i][j] = dp[i-1][j-1] + 5
            else:
                # 字符不同，选择代价最小的操作
                # 删除操作：删除word1的第i个字符
                delete_cost = dp[i-1][j] + 20
                # 插入操作：在word1中插入word2的第j个字符
                insert_cost = dp[i][j-1] + 20
                # 取最小值
                dp[i][j] = min(delete_cost, insert_cost)
    
    return dp[m][n]

def min_edit_distance_optimized(word1, word2):
    """
    优化空间复杂度的最小编辑距离算法
    
    Args:
        word1: 第一个单词
        word2: 第二个单词
    
    Returns:
        int: 最小编辑代价
    """
    m, n = len(word1), len(word2)
    
    # 确保m <= n，减少空间使用
    if m > n:
        word1, word2 = word2, word1
        m, n = n, m
    
    # 使用滚动数组，只保存前一行
    prev = [0] * (n + 1)
    
    # 初始化边界条件
    for j in range(n + 1):
        prev[j] = j * 20
    
    # 填充动态规划表
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        curr[0] = i * 20
        
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1] + 5
            else:
                delete_cost = prev[j] + 20
                insert_cost = curr[j-1] + 20
                curr[j] = min(delete_cost, insert_cost)
        
        prev = curr
    
    return prev[n]

def print_edit_table(word1, word2):
    """
    打印编辑距离表
    
    Args:
        word1: 第一个单词
        word2: 第二个单词
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 边界条件
    for i in range(1, m + 1):
        dp[i][0] = i * 20
    for j in range(1, n + 1):
        dp[0][j] = j * 20
    
    # 填充表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 5
            else:
                dp[i][j] = min(dp[i-1][j] + 20, dp[i][j-1] + 20)
    
    # 打印表
    print("编辑距离表:")
    print("   ", end="")
    for c in word2:
        print(f"  {c}", end="")
    print()
    
    for i in range(m + 1):
        if i == 0:
            print(" ", end="")
        else:
            print(word1[i-1], end="")
        
        for j in range(n + 1):
            print(f"{dp[i][j]:4}", end="")
        print()
    
    return dp

# 测试示例
if __name__ == "__main__":
    word1 = "algorithm"
    word2 = "alligator"
    
    print(f"计算 '{word1}' 到 '{word2}' 的最小编辑距离")
    print("=" * 50)
    
    # 打印编辑距离表
    dp = print_edit_table(word1, word2)
    
    # 计算最小编辑距离
    distance = min_edit_distance(word1, word2)
    print(f"\n最小编辑代价: {distance}")
    
    # 测试优化版本
    distance_optimized = min_edit_distance_optimized(word1, word2)
    print(f"优化版本最小编辑代价: {distance_optimized}")
    
    # 验证结果
    print("\n验证步骤:")
    print(f"单词1: {word1}")
    print(f"单词2: {word2}")
    print("编辑操作分析:")
    print("1. a → a: 复制 (5)")
    print("2. l → l: 复制 (5)")
    print("3. g → l: 删除g (20) + 插入l (20)")
    print("4. o → i: 删除o (20) + 插入i (20)")
    print("5. r → g: 删除r (20) + 插入g (20)")
    print("6. i → a: 删除i (20) + 插入a (20)")
    print("7. t → t: 复制 (5)")
    print("8. h → o: 删除h (20) + 插入o (20)")
    print("9. m → r: 删除m (20) + 插入r (20)")
    print(f"总代价: 5+5+40+40+40+40+5+40+40 = {5+5+40+40+40+40+5+40+40}")
