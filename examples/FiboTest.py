def fibo(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)

def fibo_dp(n):
    #fibo_array = [0, 1]

    #while len(fibo_array) < n + 1:
    #    fibo_array.append(0)
    fibo_array = [0] * n
    fibo_array[1] = 1

    if n <= 1:
        return n
    else:
        if fibo_array[n-1] == 0:
            fibo_array[n-1] = fibo_dp(n-1)
        if fibo_array[n-2] == 0:
            fibo_array[n-2] = fibo_dp(n-2)

    fibo_array[n] = fibo_array[n-1] + fibo_array[n-2]

    return fibo_array[n]


print("test")
print(fibo_dp(9))
