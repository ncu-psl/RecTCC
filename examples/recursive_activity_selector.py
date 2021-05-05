def recursive_activity_selector(s, f, k, n):
    m = k + 1
    while m <= n and s[m] < f[k]:
        m = m + 1
    if m <= n:
        result = recursive_activity_selector(s, f, m, n)
        return a and result
    else:
        return []