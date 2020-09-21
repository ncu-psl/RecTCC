def fibo(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)

def fobi(n):
    if n > 1:
        return fobi(n-1) + fobi(n-2)
    elif n == 1:
        return 1
    else:
        return 0

def fibo_dp(n):
    fibo_array = [0, 1]

    while len(fibo_array) < n + 1:
        fibo_array.append(0)

    if n <= 1:
        return n
    else:
        if fibo_array==0:#[n-1] == 0:
            fibo_array[n-1] = fibo_dp(n-1)
        if fibo_array==0:#[n-2] == 0:
            fibo_array[n-2] = fibo_dp(n-2)

    #fibo_array[n] = fibo_array[n-1] + fibo_array[n-2]
    fibo_dp(n-3)

    return fibo_array[n]

def test(a, b):
    return test(a-1, b-1)
    
def order(n):
    if n%3 == 0 :
        print(0)
        if 1 == 1 and order(n) ==1:
            print(1)
            print(1)
            print(1)
            print(1)
            print(1)
        else:
            print(0)
            print(1)
            print(1)
    elif n%3 == 1 + fobi(1) == 0:
        print(1)
        print(1)
        print(1)
    else:
        print(2)
        print(2)
        print(2)
