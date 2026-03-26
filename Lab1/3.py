import math

# 题目给定的高精度 pi
PI = 3.1415926535897932

def pade_kernel(u):
    u2 = u**2
    u4 = u2**2
    u6 = u4 * u2
    
    num = 1 - (29593/207636)*u2 + (34911/7613320)*u4 - (479249/11511339840)*u6
    den = 1 + (1671/69212)*u2 + (97/351384)*u4 + (2623/1644477120)*u6
    return u * (num / den)

def special_sin(x):
    abs_x = abs(x)
    
    # 极小值直接返回
    if abs_x < 1e-8:
        return x
        
    # 大于 pi/6，使用三倍角公式进行区间规约
    elif abs_x > PI / 6:
        u = x / 3
        sin_u = pade_kernel(u)
        return (3 - 4 * sin_u**2) * sin_u
        
    # 小于等于 pi/6，直接使用逼近公式
    else:
        return pade_kernel(x)

def taylor_sin(x):
    """4项泰勒展开近似"""
    return x - (x**3)/math.factorial(3) + (x**5)/math.factorial(5) - (x**7)/math.factorial(7)

# 测试数据点
x_values = [
    ("pi/2024", PI/2024),
    ("pi/1012", PI/1012),
    ("pi/50", PI/50),
    ("pi/8", PI/8),
    ("pi/6", PI/6),
    ("pi/4", PI/4),
    ("pi/3", PI/3)
]

# 打印结果并对比
print(f"{'x':<10} | {'Special Routine':<15} | {'Taylor (4 terms)':<15} | {'math.sin(x)':<15}")
print("-" * 65)
for label, x in x_values:
    val_special = special_sin(x)
    val_taylor = taylor_sin(x)
    val_math = math.sin(x) # 调用标准库作为参照
    
    # 保留10位小数输出
    print(f"{label:<10} | {val_special:.10f}      | {val_taylor:.10f}      | {val_math:.10f}")