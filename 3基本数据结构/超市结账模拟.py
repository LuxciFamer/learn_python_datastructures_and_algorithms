import random
import heapq
import numpy as np
import matplotlib.pyplot as plt
import time
from collections import deque

class Customer:
    """顾客类"""
    def __init__(self, arrival_time, items_count, payment_method):
        self.arrival_time = arrival_time  # 到达时间
        self.items_count = items_count  # 商品数量
        self.payment_method = payment_method  # 支付方式
        self.start_service_time = None  # 开始服务时间
        self.end_service_time = None  # 结束服务时间
        self.waiting_time = None  # 等待时间
        self.service_time = None  # 服务时间

class Cashier:
    """收银员类"""
    def __init__(self, cashier_id, efficiency=1.0):
        self.cashier_id = cashier_id  # 收银员ID
        self.efficiency = efficiency  # 工作效率（0.8-1.2）
        self.is_busy = False  # 是否忙碌
        self.current_customer = None  # 当前服务的顾客
        self.available_time = 0  # 可用时间
        self.total_working_time = 0  # 总工作时间
        self.customers_served = 0  # 服务顾客数

class Event:
    """事件类"""
    def __init__(self, event_time, event_type, customer=None, cashier=None):
        self.event_time = event_time  # 事件时间
        self.event_type = event_type  # 事件类型：'arrival', 'start_service', 'end_service'
        self.customer = customer  # 相关顾客
        self.cashier = cashier  # 相关收银员
    
    def __lt__(self, other):
        """用于优先队列排序"""
        return self.event_time < other.event_time

