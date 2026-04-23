#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
水壶问题解决方案

问题描述：有两个坛子，容量分别是4加仑和3加仑，如何通过一系列操作使得4加仑的坛子中最终有2加仑的水。

使用广度优先搜索（BFS）来解决这个问题。
"""

from collections import deque
from typing import List, Tuple, Optional


def solve_water_jug_problem() -> Optional[List[Tuple[int, int]]]:
    """解决水壶问题
    
    Returns:
        Optional[List[Tuple[int, int]]]: 解决方案路径，每个元素是一个状态 (x, y)，
        其中x是4加仑坛子中的水量，y是3加仑坛子中的水量。
        如果没有解决方案，返回None。
    """
    # 定义坛子容量
    CAPACITY_4 = 4  # 4加仑坛子的容量
    CAPACITY_3 = 3  # 3加仑坛子的容量
    
    # 初始状态：两个坛子都是空的
    initial_state = (0, 0)
    
    # 目标状态：4加仑坛子中有2加仑水
    def is_goal(state: Tuple[int, int]) -> bool:
        return state[0] == 2
    
    # 记录已访问的状态，避免循环
    visited = set()
    
    # 使用队列进行BFS
    queue = deque()
    queue.append((initial_state, []))  # 每个元素是 (当前状态, 路径)
    
    while queue:
        current_state, path = queue.popleft()
        x, y = current_state
        
        # 检查是否达到目标状态
        if is_goal(current_state):
            return path + [current_state]
        
        # 标记当前状态为已访问
        if current_state in visited:
            continue
        visited.add(current_state)
        
        # 生成所有可能的下一步操作
        # 1. 装满4加仑坛子
        new_state = (CAPACITY_4, y)
        if new_state not in visited:
            queue.append((new_state, path + [current_state]))
        
        # 2. 装满3加仑坛子
        new_state = (x, CAPACITY_3)
        if new_state not in visited:
            queue.append((new_state, path + [current_state]))
        
        # 3. 倒空4加仑坛子
        new_state = (0, y)
        if new_state not in visited:
            queue.append((new_state, path + [current_state]))
        
        # 4. 倒空3加仑坛子
        new_state = (x, 0)
        if new_state not in visited:
            queue.append((new_state, path + [current_state]))
        
        # 5. 从4加仑坛子倒到3加仑坛子
        # 计算能倒多少水
        amount = min(x, CAPACITY_3 - y)
        new_state = (x - amount, y + amount)
        if new_state not in visited:
            queue.append((new_state, path + [current_state]))
        
        # 6. 从3加仑坛子倒到4加仑坛子
        # 计算能倒多少水
        amount = min(y, CAPACITY_4 - x)
        new_state = (x + amount, y - amount)
        if new_state not in visited:
            queue.append((new_state, path + [current_state]))
    
    # 没有找到解决方案
    return None

def print_solution(solution: List[Tuple[int, int]]) -> None:
    """打印解决方案
    
    Args:
        solution (List[Tuple[int, int]]): 解决方案路径
    """
    if not solution:
        print("没有找到解决方案")
        return
    
    print("水壶问题解决方案：")
    print("步骤\t4加仑坛子\t3加仑坛子")
    print("-" * 30)
    
    for i, (x, y) in enumerate(solution):
        print(f"{i+1}\t{x}加仑\t\t{y}加仑")
    
    print("-" * 30)
    print("成功！4加仑坛子中现在有2加仑水。")


def main():
    """主函数"""
    print("水壶问题：使用4加仑和3加仑的坛子，如何得到2加仑的水")
    print("=" * 50)
    
    solution = solve_water_jug_problem()
    print_solution(solution)


if __name__ == "__main__":
    main()
