import numpy as np

def format_val(val):
    if val == 0:
        return "0.000000000000E+000"
    # 将数值转化为标准的科学计数法，保留11位小数（即12位有效数字）
    s = f"{val:.11E}" 
    sign = "-" if s.startswith("-") else ""
    if sign:
        s = s[1:]
    base_str, exp_str = s.split('E')
    base_digits = base_str.replace(".", "")
    exp_val = int(exp_str) + 1  # 调整指数，因为我们要把小数点前移一位 (例如 2.5E-1 变成 0.25E+0)
    exp_sign = "+" if exp_val >= 0 else "-"
    return f"{sign}0.{base_digits}E{exp_sign}{abs(exp_val):03d}"

print(f"{'x':<25} | {'f(x)':<25} | {'g(x)':<25}")
print("-" * 75)

for i in range(1, 12):
    # 严格使用 float32 单精度进行计算
    x = np.float32(4.0) ** np.float32(-i)
    x2 = np.float32(x * x)
    x2_plus_81 = np.float32(x2 + np.float32(81.0))
    sqrt_val = np.float32(np.sqrt(x2_plus_81))
    
    # f(x) 直接相减，会发生灾难性抵消
    f_x = np.float32(sqrt_val - np.float32(9.0))
    # g(x) 采用加法，精度稳定
    g_x = np.float32(x2 / np.float32(sqrt_val + np.float32(9.0)))
    
    print(f"$4^{{{-i}}}=$ {format_val(x)} & {format_val(f_x)} & {format_val(g_x)} \\\\ \\hline")