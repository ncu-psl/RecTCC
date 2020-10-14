#def mergeSort(array):
#
#    if len(array) < 2:
#        return array
#
#    #mid = len(array)//2
#    #L = array[:mid]
#    #R = array[mid:]
#
#    mergeSort(array[:len(array)//2])
#    mergeSort(array[len(array)//2:])
#
#    i, j, k = 0, 0, 0
#
#    while i < len(L) and j < len(R):
#        if L[i] < R[j]:
#            array[k] = L[i]
#            i += 1
#        else:
#            array[k] = R[j]
#            j += 1
#        k += 1
#
#    while i < len(L):
#        array[k] = L[i]
#        i += 1
#        k += 1
#
#    while j < len(R):
#        array[k] = R[j]
#        j += 1
#        k += 1

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
