from collections import deque
import re

class HTMLTagChecker:
    """
    HTML标签匹配检查器
    使用栈来检查HTML文档中的标签是否正确匹配
    """
    
    def __init__(self):
        """初始化检查器"""
        self.stack = deque()
    
    def extract_tags(self, html):
        """
        从HTML文本中提取所有标签
        html: HTML文本
        return: 标签列表
        """
        # 使用正则表达式提取标签
        # 匹配开始标签、结束标签和自闭合标签
        tag_pattern = r'<(/?[^>]+)>'
        tags = re.findall(tag_pattern, html)
        return tags
    
    def get_tag_name(self, tag):
        """
        从标签中提取标签名（忽略属性）
        tag: 标签字符串
        return: 标签名
        """
        # 去除结束标签的斜杠
        if tag.startswith('/'):
            tag = tag[1:]
        
        # 提取标签名（忽略属性）
        tag_name = tag.split()[0].lower()
        
        # 处理自闭合标签
        if tag_name.endswith('/'):
            tag_name = tag_name[:-1]
        
        return tag_name
    
    def is_self_closing(self, tag):
        """
        检查标签是否是自闭合标签
        tag: 标签字符串
        return: 是否是自闭合标签
        """
        # 检查是否以 '/' 结尾
        if tag.endswith('/'):
            return True
        
        # 检查是否是常见的自闭合标签
        tag_name = tag.split()[0].lower()
        return tag_name in ['br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source']
    
    def check_tags(self, html):
        """
        检查HTML标签是否正确匹配
        html: HTML文本
        return: (是否匹配, 错误信息)
        """
        # 提取标签
        tags = self.extract_tags(html)
        
        # 清空栈
        self.stack.clear()
        
        for i, tag in enumerate(tags):
            # 检查是否是结束标签
            if tag.startswith('/'):
                # 提取标签名
                tag_name = self.get_tag_name(tag)
                
                # 检查栈是否为空
                if not self.stack:
                    return False, f"第 {i+1} 个标签 </{tag_name}> 没有对应的开始标签"
                
                # 检查是否匹配
                top_tag = self.stack.pop()
                if top_tag != tag_name:
                    return False, f"第 {i+1} 个标签 </{tag_name}> 与开始标签 <{top_tag}> 不匹配"
            else:
                # 检查是否是自闭合标签
                if not self.is_self_closing(tag):
                    # 提取标签名并压入栈
                    tag_name = self.get_tag_name(tag)
                    self.stack.append(tag_name)
        
        # 检查栈是否为空
        if self.stack:
            return False, f"有未闭合的标签: {', '.join([f'<{tag}>' for tag in self.stack])}"
        
        return True, "所有标签都正确匹配"
    
    def check_file(self, file_path):
        """
        检查文件中的HTML标签是否正确匹配
        file_path: 文件路径
        return: (是否匹配, 错误信息)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
            return self.check_tags(html)
        except Exception as e:
            return False, f"读取文件时出错: {str(e)}"

# --- 测试代码 ---
if __name__ == "__main__":
    # 测试用例1: 正确的HTML
    html1 = """
    <html>
        <head>
            <title>Example</title>
        </head>
        <body>
            <h1>Hello, world</h1>
            <p>This is a <b>bold</b> text.</p>
            <img src="example.jpg" alt="Example" />
        </body>
    </html>
    """
    
    # 测试用例2: 缺少结束标签
    html2 = """
    <html>
        <head>
            <title>Example</title>
        </head>
        <body>
            <h1>Hello, world
            <p>This is a <b>bold</b> text.</p>
        </body>
    </html>
    """
    
    # 测试用例3: 标签不匹配
    html3 = """
    <html>
        <head>
            <title>Example</title>
        </head>
        <body>
            <h1>Hello, world</h2>
            <p>This is a <b>bold text.</p>
        </body>
    </html>
    """
    
    # 测试用例4: 自闭合标签
    html4 = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Example</title>
        </head>
        <body>
            <h1>Hello, world</h1>
            <br>
            <p>This is a line break above.</p>
            <hr>
            <p>This is a horizontal rule above.</p>
        </body>
    </html>
    """
    
    # 测试用例5: 嵌套错误
    html5 = """
    <html>
        <head>
            <title>Example</title>
        </head>
        <body>
            <div>
                <p>This is a paragraph.
            </div>
            </p>
        </body>
    </html>
    """
    
    checker = HTMLTagChecker()
    
    test_cases = [
        (html1, "正确的HTML"),
        (html2, "缺少结束标签"),
        (html3, "标签不匹配"),
        (html4, "自闭合标签"),
        (html5, "嵌套错误")
    ]
    
    print("=== HTML标签匹配检查 ===")
    for i, (html, description) in enumerate(test_cases):
        print(f"\n测试用例 {i+1}: {description}")
        is_valid, message = checker.check_tags(html)
        if is_valid:
            print(f"OK 标签匹配正确: {message}")
        else:
            print(f"ERROR 标签匹配错误: {message}")
    
    # 测试用户提供的HTML示例
    print("\n=== 测试用户提供的HTML示例 ===")
    user_html = """
    <html>
        <head>
            <title>
                Example
            </title>
        </head>
        <body>
            <body>
                <h1>Hello, world</h1>
            </body>
        </body>
    </html>
    """
    is_valid, message = checker.check_tags(user_html)
    if is_valid:
        print(f"OK 标签匹配正确: {message}")
    else:
        print(f"ERROR 标签匹配错误: {message}")
