#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KMP图实现

本模块实现了 KMP 算法的图表示，支持以下特性：
1. 基于图结构的 KMP 算法实现
2. 自动构建 KMP 图，包括状态转移和失配链接
3. 使用 KMP 图进行文本匹配
4. 详细的代码注释和复杂度分析
5. 测试用例
"""

from typing import Dict, List, Any


class KMPGraph:
    """KMP图数据结构类
    
    实现了 KMP 算法的图表示，包括状态转移和失配链接
    """
    
    def __init__(self):
        """初始化 KMP 图
        """
        self.adjacency_list: Dict[int, List[tuple]] = {}  # 状态转移，格式: {状态: [(下一个状态, 字符), ...]}
        self.mismatch_links: Dict[int, int] = {}  # 失配链接
        self.pattern_length: int = 0  # 模式长度
    
    def build_kmp_graph(self, pattern: str):
        """根据模式创建完整的 KMP 图
        
        Args:
            pattern: 要匹配的模式字符串
        """
        # 清空现有图结构
        self.adjacency_list = {}
        self.mismatch_links = {}
        self.pattern_length = len(pattern)
        
        n = len(pattern)
        
        # 创建状态节点（状态 0 到 n）
        for i in range(n + 1):
            self.adjacency_list[i] = []
        
        # 构建状态转移
        for state in range(n):
            char = pattern[state]
            # 添加状态转移边
            self.adjacency_list[state].append((state + 1, char))
        
        # 构建失配链接
        self.mismatch_links[0] = 0
        
        # 使用前缀函数计算失配链接
        for i in range(1, n + 1):
            j = self.mismatch_links[i - 1]
            while j > 0 and (i - 1 >= len(pattern) or pattern[i - 1] != pattern[j]):
                j = self.mismatch_links[j]
            if i - 1 < len(pattern) and pattern[i - 1] == pattern[j]:
                j += 1
            self.mismatch_links[i] = j
    
    def match_text(self, text: str) -> bool:
        """使用 KMP 图运行文本，检查匹配是否存在
        
        Args:
            text: 要匹配的文本
        
        Returns:
            bool: 如果模式在文本中存在，返回 True，否则返回 False
        """
        if self.pattern_length == 0:
            return True
        
        current_state = 0
        
        for char in text:
            # 尝试找到当前字符的转移
            found = False
            for neighbor, edge_char in self.adjacency_list[current_state]:
                if edge_char == char:
                    current_state = neighbor
                    found = True
                    break
            
            # 如果没有找到转移，使用失配链接
            if not found:
                while current_state > 0:
                    current_state = self.mismatch_links[current_state]
                    # 再次尝试找到转移
                    for neighbor, edge_char in self.adjacency_list[current_state]:
                        if edge_char == char:
                            current_state = neighbor
                            found = True
                            break
                    if found:
                        break
            
            # 检查是否达到终止状态
            if current_state == self.pattern_length:
                return True
        
        return False
    
    def __str__(self) -> str:
        """字符串表示
        
        Returns:
            str: KMP 图的字符串表示
        """
        result = []
        result.append("KMP 图结构:")
        for vertex, edges in self.adjacency_list.items():
            edge_str = []
            for neighbor, char in edges:
                edge_str.append(f"{neighbor}({char})")
            result.append(f"状态 {vertex}: {', '.join(edge_str)}")
        
        result.append("\n失配链接:")
        for state, link in self.mismatch_links.items():
            result.append(f"状态 {state} -> {link}")
        
        return "\n".join(result)


def test_kmp_graph():
    """测试 KMP 图实现"""
    print("=== 测试 KMP 图实现 ===")
    
    # 测试1: 基本模式匹配
    print("\n1. 测试基本模式匹配:")
    pattern1 = "ABABCABAB"
    kmp_graph1 = KMPGraph()
    kmp_graph1.build_kmp_graph(pattern1)
    print(f"模式: {pattern1}")
    print(kmp_graph1)
    
    text1 = "ABABDABACDABABCABAB"
    print(f"文本: {text1}")
    result1 = kmp_graph1.match_text(text1)
    print(f"匹配结果: {result1}")
    
    # 测试2: 多次匹配
    print("\n2. 测试多次匹配:")
    pattern2 = "AA"
    kmp_graph2 = KMPGraph()
    kmp_graph2.build_kmp_graph(pattern2)
    print(f"模式: {pattern2}")
    print(kmp_graph2)
    
    text2 = "AAABAAAAABAAAABA"
    print(f"文本: {text2}")
    result2 = kmp_graph2.match_text(text2)
    print(f"匹配结果: {result2}")
    
    # 测试3: 无匹配
    print("\n3. 测试无匹配:")
    pattern3 = "Python"
    kmp_graph3 = KMPGraph()
    kmp_graph3.build_kmp_graph(pattern3)
    print(f"模式: {pattern3}")
    
    text3 = "Hello, World!"
    print(f"文本: {text3}")
    result3 = kmp_graph3.match_text(text3)
    print(f"匹配结果: {result3}")
    
    # 测试4: 空模式
    print("\n4. 测试空模式:")
    pattern4 = ""
    kmp_graph4 = KMPGraph()
    kmp_graph4.build_kmp_graph(pattern4)
    print(f"模式: '{pattern4}'")
    
    text4 = "Test text"
    print(f"文本: {text4}")
    result4 = kmp_graph4.match_text(text4)
    print(f"匹配结果: {result4}")


if __name__ == "__main__":
    test_kmp_graph()
