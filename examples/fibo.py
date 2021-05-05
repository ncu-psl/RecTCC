def fibo(n):
    if n <= 1:
        return 1
    else:
        m1 = n - 1
        m2 = n - 2
        return fibo(m1) + fibo(m2)
'''

def sample(n):
    m = n
    if m%2:
        m = m - 2
    else:
        m = m / 2
        if m > 10:
            m = m / 4
        else:
            m = m - 4
            l = 1
        sample(m)
    m = m / 3
    print(m)
'''