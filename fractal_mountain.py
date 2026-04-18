import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

def midpoint(p1, p2):
    """
    计算两点的中点
    
    Args:
        p1: 第一个点 (x, y, z)
        p2: 第二个点 (x, y, z)
    
    Returns:
        tuple: 中点坐标 (x, y, z)
    """
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, (p1[2] + p2[2]) / 2)

def fractal_mountain(triangle, max_depth, current_depth=0, roughness=0.5, height_scale=100):
    """
    递归细分三角形生成分形山
    
    Args:
        triangle: 初始三角形顶点 [(x1, y1, z1), (x2, y2, z2), (x3, y3, z3)]
        max_depth: 最大细分深度
        current_depth: 当前深度
        roughness: 粗糙度参数 (0-1)
        height_scale: 高度缩放因子
    
    Returns:
        list: 细分后的三角形列表
    """
    if current_depth >= max_depth:
        return [triangle]
    
    # 计算三角形各边的中点
    mid1 = midpoint(triangle[0], triangle[1])
    mid2 = midpoint(triangle[1], triangle[2])
    mid3 = midpoint(triangle[2], triangle[0])
    
    # 计算中心点
    center = midpoint(mid1, mid2)
    
    # 计算高度扰动，随深度增加而减小
    amplitude = height_scale * (roughness ** current_depth)
    center = (center[0], center[1], center[2] + random.uniform(-amplitude, amplitude))
    
    # 为中点添加随机高度扰动
    mid1 = (mid1[0], mid1[1], mid1[2] + random.uniform(-amplitude/2, amplitude/2))
    mid2 = (mid2[0], mid2[1], mid2[2] + random.uniform(-amplitude/2, amplitude/2))
    mid3 = (mid3[0], mid3[1], mid3[2] + random.uniform(-amplitude/2, amplitude/2))
    
    # 分割为4个子三角形
    sub_triangles = [
        [triangle[0], mid1, mid3],
        [triangle[1], mid2, mid1],
        [triangle[2], mid3, mid2],
        [mid1, mid2, mid3]
    ]
    
    # 递归细分每个子三角形
    result = []
    for sub_tri in sub_triangles:
        result.extend(fractal_mountain(sub_tri, max_depth, current_depth + 1, roughness, height_scale))
    
    return result

def plot_fractal_mountain(triangles):
    """
    绘制分形山
    
    Args:
        triangles: 三角形列表
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for triangle in triangles:
        # 提取三角形的三个顶点
        x = [p[0] for p in triangle]
        y = [p[1] for p in triangle]
        z = [p[2] for p in triangle]
        
        # 绘制三角形
        ax.plot_trisurf(x, y, z, cmap='terrain', edgecolor='none', alpha=0.8)
    
    # 设置坐标轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # 设置标题
    ax.set_title('Fractal Mountain')
    
    # 调整视角
    ax.view_init(elev=30, azim=45)
    
    plt.show()

def generate_fractal_mountain(size=100, depth=5, roughness=0.5, height_scale=50):
    """
    生成并绘制分形山
    
    Args:
        size: 初始三角形大小
        depth: 细分深度
        roughness: 粗糙度参数
        height_scale: 高度缩放因子
    """
    # 定义初始三角形顶点
    # 为了创建一个更大的初始三角形，使用等边三角形
    half_size = size / 2
    triangle = [
        (-half_size, -half_size, 0),
        (half_size, -half_size, 0),
        (0, half_size, 0)
    ]
    
    # 生成分形山
    triangles = fractal_mountain(triangle, depth, 0, roughness, height_scale)
    
    # 绘制分形山
    plot_fractal_mountain(triangles)

# 测试生成分形山
if __name__ == "__main__":
    # 生成默认参数的分形山
    generate_fractal_mountain()
    
    # 可以通过调整参数生成不同形态的山
    # generate_fractal_mountain(size=150, depth=6, roughness=0.6, height_scale=70)
