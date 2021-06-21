def fibo(n):
    if n <= 1:
        return 1
    else:
        m1 = n - 1
        m2 = n - 2
        return fibo(m1) + fibo(m2)
