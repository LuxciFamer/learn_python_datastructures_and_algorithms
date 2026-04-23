def pattern_match(text, pattern):
    """查找模式在文本中出现的所有位置
    
    Args:
        text: 待搜索的文本
        pattern: 要查找的模式
    
    Returns:
        一个列表，包含模式在文本中出现的所有起始位置
    """
    if not pattern:
        return []
    
    n = len(text)
    m = len(pattern)
    positions = []
    
    # 暴力匹配算法
    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            positions.append(i)
    
    return positions

# 测试代码
if __name__ == "__main__":
    # 测试用例 1: 基本匹配
    text1 = "ABABDABACDABABCABAB"
    pattern1 = "ABABCABAB"
    print(f"文本: {text1}")
    print(f"模式: {pattern1}")
    positions1 = pattern_match(text1, pattern1)
    print(f"匹配位置: {positions1}")
    print()
    
    # 测试用例 2: 多次匹配
    text2 = "AAABAAAAABAAAABA"
    pattern2 = "AA"
    print(f"文本: {text2}")
    print(f"模式: {pattern2}")
    positions2 = pattern_match(text2, pattern2)
    print(f"匹配位置: {positions2}")
    print()
    
    # 测试用例 3: 无匹配
    text3 = "Hello, World!"
    pattern3 = "Python"
    print(f"文本: {text3}")
    print(f"模式: {pattern3}")
    positions3 = pattern_match(text3, pattern3)
    print(f"匹配位置: {positions3}")
    print()
    
    # 测试用例 4: 空模式
    text4 = "Test text"
    pattern4 = ""
    print(f"文本: {text4}")
    print(f"模式: '{pattern4}'")
    positions4 = pattern_match(text4, pattern4)
    print(f"匹配位置: {positions4}")
