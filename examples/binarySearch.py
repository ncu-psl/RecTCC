def binarySearch(array, x):

    low = 0
    high = len(array)-1

    while (low <= high):
        mid = (high + low)//2
        if array[mid] == x:
            return mid
        elif array[mid] > x:
            high = mid-1
        else:
            low = mid+1
    return -1
