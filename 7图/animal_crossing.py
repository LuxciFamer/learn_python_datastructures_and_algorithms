#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
动物过河问题解决方案

问题描述：3只羚羊和3只狮子准备乘船过河，河边有一艘能容纳2只动物的小船。
如果两侧河岸上的狮子数量大于羚羊数量，羚羊就会被吃掉。找到运送办法，使得所有动物都能安全渡河。

使用广度优先搜索（BFS）来解决这个问题。
"""

from collections import deque
from typing import List, Tuple, Optional


def is_valid_state(antelopes: int, lions: int) -> bool:
    """检查状态是否合法
    
    Args:
        antelopes (int): 某岸的羚羊数量
        lions (int): 某岸的狮子数量
        
    Returns:
        bool: 状态是否合法
    """
    # 数量不能为负数或超过3
    if antelopes < 0 or lions < 0 or antelopes > 3 or lions > 3:
        return False
    
    # 如果有羚羊，狮子数量不能多于羚羊数量
    if antelopes > 0 and lions > antelopes:
        return False
    
    return True

def solve_animal_crossing() -> Optional[List[Tuple[int, int, int]]]:
    """解决动物过河问题
    
    Returns:
        Optional[List[Tuple[int, int, int]]]: 解决方案路径，每个元素是一个状态 (left_antelopes, left_lions, boat_position)
        其中boat_position为0表示船在左岸，1表示船在右岸。
        如果没有解决方案，返回None。
    """
    # 初始状态：3只羚羊，3只狮子，船在左岸
    initial_state = (3, 3, 0)
    
    # 目标状态：0只羚羊，0只狮子在左岸，船在右岸
    goal_state = (0, 0, 1)
    
    # 记录已访问的状态，避免循环
    visited = set()
    
    # 使用队列进行BFS
    queue = deque()
    queue.append((initial_state, []))  # 每个元素是 (当前状态, 路径)
    
    # 可能的移动：(羚羊数量变化, 狮子数量变化)
    # 船每次可以载1或2只动物
    moves = [(1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]
    
    while queue:
        current_state, path = queue.popleft()
        left_antelopes, left_lions, boat_pos = current_state
        
        # 检查是否达到目标状态
        if current_state == goal_state:
            return path + [current_state]
        
        # 标记当前状态为已访问
        if current_state in visited:
            continue
        visited.add(current_state)
        
        # 生成所有可能的下一步操作
        for move in moves:
            antelopes_move, lions_move = move
            
            if boat_pos == 0:  # 船在左岸，从左岸到右岸
                new_left_antelopes = left_antelopes - antelopes_move
                new_left_lions = left_lions - lions_move
                new_boat_pos = 1
            else:  # 船在右岸，从右岸到左岸
                new_left_antelopes = left_antelopes + antelopes_move
                new_left_lions = left_lions + lions_move
                new_boat_pos = 0
            
            # 检查新状态是否合法
            if is_valid_state(new_left_antelopes, new_left_lions):
                # 检查对岸的状态是否合法
                right_antelopes = 3 - new_left_antelopes
                right_lions = 3 - new_left_lions
                if is_valid_state(right_antelopes, right_lions):
                    new_state = (new_left_antelopes, new_left_lions, new_boat_pos)
                    if new_state not in visited:
                        queue.append((new_state, path + [current_state]))
    
    # 没有找到解决方案
    return None

def print_solution(solution: List[Tuple[int, int, int]]) -> None:
    """打印解决方案
    
    Args:
        solution (List[Tuple[int, int, int]]): 解决方案路径
    """
    if not solution:
        print("没有找到解决方案")
        return
    
    print("动物过河问题解决方案：")
    print("步骤\t左岸羚羊\t左岸狮子\t右岸羚羊\t右岸狮子\t船位置")
    print("-" * 70)
    
    for i, (left_antelopes, left_lions, boat_pos) in enumerate(solution):
        right_antelopes = 3 - left_antelopes
        right_lions = 3 - left_lions
        boat_location = "左岸" if boat_pos == 0 else "右岸"
        print(f"{i+1}\t{left_antelopes}\t\t{left_lions}\t\t{right_antelopes}\t\t{right_lions}\t\t{boat_location}")
    
    print("-" * 70)
    print("成功！所有动物都安全过河。")

def main():
    """主函数"""
    print("动物过河问题：3只羚羊和3只狮子如何安全过河")
    print("船容量：2只动物")
    print("规则：任何时候河岸两边的狮子数量不能多于羚羊数量")
    print("=" * 70)
    
    solution = solve_animal_crossing()
    print_solution(solution)


if __name__ == "__main__":
    main()
