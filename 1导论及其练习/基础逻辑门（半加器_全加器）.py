#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
逻辑门与加法器实现

功能概述：
    实现基本逻辑门（与门、异或门）、半加器、全加器和多位二进制加法器
    提供面向对象和函数式两种实现方式

优化内容：
    1. 统一逻辑门接口，增加更多逻辑门类型
    2. 优化半加器和全加器的实现
    3. 增强二进制加法器的功能和错误处理
    4. 提高代码可读性和可维护性
    5. 添加更多测试用例
"""


class LogicGate:
    """逻辑门基类"""

    def __init__(self, name):
        self.name = name
        self.output = None

    def get_name(self):
        return self.name

    def get_output(self):
        return self.output


class BinaryGate(LogicGate):
    """二输入逻辑门基类"""

    def __init__(self, name, input_a=None, input_b=None):
        super().__init__(name)
        self.input_a = input_a
        self.input_b = input_b

    def set_inputs(self, a, b):
        """设置输入值"""
        self.input_a = a
        self.input_b = b


class AndGate(BinaryGate):
    """与门"""

    def __init__(self, name, input_a=None, input_b=None):
        super().__init__(name, input_a, input_b)

    def get_output(self):
        """计算与门输出
        
        与逻辑：仅当两个输入都为1时输出1
        """
        if self.input_a is not None and self.input_b is not None:
            self.output = 1 if (self.input_a == 1 and self.input_b == 1) else 0
        return self.output


class XorGate(BinaryGate):
    """异或门"""

    def __init__(self, name, input_a=None, input_b=None):
        super().__init__(name, input_a, input_b)

    def get_output(self):
        """计算异或门输出
        
        异或逻辑：当两个输入不同时输出1
        """
        if self.input_a is not None and self.input_b is not None:
            self.output = 1 if (self.input_a != self.input_b) else 0
        return self.output


class OrGate(BinaryGate):
    """或门"""

    def __init__(self, name, input_a=None, input_b=None):
        super().__init__(name, input_a, input_b)

    def get_output(self):
        """计算或门输出
        
        或逻辑：当至少一个输入为1时输出1
        """
        if self.input_a is not None and self.input_b is not None:
            self.output = 1 if (self.input_a == 1 or self.input_b == 1) else 0
        return self.output


class HalfAdder:
    """半加器类"""

    def __init__(self, name, input_a=None, input_b=None):
        self.name = name
        self.input_a = input_a
        self.input_b = input_b
        self.sum_output = None
        self.carry_output = None
        # 预创建逻辑门实例，避免重复创建
        self.xor_gate = XorGate(f"{self.name}_xor")
        self.and_gate = AndGate(f"{self.name}_and")

    def set_inputs(self, a, b):
        """设置输入值"""
        self.input_a = a
        self.input_b = b

    def compute(self):
        """执行半加器计算
        
        返回：
            (进位, 和位)
        """
        if self.input_a is not None and self.input_b is not None:
            # 使用预创建的逻辑门计算和位
            self.xor_gate.set_inputs(self.input_a, self.input_b)
            self.sum_output = self.xor_gate.get_output()

            # 使用预创建的逻辑门计算进位位
            self.and_gate.set_inputs(self.input_a, self.input_b)
            self.carry_output = self.and_gate.get_output()

        return self.carry_output, self.sum_output

    def get_outputs(self):
        """获取计算结果"""
        return self.carry_output, self.sum_output


class FullAdder:
    """全加器类"""

    def __init__(self, name):
        self.name = name
        # 预创建半加器实例
        self.half_adder1 = HalfAdder(f"{self.name}_ha1")
        self.half_adder2 = HalfAdder(f"{self.name}_ha2")
        self.or_gate = OrGate(f"{self.name}_or")

    def compute(self, bit_a, bit_b, carry_in):
        """执行全加器计算
        
        参数：
            bit_a, bit_b: 当前位的两个加数
            carry_in: 来自低位的进位
        
        返回：
            (进位输出, 和位)
        """
        # 第一个半加器：计算bit_a和bit_b的部分和
        self.half_adder1.set_inputs(bit_a, bit_b)
        carry1, sum1 = self.half_adder1.compute()

        # 第二个半加器：将部分和与进位输入相加
        self.half_adder2.set_inputs(sum1, carry_in)
        carry2, final_sum = self.half_adder2.compute()

        # 最终进位：carry1或carry2
        self.or_gate.set_inputs(carry1, carry2)
        final_carry = self.or_gate.get_output()

        return final_carry, final_sum


def half_adder(a, b):
    """
    半加器函数
    
    参数：
        a, b: 两个输入位（0或1）
    
    返回：
        (和位, 进位)
    """
    sum_bit = a ^ b  # 异或运算得到和位
    carry = a & b    # 与运算得到进位
    return sum_bit, carry


def full_adder(bit_a, bit_b, carry_in):
    """
    全加器实现（基于半加器）
    
    参数：
        bit_a, bit_b: 当前位的两个加数
        carry_in: 来自低位的进位
    
    返回：
        (进位输出, 和位)
    """
    # 第一个半加器：计算bit_a和bit_b的部分和
    sum1, carry1 = half_adder(bit_a, bit_b)

    # 第二个半加器：将部分和与进位输入相加
    final_sum, carry2 = half_adder(sum1, carry_in)

    # 最终进位：carry1或carry2
    final_carry = carry1 or carry2

    return final_carry, final_sum


def binary_adder(bin_a, bin_b, n_bits=8):
    """
    多位二进制加法器
    
    参数：
        bin_a, bin_b: 二进制字符串（如"1101"）
        n_bits: 位数
    
    返回：
        相加结果的二进制字符串
    
    异常：
        ValueError: 如果输入不是有效的二进制字符串
    """
    # 验证输入是否为有效的二进制字符串
    for bit in bin_a + bin_b:
        if bit not in ('0', '1'):
            raise ValueError("输入必须是有效的二进制字符串")

    # 确保输入位数一致
    a = bin_a.zfill(n_bits)
    b = bin_b.zfill(n_bits)

    carry = 0
    result_bits = []

    # 从最低位（最右侧）开始逐位相加
    for i in range(n_bits - 1, -1, -1):
        bit_a = int(a[i])
        bit_b = int(b[i])

        carry, sum_bit = full_adder(bit_a, bit_b, carry)
        result_bits.append(str(sum_bit))

    # 如果最后有进位，添加到结果最高位
    if carry:
        result_bits.append('1')

    # 反转结果（因为我们是从低位开始计算的）
    result = ''.join(result_bits[::-1])

    return result


def test_half_adder():
    """测试半加器"""
    print("面向对象半加器测试：")
    ha = HalfAdder("ha1")
    ha.set_inputs(1, 1)
    carry, sum_bit = ha.compute()
    print(f"输入：A=1, B=1 -> 和位={sum_bit}, 进位={carry}")

    # 批量测试
    print("\n完整真值表验证：")
    expected_results = [
        ((0, 0), (0, 0)),  # A=0, B=0 -> C=0, S=0
        ((0, 1), (0, 1)),  # A=0, B=1 -> C=0, S=1
        ((1, 0), (0, 1)),  # A=1, B=0 -> C=0, S=1
        ((1, 1), (1, 0)),  # A=1, B=1 -> C=1, S=0
    ]
    
    for (a, b), (expected_carry, expected_sum) in expected_results:
        ha.set_inputs(a, b)
        c, s = ha.compute()
        status = "OK" if (c == expected_carry and s == expected_sum) else "FAIL"
        print(f"{status} A={a}, B={b} -> S={s}, C={c} (期望: S={expected_sum}, C={expected_carry})")


def test_full_adder():
    """测试全加器"""
    print("\n全加器测试：")
    test_cases = [
        (0, 0, 0, 0, 0),  # A=0, B=0, Cin=0 -> Cout=0, S=0
        (0, 0, 1, 0, 1),  # A=0, B=0, Cin=1 -> Cout=0, S=1
        (0, 1, 0, 0, 1),  # A=0, B=1, Cin=0 -> Cout=0, S=1
        (0, 1, 1, 1, 0),  # A=0, B=1, Cin=1 -> Cout=1, S=0
        (1, 0, 0, 0, 1),  # A=1, B=0, Cin=0 -> Cout=0, S=1
        (1, 0, 1, 1, 0),  # A=1, B=0, Cin=1 -> Cout=1, S=0
        (1, 1, 0, 1, 0),  # A=1, B=1, Cin=0 -> Cout=1, S=0
        (1, 1, 1, 1, 1),  # A=1, B=1, Cin=1 -> Cout=1, S=1
    ]
    
    for a, b, cin, expected_cout, expected_sum in test_cases:
        cout, sum_bit = full_adder(a, b, cin)
        status = "OK" if (cout == expected_cout and sum_bit == expected_sum) else "FAIL"
        print(f"{status} A={a}, B={b}, Cin={cin} -> S={sum_bit}, Cout={cout} (期望: S={expected_sum}, Cout={expected_cout})")


def test_binary_adder():
    """测试多位二进制加法器"""
    print("\n8位二进制加法器测试：")
    test_cases = [
        ("11011010", "01100101", 8),  # 218 + 101 = 319
        ("00000000", "00000000", 8),  # 0 + 0 = 0
        ("11111111", "00000001", 8),  # 255 + 1 = 256
        ("10000000", "10000000", 8),  # 128 + 128 = 256
    ]
    
    for num1, num2, n_bits in test_cases:
        try:
            result = binary_adder(num1, num2, n_bits)
            decimal_result = int(result, 2)
            expected_result = int(num1, 2) + int(num2, 2)
            status = "OK" if decimal_result == expected_result else "FAIL"
            print(f"{status} {num1} + {num2} = {result} (十进制: {int(num1, 2)} + {int(num2, 2)} = {decimal_result})")
        except Exception as e:
            print(f"FAIL 测试失败: {e}")


if __name__ == "__main__":
    """主函数，执行所有测试"""
    test_half_adder()
    test_full_adder()
    test_binary_adder()
    
    # 测试面向对象全加器
    print("\n面向对象全加器测试：")
    fa = FullAdder("fa1")
    carry_out, sum_out = fa.compute(1, 1, 1)
    print(f"结果：和位={sum_out}, 进位={carry_out}")  # 输出：和位=1, 进位=1（即1+1+1=11，二进制3）
