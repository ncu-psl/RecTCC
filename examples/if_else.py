def n_k(n, k):
    if (n + k)%2:
        m = n / 2
    else:
        m = k - 2
    n_k(m, m)
