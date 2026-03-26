import numpy as np
import math

# 保证原始数据全部按 64位双精度（float64） 读入内存
nums_str = [
    "4044.045051380452", "0.000531415926535", "-2759471.276702747",
    "0.0000557052996742895", "2755463.874010974", "-36.64291531256604", "-0.000031415926535"
]
nums = np.array([float(x) for x in nums_str], dtype=np.float64)

# 定义一个求和跑分函数
def do_sum(arr):
    s = np.float64(0.0)
    for x in arr:
        s += x
    return s

# (a) 顺序求和
sum_a = do_sum(nums)

# (b) 逆序求和
sum_b = do_sum(nums[::-1])

# (c) 按绝对值从小到大求和
nums_c = sorted(nums, key=lambda x: abs(x))
sum_c = do_sum(nums_c)

# (d) 按绝对值从大到小求和
nums_d = sorted(nums, key=lambda x: abs(x), reverse=True)
sum_d = do_sum(nums_d)

# 精确值 (利用 math.fsum 避免所有的中间舍入误差)
exact_sum = math.fsum(nums)

# 格式化输出：科学计数法，保留9位小数
def format_sci(val):
    if val == 0.0:
        return "0.000000000E+00"
    return f"{val:.9E}"

print(f"(a) 顺序求和:       {format_sci(sum_a)}")
print(f"(b) 逆序求和:       {format_sci(sum_b)}")
print(f"(c) 绝对值从小到大: {format_sci(sum_c)}")
print(f"(d) 绝对值从大到小: {format_sci(sum_d)}")
print(f"精确值(math.fsum):  {format_sci(exact_sum)}")