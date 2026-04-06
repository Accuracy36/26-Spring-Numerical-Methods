import math

def f(x):
    return math.atan(x) + 2 * math.sin(x) - 0.1958

def df(x):
    # f'(x) 的解析式
    return 1 / (1 + x**2) + 2 * math.cos(x)

def ddf(x):
    # f''(x) 的解析式
    return -2 * x / ((1 + x**2)**2) - 2 * math.sin(x)

def newton_method(x0, tol=1e-8, max_iter=20000):
    x = x0
    for i in range(1, max_iter + 1):
        fx = f(x)
        if abs(fx) < tol:
            return i, x
        dfx = df(x)
        if dfx == 0:
            return max_iter + 1, None # 导数为0，失败
        x = x - fx / dfx
    return max_iter + 1, None # 超过最大迭代次数

def halley_method(x0, tol=1e-8, max_iter=20000):
    x = x0
    for i in range(1, max_iter + 1):
        fx = f(x)
        if abs(fx) < tol:
            return i, x
        dfx = df(x)
        ddfx = ddf(x)
        denominator = 2 * dfx**2 - fx * ddfx
        if denominator == 0:
            return max_iter + 1, None # 分母为0，失败
        x = x - (2 * fx * dfx) / denominator
    return max_iter + 1, None

# 实验要求的初始点
x0_list = [-200, -90, -25, -19, -13, -5, 0.1958, 5, 13, 25, 50, 80, 150]

print("请将以下输出粘贴到 LaTeX 表格中：\n")
for x0 in x0_list:
    n_iter_n, root_n = newton_method(x0)
    n_iter_h, root_h = halley_method(x0)

    str_n_iter = str(n_iter_n) if n_iter_n <= 20000 else "失败"
    str_root_n = f"{root_n:.6f}" if root_n is not None and n_iter_n <= 20000 else "-"

    str_h_iter = str(n_iter_h) if n_iter_h <= 20000 else "失败"
    str_root_h = f"{root_h:.6f}" if root_h is not None and n_iter_h <= 20000 else "-"

    print(f"{x0} & {str_n_iter} & {str_root_n} & {str_h_iter} & {str_root_h} \\\\")
