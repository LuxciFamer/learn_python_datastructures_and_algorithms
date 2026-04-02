def infix_to_postfix(infix_expr):
    # 定义运算符的优先级字典
    # 乘除优先级高于加减，括号优先级最低（用于栈内比较）
    prec = {
        "*": 3,
        "/": 3,
        "+": 2,
        "-": 2,
        "(": 1
    }

    # 定义有效的运算符集合
    valid_operators = set(prec.keys()) | {')'}

    # (1) 创建用于保存运算符的空栈 opstack，以及一个用于保存结果的空列表
    opstack = []
    result = []
    parentheses_count = 0

    # 处理空表达式
    if not infix_expr.strip():
        raise ValueError("输入表达式为空")

    # (2) 使用字符串方法 split 将输入的中序表达式转换成一个列表
    token_list = infix_expr.split()

    # 检查表达式是否以运算符开始或结束
    if token_list and token_list[0] in valid_operators - {'('}:
        raise ValueError("表达式不能以运算符开始")
    if token_list and token_list[-1] in valid_operators - {')'}:
        raise ValueError("表达式不能以运算符结束")

    # (3) 从左往右扫描这个标记列表
    for i, token in enumerate(token_list):
        # 检查无效字符
        if not (token.isalnum() or token in valid_operators):
            raise ValueError(f"无效字符: {token}")

        # 如果标记是操作数，将其添加到结果列表的末尾
        if token.isalnum() and token not in prec:
            result.append(token)

        # 如果标记是左括号，将其压入 opstack 栈中
        elif token == '(':
            opstack.append(token)
            parentheses_count += 1

        # 如果标记是右括号，反复从 opstack 栈中移除元素，直到移除对应的左括号
        elif token == ')':
            parentheses_count -= 1
            if parentheses_count < 0:
                raise ValueError("括号不匹配：右括号过多")
            if not opstack:
                raise ValueError("括号不匹配：右括号没有对应的左括号")
            
            top_token = opstack.pop()
            while top_token != '(':
                result.append(top_token)
                if not opstack:
                    raise ValueError("括号不匹配：右括号没有对应的左括号")
                top_token = opstack.pop()

        # 如果标记是运算符
        else:
            # 检查连续运算符
            if i > 0 and token_list[i-1] in valid_operators - {')'}:
                raise ValueError(f"连续运算符：{token_list[i-1]} {token}")
            
            # 在压入之前，需要先从栈中取出优先级更高或相同的运算符
            # while循环条件：栈不为空 且 栈顶元素优先级 >= 当前标记优先级
            while (len(opstack) != 0) and (prec[opstack[-1]] >= prec[token]):
                result.append(opstack.pop())
            # 将当前运算符压入栈中
            opstack.append(token)

    # 检查括号是否匹配
    if parentheses_count > 0:
        raise ValueError("括号不匹配：左括号过多")

    # (4) 当处理完输入表达式以后，检查 opstack。
    # 将其中所有残留的运算符全部添加到结果列表的末尾
    while len(opstack) != 0:
        result.append(opstack.pop())

    # 将列表转换为以空格分隔的字符串返回
    return " ".join(result)


# --- 测试代码 ---
if __name__ == "__main__":
    # 正常情况测试
    print("=== 正常情况测试 ===")
    # 测试用例 1: A + B * C  ->  预期输出: A B C * +
    print(infix_to_postfix("A + B * C"))

    # 测试用例 2: ( A + B ) * C  ->  预期输出: A B + C *
    print(infix_to_postfix("( A + B ) * C"))

    # 测试用例 3: A + B * C - D  ->  预期输出: A B C * + D -
    print(infix_to_postfix("A + B * C - D"))

    # 测试用例 4: ( A + B ) * ( C + D ) -> 预期输出: A B + C D + *
    print(infix_to_postfix("( A + B ) * ( C + D )"))
    
    # 异常情况测试
    print("\n=== 异常情况测试 ===")
    # 测试空表达式
    try:
        print(infix_to_postfix(""))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试括号不匹配 - 右括号过多
    try:
        print(infix_to_postfix("( A + B ) * C )"))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试括号不匹配 - 左括号过多
    try:
        print(infix_to_postfix("( ( A + B ) * C"))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试连续运算符
    try:
        print(infix_to_postfix("A + + B"))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试无效字符
    try:
        print(infix_to_postfix("A @ B"))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试以运算符开始
    try:
        print(infix_to_postfix("+ A + B"))
    except ValueError as e:
        print(f"预期异常: {e}")
    
    # 测试以运算符结束
    try:
        print(infix_to_postfix("A + B +"))
    except ValueError as e:
        print(f"预期异常: {e}")
