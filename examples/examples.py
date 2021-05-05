'''
def mergeSort(array):

    if len(array) < 2:
        return array

    mid = len(array)//2
    L = array[:mid]
    R = array[mid:]

    mergeSort(L)
    mergeSort(R)

    i, j, k = 0, 0, 0

    while i < len(L) and j < len(R):
        if L[i] < R[j]:
            array[k] = L[i]
            i += 1
        else:
            array[k] = R[j]
            j += 1
        k += 1

    while i < len(L):
        array[k] = L[i]
        i += 1
        k += 1

    while j < len(R):
        array[k] = R[j]
        j += 1
        k += 1

    return array

print(mergeSort([1, 2, 3, 5, 4, 3, 9, 7, 6, 4, 67, 7]))
'''

def fibo(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)


def binarySearch(array, low, high, x):

    if high >= low:
        #mid = (high + low)//2

        if array[(high + low)//2] == x:
            return mid
        elif array[(high + low)//2] > x:
            return binarySearch(array, low, (high + low)//2-1, x)
        else:
            return binarySearch(array, (high + low)//2+1, high, x)
    else:
        return -1

def mul_step(n):
    if n%2:
        m = n + 10
    else:
        m = n - 5
    for i in m:
        print(1)


def two_if():
    if 1:
        print(1)
    else:
        print(0)
        print(0)
        two_if()

    if 2:
        print(2)
        print(2)
        print(2)
    else:
        print(0)
        print(0)
        print(0)
        print(0)
        print(0)

def m_n(n):
    m = n
    if 1:
        m = m - 2
    else:
        m = m / 2

    if 1:
        m = m - 4
    else:
        m = m / 4
