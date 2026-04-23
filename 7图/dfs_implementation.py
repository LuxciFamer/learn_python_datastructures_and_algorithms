#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
深度优先搜索(DFS)算法实现

本模块实现了一个功能完善的深度优先搜索算法，支持以下特性：
1. 图数据结构的定义与初始化
2. 递归式DFS实现
3. 非递归式DFS实现
4. 多种应用场景：路径查找、连通分量识别、拓扑排序
5. 完整的错误处理机制
6. 详细的代码注释和复杂度分析
7. 测试用例
"""

from typing import Dict, List, Set, Optional, Any, Tuple


class Graph:
    """图数据结构类
    
    支持有向图和无向图的创建与管理
    """
    
    def __init__(self, directed: bool = False):
        """初始化图
        
        Args:
            directed (bool): 是否为有向图，默认为无向图
        """
        self.directed = directed
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
        
        # 添加边
        self.adjacency_list[start].append(end)
        
        # 如果是无向图，添加反向边
        if not self.directed:
            self.adjacency_list[end].append(start)
    
    def get_vertices(self) -> List[Any]:
        """获取所有顶点
        
        Returns:
            List[Any]: 顶点列表
        """
        return list(self.adjacency_list.keys())
    
    def get_edges(self) -> List[Tuple[Any, Any]]:
        """获取所有边
        
        Returns:
            List[Tuple[Any, Any]]: 边列表
        """
        edges = []
        for vertex, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                edges.append((vertex, neighbor))
        return edges
    
    def __str__(self) -> str:
        """字符串表示
        
        Returns:
            str: 图的字符串表示
        """
        result = []
        for vertex, neighbors in self.adjacency_list.items():
            result.append(f"{vertex}: {neighbors}")
        return "\n".join(result)


def recursive_dfs(graph: Graph, start: Any, visited: Optional[Set[Any]] = None, 
                 path: Optional[List[Any]] = None) -> List[Any]:
    """递归式深度优先搜索
    
    Args:
        graph (Graph): 图对象
        start (Any): 起始顶点
        visited (Optional[Set[Any]]): 已访问顶点集合
        path (Optional[List[Any]]): 路径记录
        
    Returns:
        List[Any]: DFS遍历路径
        
    时间复杂度: O(V + E)，其中V是顶点数，E是边数
    空间复杂度: O(V)，用于存储访问标记和递归栈
    """
    # 初始化
    if visited is None:
        visited = set()
    if path is None:
        path = []
    
    # 检查顶点是否存在
    if start not in graph.adjacency_list:
        raise ValueError(f"Vertex {start} not found in graph")
    
    # 标记为已访问并记录路径
    visited.add(start)
    path.append(start)
    
    # 递归访问相邻顶点
    for neighbor in graph.adjacency_list[start]:
        if neighbor not in visited:
            recursive_dfs(graph, neighbor, visited, path)
    
    return path


def iterative_dfs(graph: Graph, start: Any) -> List[Any]:
    """非递归式深度优先搜索
    
    Args:
        graph (Graph): 图对象
        start (Any): 起始顶点
        
    Returns:
        List[Any]: DFS遍历路径
        
    时间复杂度: O(V + E)，其中V是顶点数，E是边数
    空间复杂度: O(V)，用于存储访问标记和栈
    """
    # 检查顶点是否存在
    if start not in graph.adjacency_list:
        raise ValueError(f"Vertex {start} not found in graph")
    
    visited = set()
    path = []
    stack = [start]
    
    while stack:
        vertex = stack.pop()
        
        if vertex not in visited:
            visited.add(vertex)
            path.append(vertex)
            
            # 将邻居顶点逆序入栈，以保持与递归DFS相同的遍历顺序
            for neighbor in reversed(graph.adjacency_list[vertex]):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return path


def find_path(graph: Graph, start: Any, end: Any) -> Optional[List[Any]]:
    """查找从起点到终点的路径
    
    Args:
        graph (Graph): 图对象
        start (Any): 起始顶点
        end (Any): 目标顶点
        
    Returns:
        Optional[List[Any]]: 路径列表，如果不存在路径则返回None
    """
    # 检查顶点是否存在
    if start not in graph.adjacency_list or end not in graph.adjacency_list:
        raise ValueError("Start or end vertex not found in graph")
    
    visited = set()
    path = []
    
    def dfs(current: Any) -> bool:
        """内部DFS函数"""
        visited.add(current)
        path.append(current)
        
        if current == end:
            return True
        
        for neighbor in graph.adjacency_list[current]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
        
        # 回溯
        path.pop()
        return False
    
    if dfs(start):
        return path
    return None


def find_connected_components(graph: Graph) -> List[List[Any]]:
    """识别图中的所有连通分量
    
    Args:
        graph (Graph): 图对象
        
    Returns:
        List[List[Any]]: 连通分量列表
    """
    if not graph.adjacency_list:
        return []
    
    visited = set()
    components = []
    
    for vertex in graph.adjacency_list:
        if vertex not in visited:
            # 使用递归DFS找到一个连通分量
            component = []
            def dfs(current: Any):
                visited.add(current)
                component.append(current)
                for neighbor in graph.adjacency_list[current]:
                    if neighbor not in visited:
                        dfs(neighbor)
            
            dfs(vertex)
            components.append(component)
    
    return components


def topological_sort(graph: Graph) -> Optional[List[Any]]:
    """拓扑排序
    
    Args:
        graph (Graph): 有向图对象
        
    Returns:
        Optional[List[Any]]: 拓扑排序结果，如果图中存在环则返回None
    """
    if not graph.directed:
        raise ValueError("Topological sort only applicable to directed graphs")
    
    visited = set()
    temp_visited = set()  # 用于检测环
    result = []
    
    def dfs(current: Any) -> bool:
        """内部DFS函数，返回是否存在环"""
        if current in temp_visited:
            return True  # 存在环
        
        if current in visited:
            return False
        
        temp_visited.add(current)
        
        for neighbor in graph.adjacency_list[current]:
            if dfs(neighbor):
                return True
        
        temp_visited.remove(current)
        visited.add(current)
        result.insert(0, current)  # 逆后序遍历
        return False
    
    # 对所有未访问的顶点进行DFS
    for vertex in graph.adjacency_list:
        if vertex not in visited:
            if dfs(vertex):
                return None  # 存在环
    
    return result


def test_dfs():
    """测试DFS实现"""
    print("=== 测试深度优先搜索 ===")
    
    # 测试1: 无向图
    print("\n1. 测试无向图:")
    undirected_graph = Graph(directed=False)
    undirected_graph.add_edge('A', 'B')
    undirected_graph.add_edge('A', 'C')
    undirected_graph.add_edge('B', 'D')
    undirected_graph.add_edge('B', 'E')
    undirected_graph.add_edge('C', 'F')
    undirected_graph.add_edge('E', 'F')
    
    print("图结构:")
    print(undirected_graph)
    
    print("\n递归式DFS遍历:")
    result = recursive_dfs(undirected_graph, 'A')
    print(result)
    
    print("\n非递归式DFS遍历:")
    result = iterative_dfs(undirected_graph, 'A')
    print(result)
    
    # 测试2: 有向图
    print("\n2. 测试有向图:")
    directed_graph = Graph(directed=True)
    directed_graph.add_edge('A', 'B')
    directed_graph.add_edge('A', 'C')
    directed_graph.add_edge('B', 'D')
    directed_graph.add_edge('C', 'D')
    directed_graph.add_edge('D', 'E')
    
    print("图结构:")
    print(directed_graph)
    
    print("\n递归式DFS遍历:")
    result = recursive_dfs(directed_graph, 'A')
    print(result)
    
    print("\n非递归式DFS遍历:")
    result = iterative_dfs(directed_graph, 'A')
    print(result)
    
    # 测试3: 路径查找
    print("\n3. 测试路径查找:")
    path = find_path(undirected_graph, 'A', 'F')
    print(f"从A到F的路径: {path}")
    
    path = find_path(directed_graph, 'A', 'E')
    print(f"从A到E的路径: {path}")
    
    # 测试4: 连通分量
    print("\n4. 测试连通分量:")
    disconnected_graph = Graph(directed=False)
    disconnected_graph.add_edge('A', 'B')
    disconnected_graph.add_edge('B', 'C')
    disconnected_graph.add_edge('D', 'E')
    disconnected_graph.add_edge('E', 'F')
    disconnected_graph.add_vertex('G')  # 孤立顶点
    
    components = find_connected_components(disconnected_graph)
    print(f"连通分量: {components}")
    
    # 测试5: 拓扑排序
    print("\n5. 测试拓扑排序:")
    dag = Graph(directed=True)
    dag.add_edge('A', 'B')
    dag.add_edge('A', 'C')
    dag.add_edge('B', 'D')
    dag.add_edge('C', 'D')
    dag.add_edge('D', 'E')
    
    topo_order = topological_sort(dag)
    print(f"拓扑排序结果: {topo_order}")
    
    # 测试6: 带环图的拓扑排序
    print("\n6. 测试带环图的拓扑排序:")
    cyclic_graph = Graph(directed=True)
    cyclic_graph.add_edge('A', 'B')
    cyclic_graph.add_edge('B', 'C')
    cyclic_graph.add_edge('C', 'A')  # 形成环
    
    topo_order = topological_sort(cyclic_graph)
    print(f"带环图的拓扑排序结果: {topo_order}")
    
    # 测试7: 空图
    print("\n7. 测试空图:")
    empty_graph = Graph()
    components = find_connected_components(empty_graph)
    print(f"空图的连通分量: {components}")
    
    # 测试8: 错误处理
    print("\n8. 测试错误处理:")
    try:
        recursive_dfs(undirected_graph, 'X')  # 不存在的顶点
    except ValueError as e:
        print(f"错误处理测试: {e}")
    
    try:
        topological_sort(undirected_graph)  # 无向图不能拓扑排序
    except ValueError as e:
        print(f"错误处理测试: {e}")


if __name__ == "__main__":
    test_dfs()
