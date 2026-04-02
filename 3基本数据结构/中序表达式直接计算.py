def infix_eval(infix_expr):
    """
    直接计算中序表达式
    使用两个栈：一个保存运算符，一个保存操作数
    """
    # 定义运算符的优先级字典
    prec = {
        "*": 3,
        "/": 3,
        "+": 2,
        "-": 2,
        "(": 1
    }
    
    # 定义有效的运算符集合
    valid_operators = set(prec.keys()) | {')'}
    
    # 创建两个栈：一个用于保存运算符，一个用于保存操作数
    op_stack = []
    operand_stack = []
    parentheses_count = 0
    
    # 处理空表达式
    if not infix_expr.strip():
        raise ValueError("输入表达式为空")
    
    # 使用字符串方法 split 将输入的中序表达式转换成一个列表
    token_list = infix_expr.split()
    
    # 检查表达式是否为空
    if not token_list:
        raise ValueError("输入表达式为空")
    
    # 检查表达式是否以运算符开始或结束
    if token_list[0] in valid_operators - {'('}:
        raise ValueError("表达式不能以运算符开始")
    if token_list[-1] in valid_operators - {')'}:
        raise ValueError("表达式不能以运算符结束")
    
    # 从左往右扫描这个标记列表
    for i, token in enumerate(token_list):
        # 检查无效字符
        if not (token.isdigit() or token in valid_operators):
            raise ValueError(f"无效字符: {token}")
        
        # 如果标记是操作数，将其转换成整数并且压入 operand_stack 栈中
        if token.isdigit():
            operand_stack.append(int(token))
        
        # 如果标记是左括号，将其压入 op_stack 栈中
        elif token == '(':
            op_stack.append(token)
            parentheses_count += 1
        
        # 如果标记是右括号，反复从 op_stack 栈中移除元素，直到移除对应的左括号
        elif token == ')':
            parentheses_count -= 1
            if parentheses_count < 0:
                raise ValueError("括号不匹配：右括号过多")
            if not op_stack:
                raise ValueError("括号不匹配：右括号没有对应的左括号")
            
            # 当遇到左括号之前，执行栈中的运算符
            top_token = op_stack.pop()
            while top_token != '(':
                # 确保操作数栈中有足够的操作数
                if len(operand_stack) < 2:
                    raise ValueError(f"运算符 {top_token} 缺少操作数")
                
                # 从 operand_stack 栈中取出两个操作数
                right_operand = operand_stack.pop()
                left_operand = operand_stack.pop()
                
                # 进行相应的算术运算
                result = do_math(top_token, left_operand, right_operand)
                
                # 将运算结果压入 operand_stack 栈中
                operand_stack.append(result)
                
                if not op_stack:
                    raise ValueError("括号不匹配：右括号没有对应的左括号")
                top_token = op_stack.pop()
        
        # 如果标记是运算符
        else:
            # 检查连续运算符
            if i > 0 and token_list[i-1] in valid_operators - {')'}:
                raise ValueError(f"连续运算符：{token_list[i-1]} {token}")
            
            # 在压入之前，需要先从栈中取出优先级更高或相同的运算符并执行
            while (len(op_stack) != 0) and (prec[op_stack[-1]] >= prec[token]):
                # 确保操作数栈中有足够的操作数
                if len(operand_stack) < 2:
                    raise ValueError(f"运算符 {op_stack[-1]} 缺少操作数")
                
                # 从 operand_stack 栈中取出两个操作数
                right_operand = operand_stack.pop()
                left_operand = operand_stack.pop()
                
                # 进行相应的算术运算
                op = op_stack.pop()
                result = do_math(op, left_operand, right_operand)
                
                # 将运算结果压入 operand_stack 栈中
                operand_stack.append(result)
            
            # 将当前运算符压入栈中
            op_stack.append(token)
    
    # 检查括号是否匹配
    if parentheses_count > 0:
        raise ValueError("括号不匹配：左括号过多")
    
    # 当处理完输入表达式以后，执行栈中所有残留的运算符
    while len(op_stack) != 0:
        # 确保操作数栈中有足够的操作数
        if len(operand_stack) < 2:
            raise ValueError(f"运算符 {op_stack[-1]} 缺少操作数")
        
        # 从 operand_stack 栈中取出两个操作数
        right_operand = operand_stack.pop()
        left_operand = operand_stack.pop()
        
        # 进行相应的算术运算
        op = op_stack.pop()
        result = do_math(op, left_operand, right_operand)
        
        # 将运算结果压入 operand_stack 栈中
        operand_stack.append(result)
    
    # 当处理完所有运算符后，栈中的值就是结果
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


def calculator():
    """
    交互式计算器
    支持中序表达式的直接计算
    """
    print("=================================")
    print("        中序表达式计算器")
    print("=================================")
    print("支持的运算符: +, -, *, /")
    print("支持括号: (, )")
    print("请在数字和运算符之间添加空格")
    print("输入 'exit' 退出计算器")
    print("=================================")
    
    while True:
        # 获取用户输入
        user_input = input("\n请输入表达式: ").strip()
        
        # 检查是否退出
        if user_input.lower() == 'exit':
            print("计算器已退出，感谢使用！")
            break
        
        # 检查是否为空输入
        if not user_input:
            print("错误: 输入表达式为空")
            continue
        
        try:
            # 计算表达式
            result = infix_eval(user_input)
            # 输出结果
            print(f"结果: {result}")
        except Exception as e:
            # 处理异常
            print(f"错误: {e}")


# --- 主程序 ---
if __name__ == "__main__":
    calculator()
