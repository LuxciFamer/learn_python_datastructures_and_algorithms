import turtle
import random

def get_branch_color(branch_len):
    """
    根据树枝长度获取颜色
    
    Args:
        branch_len: 树枝长度
    
    Returns:
        str: 树枝颜色
    """
    if branch_len < 15:
        # 小树枝用绿色
        return "green"
    elif branch_len < 30:
        # 中等树枝用棕绿色
        return "#8B4513"
    else:
        # 大树枝用棕色
        return "#654321"

def draw_branch(t, branch_len, x, y):
    """
    绘制树枝
    
    Args:
        t: 海龟对象
        branch_len: 树枝长度
        x, y: 起始位置
    """
    if branch_len < 5:
        return
    
    # 计算树枝粗细 (线性递减)
    thickness = branch_len / 10
    
    # 获取树枝颜色
    color = get_branch_color(branch_len)
    
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.pensize(thickness)
    t.pencolor(color)
    
    # 绘制当前树枝
    t.forward(branch_len)
    new_x, new_y = t.position()
    
    # 随机生成转向角度 (15-45度)
    angle = random.randint(15, 45)
    
    # 随机生成长度递减值 (5-15)
    length_decrement = random.randint(5, 15)
    
    # 递归绘制左右分支
    t.left(angle)
    draw_branch(t, branch_len - length_decrement, new_x, new_y)
    t.right(angle * 2)
    draw_branch(t, branch_len - length_decrement, new_x, new_y)
    t.left(angle)
    
    # 回到起始位置
    t.penup()
    t.goto(x, y)
    t.pendown()

def draw_tree(branch_len, x=0, y=-200):
    """
    绘制递归树
    
    Args:
        branch_len: 初始树枝长度
        x, y: 树的起始位置
    """
    # 设置画布和海龟
    window = turtle.Screen()
    window.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)  # 最快速度
    t.left(90)  # 向上
    
    # 绘制树干
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.pensize(branch_len / 10)
    t.pencolor("#654321")
    t.forward(branch_len)
    
    # 递归绘制树枝
    new_x, new_y = t.position()
    draw_branch(t, branch_len - random.randint(5, 15), new_x, new_y)
    
    window.mainloop()

# 测试绘制树
if __name__ == "__main__":
    draw_tree(100)
