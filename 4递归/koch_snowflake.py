import turtle

def koch_curve(t, length, depth):
    """
    递归绘制科赫曲线
    
    Args:
        t: 海龟对象
        length: 线段长度
        depth: 递归深度
    """
    if depth == 0:
        # 递归终止条件：直接绘制线段
        t.forward(length)
    else:
        # 递归绘制科赫曲线
        length /= 3
        koch_curve(t, length, depth - 1)
        t.left(60)
        koch_curve(t, length, depth - 1)
        t.right(120)
        koch_curve(t, length, depth - 1)
        t.left(60)
        koch_curve(t, length, depth - 1)

def draw_koch_snowflake(size, depth):
    """
    绘制科赫雪花
    
    Args:
        size: 雪花的大小
        depth: 递归深度
    """
    # 创建海龟对象
    t = turtle.Turtle()
    t.speed(1)  # 设置绘制速度，使过程清晰可见
    t.pensize(2)  # 设置画笔粗细
    t.pencolor("blue")  # 设置画笔颜色
    
    # 设置画布
    screen = turtle.Screen()
    screen.setup(800, 800)
    screen.bgcolor("white")
    screen.title(f"科赫雪花 (深度: {depth})")
    
    # 移动到起始位置
    t.penup()
    t.goto(-size / 2, -size / 3)
    t.pendown()
    t.left(60)  # 调整初始角度
    
    # 绘制三个科赫曲线，构成雪花
    for _ in range(3):
        koch_curve(t, size, depth)
        t.right(120)
    
    # 隐藏海龟
    t.hideturtle()
    
    # 保持窗口打开
    screen.mainloop()

def main():
    """
    主函数，绘制科赫雪花
    """
    # 设置雪花大小和递归深度
    size = 500
    depth = 3
    
    print(f"正在绘制科赫雪花，深度: {depth}")
    draw_koch_snowflake(size, depth)

if __name__ == "__main__":
    main()
