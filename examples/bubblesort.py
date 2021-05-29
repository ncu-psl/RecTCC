def bubblesort(A):
    for i in range(len(A)):
        for j in range(i):
            if A[j] < A[j-1]:
                exchange(A[j], A[j-1])