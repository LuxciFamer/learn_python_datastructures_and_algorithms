#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基于宽度优先搜索（BFS）的最短路径算法

本模块实现了一个功能完善的BFS算法，用于计算无向无权图中所有顶点对之间的最短路径
"""

from typing import Dict, List, Optional, Any
from collections import deque


class Graph:
    """图数据结构类
    
    支持无向无权图的创建与管理
    """
    
    def __init__(self):
        """初始化图"""
        self.adjacency_list: Dict[Any, List[Any]] = {}
    
    def add_vertex(self, vertex: Any) -> None:
        """添加顶点
        
        Args:
            vertex: 顶点标识符
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, start: Any, end: Any) -> None:
        """添加边
        
        Args:
            start: 起始顶点
            end: 结束顶点
        """
        # 确保顶点存在
        self.add_vertex(start)
        self.add_vertex(end)
        
        # 添加边（无向图）
        if end not in self.adjacency_list[start]:
            self.adjacency_list[start].append(end)
        if start not in self.adjacency_list[end]:
            self.adjacency_list[end].append(start)
    
    def get_vertices(self) -> List[Any]:
        """获取所有顶点
        
        Returns:
            List[Any]: 顶点列表
        """
        return list(self.adjacency_list.keys())
    
    def __str__(self) -> str:
        """字符串表示
        
        Returns:
            str: 图的字符串表示
        """
        result = []
        for vertex, neighbors in self.adjacency_list.items():
            result.append(f"{vertex}: {neighbors}")
        return "\n".join(result)


def compute_all_pairs_shortest_paths(graph: Graph) -> List[List[int]]:
    """计算所有顶点对之间的最短路径
    
    Args:
        graph (Graph): 无向无权图
        
    Returns:
        List[List[int]]: 距离矩阵，dist[i][j]表示顶点i到顶点j的最短路径长度
        若不存在路径，值为-1
        
    时间复杂度: O(V * (V + E))，其中V是顶点数，E是边数
    空间复杂度: O(V^2)，用于存储距离矩阵
    """
    vertices = graph.get_vertices()
    n = len(vertices)
    
    # 处理空图情况
    if n == 0:
        return []
    
    # 创建顶点到索引的映射
    vertex_to_index = {vertex: i for i, vertex in enumerate(vertices)}
    
    # 初始化距离矩阵，默认值为-1（表示不可达）
    dist = [[-1 for _ in range(n)] for _ in range(n)]
    
    # 对每个顶点执行BFS
    for i, start_vertex in enumerate(vertices):
        # 起点到自身的距离为0
        dist[i][i] = 0
        
        # 使用队列进行BFS
        queue = deque()
        queue.append(start_vertex)
        
        while queue:
            current = queue.popleft()
            current_index = vertex_to_index[current]
            
            # 遍历所有邻居
            for neighbor in graph.adjacency_list[current]:
                neighbor_index = vertex_to_index[neighbor]
                # 如果邻居未访问过（距离为-1）
                if dist[i][neighbor_index] == -1:
                    # 距离为当前顶点距离+1
                    dist[i][neighbor_index] = dist[i][current_index] + 1
                    queue.append(neighbor)
    
    return dist


def print_distance_matrix(dist: List[List[int]], vertices: List[Any]) -> None:
    """打印距离矩阵
    
    Args:
        dist (List[List[int]]): 距离矩阵
        vertices (List[Any]): 顶点列表
    """
    n = len(vertices)
    if n == 0:
        print("空图，无距离矩阵")
        return
    
    # 打印表头
    print("\n距离矩阵:")
    print("   ", end="")
    for vertex in vertices:
        print(f"{vertex:4}", end="")
    print()
    
    # 打印每行
    for i, vertex in enumerate(vertices):
        print(f"{vertex:3}", end="")
        for j in range(n):
            print(f"{dist[i][j]:4}", end="")
        print()


def test_all_pairs_shortest_paths():
    """测试所有顶点对之间的最短路径计算"""
    print("=== 测试所有顶点对之间的最短路径 ===")
    
    # 测试1: 简单图
    print("\n1. 测试简单图:")
    graph1 = Graph()
    graph1.add_edge(0, 1)
    graph1.add_edge(0, 2)
    graph1.add_edge(1, 3)
    graph1.add_edge(2, 3)
    graph1.add_edge(3, 4)
    
    print("图结构:")
    print(graph1)
    
    dist1 = compute_all_pairs_shortest_paths(graph1)
    print_distance_matrix(dist1, graph1.get_vertices())
    
    # 测试2: 树结构
    print("\n2. 测试树结构:")
    graph2 = Graph()
    graph2.add_edge('A', 'B')
    graph2.add_edge('A', 'C')
    graph2.add_edge('B', 'D')
    graph2.add_edge('B', 'E')
    graph2.add_edge('C', 'F')
    graph2.add_edge('C', 'G')
    
    print("图结构:")
    print(graph2)
    
    dist2 = compute_all_pairs_shortest_paths(graph2)
    print_distance_matrix(dist2, graph2.get_vertices())
    
    # 测试3: 含孤立顶点的图
    print("\n3. 测试含孤立顶点的图:")
    graph3 = Graph()
    graph3.add_edge(0, 1)
    graph3.add_edge(1, 2)
    graph3.add_vertex(3)  # 孤立顶点
    graph3.add_vertex(4)  # 孤立顶点
    
    print("图结构:")
    print(graph3)
    
    dist3 = compute_all_pairs_shortest_paths(graph3)
    print_distance_matrix(dist3, graph3.get_vertices())
    
    # 测试4: 完全图
    print("\n4. 测试完全图:")
    graph4 = Graph()
    for i in range(4):
        for j in range(i+1, 4):
            graph4.add_edge(i, j)
    
    print("图结构:")
    print(graph4)
    
    dist4 = compute_all_pairs_shortest_paths(graph4)
    print_distance_matrix(dist4, graph4.get_vertices())
    
    # 测试5: 空图
    print("\n5. 测试空图:")
    graph5 = Graph()
    dist5 = compute_all_pairs_shortest_paths(graph5)
    print_distance_matrix(dist5, graph5.get_vertices())


if __name__ == "__main__":
    test_all_pairs_shortest_paths()
