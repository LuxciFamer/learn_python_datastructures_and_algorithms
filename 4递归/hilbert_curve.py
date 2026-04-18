import turtle

def hilbert_curve(t, order, size, direction):
    """
    递归绘制希尔伯特曲线
    
    Args:
        t: 海龟对象
        order: 曲线阶数
        size: 每段线段的长度
        direction: 绘制方向 (0: 右, 1: 上, 2: 左, 3: 下)
    """
    if order == 0:
        return
    
    # 调整方向
    t.right(direction * 90)
    
    # 递归绘制四个子曲线
    hilbert_curve(t, order - 1, size, (direction + 3) % 4)
    t.forward(size)
    hilbert_curve(t, order - 1, size, direction)
    t.forward(size)
    hilbert_curve(t, order - 1, size, direction)
    t.right(90)
    t.forward(size)
    t.right(270)
    hilbert_curve(t, order - 1, size, (direction + 1) % 4)
    
    # 恢复方向
    t.left(direction * 90)

def draw_hilbert_curve(order=3, size=20):
    """
    绘制希尔伯特曲线
    
    Args:
        order: 曲线阶数
        size: 每段线段的长度
    """
    # 创建海龟对象
    t = turtle.Turtle()
    t.speed(0)  # 最快速度
    
    # 计算画布大小
    canvas_size = size * (2 ** order)
    
    # 设置画布
    screen = turtle.Screen()
    screen.setup(canvas_size + 100, canvas_size + 100)
    screen.title(f"希尔伯特曲线 (阶数: {order})")
    
    # 移动到起始位置
    start_x = -canvas_size / 2
    start_y = -canvas_size / 2
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    
    # 开始绘制
    hilbert_curve(t, order, size, 0)
    
    # 隐藏海龟
    t.hideturtle()
    
    # 保持窗口打开
    screen.mainloop()

def main(order=3):
    """
    主函数，绘制希尔伯特曲线
    
    Args:
        order: 曲线阶数
    """
    if order < 1:
        print("阶数必须大于等于1")
        return
    
    # 计算合适的线段长度
    # 确保画布不会太大
    max_size = 600
    size = max_size // (2 ** order)
    if size < 5:
        size = 5
        print(f"线段长度已自动调整为 {size}")
    
    # 绘制希尔伯特曲线
    draw_hilbert_curve(order, size)

if __name__ == "__main__":
    # 直接绘制阶数为3的希尔伯特曲线
    print("正在绘制阶数为3的希尔伯特曲线...")
    main(3)
    
    # 也可以取消下面的注释，获取用户输入
    # try:
    #     order = int(input("请输入希尔伯特曲线的阶数 (推荐 1-6): "))
    #     main(order)
    # except ValueError:
    #     print("请输入有效的整数")

