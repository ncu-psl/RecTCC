def randomize_in_place(A):
    n = len(A)
    random_index = random(i, n)
    for i in n:
        temp = A[i]
        A[i] = A[random_index]
        A[random_index] = temp
