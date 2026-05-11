import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BarycentricInterpolator

# 定义原函数
def f(x):
    return (2 * x + 3) / (x**2 - 2 * x + 5)

# 定义误差评估点 y_i (501个点)
y = np.linspace(-5, 5, 501)
f_y = f(y)

N_values = [4, 8, 16, 32, 64]

for N in N_values:
    # 1. 均匀节点
    x_uni = np.linspace(-5, 5, N + 1)
    
    # 2. Chebyshev节点
    i = np.arange(N + 1)
    x_cheb = -5 * np.cos((2 * i + 1) / (2 * N + 2) * np.pi)
    
    poly_uni = BarycentricInterpolator(x_uni, f(x_uni))
    poly_cheb = BarycentricInterpolator(x_cheb, f(x_cheb))
    
    # 计算误差
    err_uni = np.max(np.abs(f_y - poly_uni(y)))
    err_cheb = np.max(np.abs(f_y - poly_cheb(y)))
    
    # 打印 LaTeX 格式的表格行，使用科学记数法
    print(f"{N} & {err_uni:.4e} & {err_cheb:.4e} \\\\")
