def mergeSort(array):

    if len(array) < 2:
        return array

    mid = len(array)//2
    L = array[:mid]
    R = array[mid:]

    mergeSort(L)
    mergeSort(R)

    i = 0
    j = 0
    k = 0

    while i < len(L) and j < len(R):
        if L[i] < R[j]:
            array[k] = L[i]
            i += 1
        else:
            array[k] = R[j]
            j += 1
        k += 1

    #while i < len(L):
    #    array[k] = L[i]
    #    i += 1
    #    k += 1

    while j < len(R):
        array[k] = R[j]
        j += 1
        k += 1
'''
def mergesort(a, b, e):

    if b < e:
        m = (b + e) // 2
        # print("ms1",a,b,m)
        mergesort(a, b, m)
        # print("ms2",a,m+1,e)
        mergesort(a, m + 1, e)
        # print("m",a,b,m,e)
        merge(a, b, m, e)
        return a

def fibo(n):
    a = 1
    b, c = 2, 3
    if n == 0:
        return 1
    elif n == 1:
        if (1 == 1):
            print('pass')
            return 1
        else:
            print('false')
            return 0
    else:
        return fibo(n-1) + fibo(n-2)

#def main():
#    while 1 != 1:
#        print('false')
#    else:
#        print('pass')
#    
#    print(fibo(3))
#
#
#
#
#if __name__ == "__main__":
#    main()
#    #import doctest
#
#    #doctest.testmod()
#
'''