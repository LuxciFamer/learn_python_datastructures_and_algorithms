#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打印机队列模拟程序

功能概述：
    该程序模拟实验室打印机的工作场景，通过队列数据结构实现任务管理，
    计算不同打印速度下的平均等待时间，帮助分析打印机性能。

核心算法原理：
    1. 使用队列（FIFO）存储打印任务
    2. 随机生成打印任务（每180秒平均生成1个任务）
    3. 模拟打印机处理任务的过程，计算任务等待时间
    4. 统计并输出平均等待时间和队列剩余任务数

时间复杂度分析：
    - 入队操作（enqueue）：O(n)，因为使用list.insert(0, item)需要移动元素
    - 出队操作（dequeue）：O(1)，使用list.pop()操作
    - 模拟过程：O(n)，其中n为模拟的总秒数

空间复杂度分析：
    - O(k)，其中k为队列中同时存在的最大任务数
    - 最坏情况下，当打印机处理速度远低于任务生成速度时，空间复杂度会接近O(n)

优化方向：
    1. 队列实现优化：使用collections.deque代替list，使入队操作变为O(1)
    2. 任务生成机制：可考虑使用更真实的概率分布模型
    3. 多打印机模拟：支持多台打印机并行处理任务
    4. 任务优先级：添加任务优先级机制
    5. 统计信息：增加更详细的统计信息，如最长等待时间、队列长度变化等
"""

import random


class Queue:
    """
    队列数据结构实现
    
    特性：先进先出（FIFO）
    实现方式：使用Python列表作为底层存储
    """
    
    def __init__(self):
        """
        初始化队列
        
        创建一个空列表来存储队列元素
        """
        self.items = []

    def isEmpty(self):
        """
        检查队列是否为空
        
        返回值：
            bool: 队列为空返回True，否则返回False
        """
        return self.items == []

    def enqueue(self, item):
        """
        入队操作
        
        参数：
            item: 要添加到队列的元素
        
        时间复杂度：O(n)，因为需要将列表中所有元素后移
        """
        self.items.insert(0, item)

    def dequeue(self):
        """
        出队操作
        
        返回值：
            队列头部的元素
        
        时间复杂度：O(1)，直接弹出列表末尾元素
        """
        return self.items.pop()

    def size(self):
        """
        获取队列大小
        
        返回值：
            int: 队列中元素的数量
        """
        return len(self.items)


class Task:
    """
    打印任务类
    
    表示一个打印任务，包含任务创建时间和打印页数
    """
    
    def __init__(self, time):
        """
        初始化打印任务
        
        参数：
            time: 任务创建的时间戳（秒）
        
        特性：
            - 随机生成1-20页的打印量
            - 记录任务创建时间
        """
        self.timestamp = time  # 任务创建时间戳
        self.pages = random.randrange(1, 21)  # 随机生成1-20页

    def getStamp(self):
        """
        获取任务创建时间戳
        
        返回值：
            int: 任务创建的时间戳
        """
        return self.timestamp

    def getPages(self):
        """
        获取打印页数
        
        返回值：
            int: 任务的打印页数
        """
        return self.pages

    def waitTime(self, currenttime):
        """
        计算任务等待时间
        
        参数：
            currenttime: 当前时间戳
        
        返回值：
            int: 任务从创建到开始处理的等待时间（秒）
        """
        return currenttime - self.timestamp


class Printer:
    """
    打印机类
    
    模拟打印机的工作状态和行为
    """
    
    def __init__(self, ppm):
        """
        初始化打印机
        
        参数：
            ppm: 打印机速度（页/分钟）
        """
        self.pagerate = ppm  # 打印速度（页/分钟）
        self.currentTask = None  # 当前正在处理的任务
        self.timeRemaining = 0  # 剩余处理时间（秒）

    def tick(self):
        """
        模拟打印机的时间 tick
        
        每调用一次，时间前进1秒，减少剩余处理时间
        如果任务处理完成，将currentTask设为None
        """
        if self.currentTask is not None:
            self.timeRemaining -= 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        """
        检查打印机是否繁忙
        
        返回值：
            bool: 打印机繁忙返回True，否则返回False
        """
        return self.currentTask is not None

    def startNext(self, newtask):
        """
        开始处理新任务
        
        参数：
            newtask: 新的打印任务
        
        计算任务所需的处理时间：
        处理时间（秒）= 页数 * 60秒/分钟 / 打印速度（页/分钟）
        """
        self.currentTask = newtask
        self.timeRemaining = newtask.getPages() * 60 / self.pagerate


def newPrintTask():
    """
    模拟新打印任务的生成
    
    概率模型：
        - 生成1-180之间的随机数
        - 只有当随机数为180时，才生成新任务
        - 平均每180秒生成1个任务
    
    返回值：
        bool: 是否生成新任务
    """
    num = random.randrange(1, 181)
    return num == 180


def simulation(numSeconds, pagesPerMinute):
    """
    模拟打印机工作过程
    
    参数：
        numSeconds: 模拟的总时间（秒）
        pagesPerMinute: 打印机速度（页/分钟）
    
    流程：
        1. 初始化打印机和打印队列
        2. 循环模拟每一秒的情况：
           a. 随机生成新任务
           b. 如果打印机空闲且队列不为空，处理下一个任务
           c. 打印机处理当前任务（tick）
        3. 计算并输出平均等待时间和队列剩余任务数
    """
    # 初始化打印机实例
    labprinter = Printer(pagesPerMinute)
    # 初始化打印队列
    printQueue = Queue()
    # 存储每个任务的等待时间
    waitingtimes = []

    # 模拟每一秒的情况
    for currentSecond in range(numSeconds):
        # 随机生成新任务
        if newPrintTask():
            task = Task(currentSecond)
            printQueue.enqueue(task)

        # 如果打印机空闲且队列不为空，处理下一个任务
        if (not labprinter.busy()) and (not printQueue.isEmpty()):
            nexttask = printQueue.dequeue()
            # 记录任务等待时间
            waitingtimes.append(nexttask.waitTime(currentSecond))
            # 开始处理新任务
            labprinter.startNext(nexttask)

        # 打印机处理当前任务（时间前进1秒）
        labprinter.tick()

    # 计算平均等待时间
    if waitingtimes:
        averageWait = sum(waitingtimes) / len(waitingtimes)
    else:
        averageWait = 0
    
    # 输出模拟结果
    print(f"平均等待时间 {averageWait:6.2f} 秒， 队列中剩余 {printQueue.size():3d} 个任务。")


if __name__ == '__main__':
    """
    主函数，执行模拟实验
    
    分别模拟两种打印速度下的情况：
    1. 5页/分钟
    2. 10页/分钟
    每种情况运行5次，观察平均等待时间
    """
    # 模拟配置：3600秒（1小时），5页/分钟
    print("【模拟配置：3600秒， 5页/分钟】")
    for _ in range(5):
        simulation(3600, 5)

    print("\n" + "="*50 + "\n")

    # 模拟配置：3600秒（1小时），10页/分钟
    print("【模拟配置：3600秒， 10页/分钟】")
    for _ in range(5):
        simulation(3600, 10)
