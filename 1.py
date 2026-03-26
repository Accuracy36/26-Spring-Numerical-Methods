import numpy as np
import scipy.linalg
import time

def solve_system(n):
    # 构建 Hilbert 矩阵 H
    i = np.arange(1, n + 1)
    j = np.arange(1, n + 1)
    I, J = np.meshgrid(i, j, indexing='ij')
    H = 1.0 / (I + J - 1)
    
    # 构建 A = H + 1.8I
    A = H + 1.8 * np.eye(n)
    
    # 精确解 x* 和 右端向量 b
    x_star = np.ones(n)
    b = A @ x_star
    
    epsilon = 1e-5
    max_iter = 500000
    
    # === Jacobi 迭代 ===
    x_jacobi = np.zeros(n)
    D = np.diag(A)
    R = A - np.diag(D)
    
    iter_jacobi = 0
    err_jacobi = float('inf')
    jacobi_failed = False
    
    while iter_jacobi < max_iter:
        x_new = (b - R @ x_jacobi) / D
        err_jacobi = np.sum(np.abs(x_new - x_star))  # 1-范数误差
        
        if err_jacobi < epsilon:
            x_jacobi = x_new
            iter_jacobi += 1
            break
        
        # 发散保护：如果误差爆炸，提前判定失败
        if err_jacobi > 1e10 or np.isnan(err_jacobi):
            jacobi_failed = True
            break
            
        x_jacobi = x_new
        iter_jacobi += 1
        
    if iter_jacobi == max_iter:
        jacobi_failed = True
        
    norm_jacobi = np.sum(np.abs(x_jacobi)) if not jacobi_failed else np.nan
    
    # === Gauss-Seidel 迭代 ===
    x_gs = np.zeros(n)
    U = np.triu(A, 1)
    D_plus_L = np.tril(A) # 包含对角线和下三角
    
    iter_gs = 0
    err_gs = float('inf')
    gs_failed = False
    
    while iter_gs < max_iter:
        # GS公式可以写为解下三角方程: (D+L)x_new = b - U*x_old
        c = b - U @ x_gs
        # 使用 scipy 的 solve_triangular 极大提升大规模矩阵的迭代速度
        x_new = scipy.linalg.solve_triangular(D_plus_L, c, lower=True)
        err_gs = np.sum(np.abs(x_new - x_star))
        
        if err_gs < epsilon:
            x_gs = x_new
            iter_gs += 1
            break
            
        if err_gs > 1e10 or np.isnan(err_gs):
            gs_failed = True
            break
            
        x_gs = x_new
        iter_gs += 1

    if iter_gs == max_iter:
        gs_failed = True
        
    norm_gs = np.sum(np.abs(x_gs)) if not gs_failed else np.nan

    return {
        'n': n,
        'jacobi': ('失败' if jacobi_failed else iter_jacobi, 
                   '> 1e10' if jacobi_failed else f"{err_jacobi:.2e}", 
                   '-' if jacobi_failed else f"{norm_jacobi:.6f}"),
        'gs': ('失败' if gs_failed else iter_gs, 
               '> 1e10' if gs_failed else f"{err_gs:.2e}", 
               '-' if gs_failed else f"{norm_gs:.6f}")
    }

if __name__ == "__main__":
    ns = [10, 20, 60, 100, 200, 500, 2000]
    print(f"{'n':<6} | {'Method':<12} | {'Iterations':<10} | {'Error (1-norm)':<15} | {'Norm ||x||_1':<15}")
    print("-" * 65)
    for n in ns:
        t0 = time.time()
        res = solve_system(n)
        print(f"{n:<6} | {'Jacobi':<12} | {str(res['jacobi'][0]):<10} | {res['jacobi'][1]:<15} | {res['jacobi'][2]:<15}")
        print(f"{'':<6} | {'Gauss-Seidel':<12} | {str(res['gs'][0]):<10} | {res['gs'][1]:<15} | {res['gs'][2]:<15}")
        print("-" * 65)