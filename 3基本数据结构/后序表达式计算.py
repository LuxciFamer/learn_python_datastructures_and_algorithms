def postfix_eval(postfix_expr):
    # 定义有效的运算符集合
    valid_operators = {'+', '-', '*', '/'}
    
    # (1) 创建空栈 operandStack
    operand_stack = []

    # 处理空表达式
    if not postfix_expr.strip():
        raise ValueError("输入表达式为空")

    # (2) 使用字符串方法 split 将输入的后序表达式转换成一个列表
    token_list = postfix_expr.split()

    # 检查表达式是否为空
    if not token_list:
        raise ValueError("输入表达式为空")

    # (3) 从左往右扫描这个标记列表
    for token in token_list:
        # 如果标记是操作数，将其转换成整数并且压入 operandStack 栈中
        # 这里假设标记是数字字符串。isdigit() 方法用于判断字符串是否只包含数字
        if token.isdigit():
            operand_stack.append(int(token))

        # 如果标记是运算符
        elif token in valid_operators:
            # 检查操作数是否足够
            if len(operand_stack) < 2:
                raise ValueError(f"运算符 {token} 缺少操作数")
            
            # 从 operandStack 栈中取出两个操作数
            # 第一次取出右操作数
            right_operand = operand_stack.pop()
            # 第二次取出左操作数
            left_operand = operand_stack.pop()

            # 进行相应的算术运算
            result = do_math(token, left_operand, right_operand)

            # 将运算结果压入 operandStack 栈中
            operand_stack.append(result)
        else:
            # 无效字符
            raise ValueError(f"无效字符: {token}")

    # (4) 当处理完输入表达式时，栈中的值就是结果。将其从栈中返回。
    if len(operand_stack) == 0:
        raise ValueError("表达式无效：没有结果")
    elif len(operand_stack) > 1:
        raise ValueError("表达式无效：操作数过多")
    
    return operand_stack.pop()


def do_math(op, left, right):
    """辅助函数：执行算术运算"""
    if op == "*":
        return left * right
    elif op == "/":
        if right == 0:
            raise ZeroDivisionError("除零错误")
        return left / right  # 注意：Python中 / 是浮点除法，// 是整除
    elif op == "+":
        return left + right
    elif op == "-":
        return left - right
    else:
        raise ValueError(f"未知运算符: {op}")


# --- 测试代码 ---
if __name__ == "__main__":
    # 正常情况测试
    print("=== 正常情况测试 ===")
    # 测试用例 1: "4 5 +" -> 4 + 5 = 9
    print(f"结果: {postfix_eval('4 5 +')}")

    # 测试用例 2: "7 8 * 4 +" -> 7 * 8 + 4 = 60
    # 后序计算逻辑:
    # 1. 遇 7，入栈 [7]
    # 2. 遇 8，入栈 [7, 8]
    # 3. 遇 *，取 8(右)，取 7(左)，7*8=56，入栈 [56]
    # 4. 遇 4，入栈 [56, 4]
    # 5. 遇 +，取 4(右)，取 56(左)，56+4=60，入栈 [60]
    print(f"结果: {postfix_eval('7 8 * 4 +')}")

    # 测试用例 3: "9 3 /" -> 9 / 3 = 3
    print(f"结果: {postfix_eval('9 3 /')}")

    # 测试用例 4: 复杂表达式 (1 + 2) * (3 + 4) 对应的后序 "1 2 + 3 4 + *"
    # 结果应为 21
    print(f"结果: {postfix_eval('1 2 + 3 4 + *')}")
    
    # 异常情况测试
    print("\n=== 异常情况测试 ===")
    # 测试空表达式
    try:
        print(postfix_eval(""))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试运算符缺少操作数
    try:
        print(postfix_eval("4 +"))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试操作数过多
    try:
        print(postfix_eval("4 5 6 +"))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试无效字符
    try:
        print(postfix_eval("4 5 a +"))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试除零错误
    try:
        print(postfix_eval("4 0 /"))
    except ZeroDivisionError as e:
        print(f"预期异常: {e}")
    
    # 测试未知运算符
    try:
        print(postfix_eval("4 5 ^"))
    except ValueError as e:
        print(f"预期异常: {e}")
