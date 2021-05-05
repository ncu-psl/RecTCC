def binarySearch(array, low, high, x):

    if high >= low:
        mid = (high + low)//2

        if array[mid] == x:
            return mid
        elif array[mid] > x:
            return binarySearch(array, low, mid, x)
        else:
            return binarySearch(array, mid, high, x)
    else:
        return -1
