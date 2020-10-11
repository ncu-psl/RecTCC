def normal_no():
    print('normal')
    return

def normal_normal():
    normal_no()
    return

def normal_recursive():
    recursive_no(n)
    return 

def recursive_no(n):
    return recursive_no(n-1)

def recursive_normal(n):
    normal_no()
    return recursive_normal(n-1)

def recursive_recursive(n):
    recursive_no(n-1)
    return (recursive_recursive(n-1))

print('a')
