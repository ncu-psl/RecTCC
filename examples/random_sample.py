def random_sample(m, n):
    if m == 0:
        return 0
    else:
        new_m = m - 1
        new_n = n - 1
        s = random_sample(new_m)
        i = 0
        for j in n:
            i += j
        i = i%n
        if i in S:
            s.append(n)
        else:
            s.append(i)
        return s
