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
