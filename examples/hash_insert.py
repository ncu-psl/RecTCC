def hash_insert(T,k):
    i = 0
    while i != m:
        for j in h(k, i):
            if T[j] == Null:
                T[j] = k
                return j
            else:
                i += 1
    raise OverflowError
