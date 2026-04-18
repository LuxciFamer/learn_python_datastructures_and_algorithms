def classic_hash(input_data, hash_size=32):
    """
    经典散列函数算法
    
    Args:
        input_data: 输入数据（字符串、数字或二进制数据）
        hash_size: 散列值位数（32或64）
    
    Returns:
        int: 固定长度的散列值
    """
    # 处理不同数据类型
    if isinstance(input_data, int):
        input_data = str(input_data)
    elif isinstance(input_data, bytes):
        input_data = input_data.decode('utf-8', errors='replace')
    elif not isinstance(input_data, str):
        input_data = str(input_data)
    
    # 初始化散列值
    if hash_size == 64:
        hash_value = 0x1505150515051505
        prime = 0x1000193  # 64位质数
    else:  # 32位
        hash_value = 0x811c9dc5
        prime = 0x1000193  # 32位质数
    
    # 处理输入数据
    for char in input_data:
        # 获取字符的ASCII值
        char_code = ord(char)
        
        # 结合位运算、模运算和非线性变换
        hash_value ^= char_code
        hash_value *= prime
        
        # 非线性变换：循环移位
        if hash_size == 64:
            hash_value = (hash_value << 13) | (hash_value >> 51)
        else:
            hash_value = (hash_value << 13) | (hash_value >> 19)
    
    # 确保散列值在指定范围内
    if hash_size == 64:
        return hash_value & 0xFFFFFFFFFFFFFFFF
    else:
        return hash_value & 0xFFFFFFFF

def test_hash_function():
    """
    测试散列函数
    """
    test_cases = [
        # 基本测试
        "hello",
        "world",
        "Hello",  # 大小写不同
        "hello!",  # 特殊字符
        
        # 长字符串
        "a" * 1000,
        "abcdefghijklmnopqrstuvwxyz" * 50,
        
        # 数字混合
        "12345",
        "abc123",
        12345,
        
        # 特殊字符
        "!@#$%^&*()",
        "你好世界",  # 中文字符
        
        # 重复模式
        "abababababab",
        "aaaaa",
        
        # 空字符串
        ""
    ]
    
    print("测试32位散列函数:")
    print("=" * 80)
    print(f"{'输入':<40} {'散列值':<20} {'十六进制':<20}")
    print("=" * 80)
    
    hash_values = []
    for test in test_cases:
        hash_val = classic_hash(test, 32)
        hash_values.append(hash_val)
        print(f"{str(test)[:39]:<40} {hash_val:<20} {hex(hash_val):<20}")
    
    print("\n测试64位散列函数:")
    print("=" * 80)
    print(f"{'输入':<40} {'散列值':<20} {'十六进制':<20}")
    print("=" * 80)
    
    hash_values_64 = []
    for test in test_cases:
        hash_val = classic_hash(test, 64)
        hash_values_64.append(hash_val)
        print(f"{str(test)[:39]:<40} {hash_val:<20} {hex(hash_val):<20}")
    
    # 测试雪崩效应
    print("\n测试雪崩效应:")
    print("=" * 80)
    base_str = "hello world"
    base_hash = classic_hash(base_str)
    
    for i, char in enumerate(base_str):
        # 对每个字符进行微小修改
        modified_str = base_str[:i] + chr((ord(char) + 1) % 256) + base_str[i+1:]
        modified_hash = classic_hash(modified_str)
        # 计算不同位的数量
        diff_bits = bin(base_hash ^ modified_hash).count('1')
        print(f"修改位置 {i}: 不同位数 = {diff_bits}/32")
    
    # 分析分布特性
    print("\n分析分布特性:")
    print("=" * 80)
    
    # 计算散列值的分布
    buckets = [0] * 10
    for hash_val in hash_values:
        bucket = hash_val % 10
        buckets[bucket] += 1
    
    print("32位散列值分布:")
    for i, count in enumerate(buckets):
        print(f"桶 {i}: {count} 个")
    
    # 计算碰撞率
    unique_hashes = len(set(hash_values))
    collision_rate = (len(hash_values) - unique_hashes) / len(hash_values) * 100
    print(f"\n32位散列碰撞率: {collision_rate:.2f}%")
    
    # 64位散列值分布
    buckets_64 = [0] * 10
    for hash_val in hash_values_64:
        bucket = hash_val % 10
        buckets_64[bucket] += 1
    
    print("\n64位散列值分布:")
    for i, count in enumerate(buckets_64):
        print(f"桶 {i}: {count} 个")
    
    unique_hashes_64 = len(set(hash_values_64))
    collision_rate_64 = (len(hash_values_64) - unique_hashes_64) / len(hash_values_64) * 100
    print(f"\n64位散列碰撞率: {collision_rate_64:.2f}%")

if __name__ == "__main__":
    test_hash_function()