class SupermarketCheckoutSimulator:
    """超市结账模拟系统"""
    def __init__(self, num_cashiers=5, simulation_time=43200, arrival_rate=0.1, 
                 items_mean=15, items_std=5, scan_time=2, payment_times=None):
        """
        初始化模拟系统
        num_cashiers: 收银员数量
        simulation_time: 模拟时间（秒）
        arrival_rate: 顾客到达率（每秒）
        items_mean: 商品数量均值
        items_std: 商品数量标准差
        scan_time: 单位商品扫描时间（秒）
        payment_times: 不同支付方式的时间（秒）
        """
        self.num_cashiers = num_cashiers
        self.simulation_time = simulation_time
        self.arrival_rate = arrival_rate
        self.items_mean = items_mean
        self.items_std = items_std
        self.scan_time = scan_time
        
        # 支付方式时间（秒）
        if payment_times is None:
            self.payment_times = {
                'cash': 30,
                'card': 20,
                'mobile': 15
            }
        else:
            self.payment_times = payment_times
        
        # 支付方式概率分布
        self.payment_probs = {
            'cash': 0.3,
            'card': 0.4,
            'mobile': 0.3
        }
        
        # 初始化收银员
        self.cashiers = [Cashier(i, efficiency=random.uniform(0.9, 1.1)) for i in range(num_cashiers)]
        
        # 初始化队列
        self.queue = deque()
        
        # 事件优先队列
        self.event_queue = []
        
        # 统计数据
        self.customers = []  # 所有顾客
        self.waiting_times = []  # 等待时间
        self.service_times = []  # 服务时间
        self.queue_lengths = []  # 队列长度记录
        self.queue_times = []  # 队列长度记录时间
        
        # 初始化顾客到达事件
        self._schedule_next_arrival()
    
    def _schedule_next_arrival(self):
        """安排所有顾客到达事件"""
        current_time = 0
        while True:
            # 指数分布生成到达间隔时间
            inter_arrival_time = np.random.exponential(1/self.arrival_rate)
            next_arrival_time = current_time + inter_arrival_time
            
            if next_arrival_time > self.simulation_time:
                break
            
            # 生成顾客
            items_count = max(1, int(np.random.normal(self.items_mean, self.items_std)))
            payment_method = random.choices(
                list(self.payment_probs.keys()),
                weights=list(self.payment_probs.values())
            )[0]
            
            customer = Customer(next_arrival_time, items_count, payment_method)
            self.customers.append(customer)
            
            # 创建到达事件
            event = Event(next_arrival_time, 'arrival', customer=customer)
            heapq.heappush(self.event_queue, event)
            
            current_time = next_arrival_time
    
    def _get_service_time(self, customer, cashier):
        """计算服务时间"""
        # 扫描时间 = 商品数量 * 单位扫描时间 / 收银员效率
        scan_time = customer.items_count * self.scan_time / cashier.efficiency
        # 支付时间
        payment_time = self.payment_times[customer.payment_method]
        return scan_time + payment_time
    
    def _find_available_cashier(self):
        """找到可用的收银员"""
        for cashier in self.cashiers:
            if not cashier.is_busy:
                return cashier
        return None
    
    def _assign_customer_to_cashier(self, customer, current_time):
        """将顾客分配给收银员"""
        cashier = self._find_available_cashier()
        if cashier:
            # 开始服务
            cashier.is_busy = True
            cashier.current_customer = customer
            customer.start_service_time = current_time
            
            # 计算服务时间
            service_time = self._get_service_time(customer, cashier)
            customer.service_time = service_time
            
            # 安排服务结束事件
            end_service_time = current_time + service_time
            event = Event(end_service_time, 'end_service', customer=customer, cashier=cashier)
            heapq.heappush(self.event_queue, event)
        else:
            # 加入队列
            self.queue.append(customer)
    
    def _process_arrival(self, event):
        """处理顾客到达事件"""
        customer = event.customer
        current_time = event.event_time
        
        # 记录队列长度
        self.queue_lengths.append(len(self.queue))
        self.queue_times.append(current_time)
        
        # 尝试分配收银员
        self._assign_customer_to_cashier(customer, current_time)
    
    def _process_end_service(self, event):
        """处理服务结束事件"""
        customer = event.customer
        cashier = event.cashier
        current_time = event.event_time
        
        # 完成服务
        cashier.is_busy = False
        cashier.current_customer = None
        cashier.available_time = current_time
        cashier.total_working_time += customer.service_time
        cashier.customers_served += 1
        
        # 计算顾客等待时间
        customer.end_service_time = current_time
        customer.waiting_time = customer.start_service_time - customer.arrival_time
        self.waiting_times.append(customer.waiting_time)
        self.service_times.append(customer.service_time)
        
        # 记录队列长度
        self.queue_lengths.append(len(self.queue))
        self.queue_times.append(current_time)
        
        # 如果队列不为空，服务下一个顾客
        if self.queue:
            next_customer = self.queue.popleft()
            self._assign_customer_to_cashier(next_customer, current_time)
    
    def run_simulation(self):
        """运行模拟"""
        print(f"开始模拟超市结账场景...")
        print(f"模拟时间: {self.simulation_time/3600:.1f}小时")
        print(f"收银员数量: {self.num_cashiers}")
        print(f"顾客到达率: {self.arrival_rate}人/秒")
        print("=" * 60)
        
        start_time = time.time()
        
        # 处理事件队列
        while self.event_queue:
            # 取出时间最早的事件
            event = heapq.heappop(self.event_queue)
            
            # 如果事件时间超过模拟时间，结束模拟
            if event.event_time > self.simulation_time:
                break
            
            # 处理事件
            if event.event_type == 'arrival':
                self._process_arrival(event)
            elif event.event_type == 'end_service':
                self._process_end_service(event)
        
        # 计算统计数据
        self._calculate_statistics()
        
        elapsed_time = time.time() - start_time
        print(f"模拟完成，耗时: {elapsed_time:.2f}秒")
    
    def _calculate_statistics(self):
        """计算统计数据"""
        # 顾客统计
        self.total_customers = len(self.customers)
        self.served_customers = len(self.waiting_times)
        self.average_waiting_time = np.mean(self.waiting_times) if self.waiting_times else 0
        self.max_waiting_time = max(self.waiting_times) if self.waiting_times else 0
        self.average_service_time = np.mean(self.service_times) if self.service_times else 0
        
        # 队列统计
        self.average_queue_length = np.mean(self.queue_lengths) if self.queue_lengths else 0
        self.max_queue_length = max(self.queue_lengths) if self.queue_lengths else 0
        
        # 收银员统计
        self.cashier_utilization = []
        for cashier in self.cashiers:
            utilization = cashier.total_working_time / self.simulation_time
            self.cashier_utilization.append(utilization)
        self.average_utilization = np.mean(self.cashier_utilization)
    
    def print_statistics(self):
        """打印统计结果"""
        print("\n===== 模拟统计结果 =====")
        print(f"总顾客数: {self.total_customers}")
        print(f"已服务顾客数: {self.served_customers}")
        print(f"平均等待时间: {self.average_waiting_time:.2f}秒 ({self.average_waiting_time/60:.2f}分钟)")
        print(f"最大等待时间: {self.max_waiting_time:.2f}秒 ({self.max_waiting_time/60:.2f}分钟)")
        print(f"平均服务时间: {self.average_service_time:.2f}秒 ({self.average_service_time/60:.2f}分钟)")
        print(f"平均队列长度: {self.average_queue_length:.2f}")
        print(f"最大队列长度: {self.max_queue_length}")
        print(f"平均收银员利用率: {self.average_utilization:.2f}")
        
        print("\n===== 收银员工作情况 =====")
        for i, cashier in enumerate(self.cashiers):
            utilization = self.cashier_utilization[i]
            print(f"收银员 {i+1}: 服务顾客数={cashier.customers_served}, 利用率={utilization:.2f}")
    
    def visualize_results(self):
        """可视化结果"""
        fig, axs = plt.subplots(2, 2, figsize=(15, 10))
        
        # 等待时间分布
        axs[0, 0].hist(self.waiting_times, bins=30, edgecolor='black')
        axs[0, 0].set_title('等待时间分布')
        axs[0, 0].set_xlabel('等待时间 (秒)')
        axs[0, 0].set_ylabel('顾客数')
        axs[0, 0].grid(True, alpha=0.3)
        
        # 队列长度变化
        axs[0, 1].plot(np.array(self.queue_times)/3600, self.queue_lengths)
        axs[0, 1].set_title('队列长度变化')
        axs[0, 1].set_xlabel('时间 (小时)')
        axs[0, 1].set_ylabel('队列长度')
        axs[0, 1].grid(True, alpha=0.3)
        
        # 收银员利用率
        axs[1, 0].bar([f'收银员{i+1}' for i in range(self.num_cashiers)], self.cashier_utilization)
        axs[1, 0].set_title('收银员利用率')
        axs[1, 0].set_xlabel('收银员')
        axs[1, 0].set_ylabel('利用率')
        axs[1, 0].set_ylim(0, 1)
        axs[1, 0].grid(True, alpha=0.3, axis='y')
        
        # 等待时间与服务时间关系
        if len(self.waiting_times) > 0:
            axs[1, 1].scatter(self.service_times, self.waiting_times, alpha=0.5)
            axs[1, 1].set_title('等待时间与服务时间关系')
            axs[1, 1].set_xlabel('服务时间 (秒)')
            axs[1, 1].set_ylabel('等待时间 (秒)')
            axs[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('超市结账模拟结果.png')
        print("\n可视化结果已保存为 '超市结账模拟结果.png'")
    
    def generate_recommendation(self):
        """生成优化建议"""
        print("\n===== 优化建议 =====")
        
        # 基于等待时间的建议
        if self.average_waiting_time > 300:  # 5分钟
            print("1. 等待时间较长，建议增加收银员数量")
        elif self.average_waiting_time > 180:  # 3分钟
            print("1. 等待时间适中，可考虑在高峰期增加临时收银员")
        else:
            print("1. 等待时间合理，服务质量良好")
        
        # 基于队列长度的建议
        if self.max_queue_length > 10:
            print("2. 队列长度较长，建议优化结账流程或增加结账通道")
        elif self.max_queue_length > 5:
            print("2. 队列长度适中，可考虑优化顾客引导")
        else:
            print("2. 队列长度合理，无需调整")
        
        # 基于收银员利用率的建议
        if self.average_utilization > 0.8:
            print("3. 收银员利用率较高，建议增加收银员数量")
        elif self.average_utilization < 0.5:
            print("3. 收银员利用率较低，可考虑减少收银员数量以节约成本")
        else:
            print("3. 收银员利用率合理，人员配置适当")
        
        # 其他建议
        print("4. 建议根据历史数据调整高峰期的收银员配置")
        print("5. 考虑设置快速结账通道（如10件商品以下）")
        print("6. 推广移动支付以减少支付时间")

# 模拟场景对比
def compare_scenarios():
    """对比不同场景"""
    print("\n===== 场景对比 =====")
    
    # 场景1：标准配置
    print("\n场景1：标准配置")
    print("- 收银员数量: 5")
    print("- 顾客到达率: 0.1人/秒")
    simulator1 = SupermarketCheckoutSimulator(num_cashiers=5, arrival_rate=0.1)
    simulator1.run_simulation()
    simulator1.print_statistics()
    
    # 场景2：高峰期配置
    print("\n场景2：高峰期配置")
    print("- 收银员数量: 8")
    print("- 顾客到达率: 0.15人/秒")
    simulator2 = SupermarketCheckoutSimulator(num_cashiers=8, arrival_rate=0.15)
    simulator2.run_simulation()
    simulator2.print_statistics()
    
    # 场景3：低峰期配置
    print("\n场景3：低峰期配置")
    print("- 收银员数量: 3")
    print("- 顾客到达率: 0.05人/秒")
    simulator3 = SupermarketCheckoutSimulator(num_cashiers=3, arrival_rate=0.05)
    simulator3.run_simulation()
    simulator3.print_statistics()
    
    # 可视化对比
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    
    # 场景1队列长度
    axs[0].plot(np.array(simulator1.queue_times)/3600, simulator1.queue_lengths)
    axs[0].set_title('场景1：标准配置')
    axs[0].set_xlabel('时间 (小时)')
    axs[0].set_ylabel('队列长度')
    axs[0].grid(True, alpha=0.3)
    
    # 场景2队列长度
    axs[1].plot(np.array(simulator2.queue_times)/3600, simulator2.queue_lengths)
    axs[1].set_title('场景2：高峰期配置')
    axs[1].set_xlabel('时间 (小时)')
    axs[1].set_ylabel('队列长度')
    axs[1].grid(True, alpha=0.3)
    
    # 场景3队列长度
    axs[2].plot(np.array(simulator3.queue_times)/3600, simulator3.queue_lengths)
    axs[2].set_title('场景3：低峰期配置')
    axs[2].set_xlabel('时间 (小时)')
    axs[2].set_ylabel('队列长度')
    axs[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('不同场景队列长度对比.png')
    print("\n场景对比可视化已保存为 '不同场景队列长度对比.png'")

if __name__ == "__main__":
    # 运行单个模拟
    simulator = SupermarketCheckoutSimulator(
        num_cashiers=5,
        simulation_time=43200,  # 12小时
        arrival_rate=0.1,
        items_mean=15,
        items_std=5,
        scan_time=2
    )
    simulator.run_simulation()
    simulator.print_statistics()
    simulator.visualize_results()
    simulator.generate_recommendation()
    
    # 运行场景对比
    compare_scenarios()
