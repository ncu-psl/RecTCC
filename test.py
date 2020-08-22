l = [[('fibo', ['(n - 1)']), [[[[('fibo', ['(n / 2)']), ('fibo', ['(n / 4)']), ('fibo', ['(n / 4)']), ('fibo', ['(n / 8)'])]]]], ('fibo', ['(n - 2)'])], [[[[[('fibo_dp', ['(n - 1)'])]], [[('fibo_dp', ['(n - 2)'])]]]]]]


l = [[[('fibo_dp', ['(n - 0)']), [[('fibo_dp', ['(n - 1)'])]], [[('fibo_dp', ['(n - 2)'])]]]]]



#l = ['a', 'e', [['f'], ['b', 'c']], 'd']
#l = ['a', 'e', [['f']], 'd']
l = ['a', 'e', [['b'], ['c']], 'd', [[[['f']], [['g']]]]]



#def spread(l):
#
#    rosen = [[]]
#    for element in l:
#        if isinstance(element, str):
#            rosen = add_road(rosen, element)
#        if isinstance(element, list):
#            for elem in element:
#                rosen = add_road(rosen, elem)
#
#    return rosen


def travel(l):

    rosen = [[]]
    while l:
        next_node = l.pop(0)
        if isinstance(next_node, str):
            rosen = add_road(rosen, next_node)
        if isinstance(next_node, list):
            rosen = add_road(rosen, next_node)
    return rosen
            

def spread(l):
    for element in l:
        if 

def add_road(old, new):

    old_road = old
    new_road = new

    final = []
    for new_road in new:
        for old_r in old_road:
            old_r_copy = old_r.copy()
            old_r_copy.extend(new_road)
            final.append(old_r_copy)

    return final

#def add_road(old, new):
#
#    old_road = old
#    new_road = new
#
#    final = []
#    for new_road in new:
#        for old_r in old_road:
#            old_r_copy = old_r.copy()
#            old_r_copy.append(new_road)
#            final.append(old_r_copy)
#
#    return final
      

print(add_road([['a', 'd'], ['a', 'e']], [['b', 'd'], ['c']]))
print(add_road([[]], [['b', 'd'], ['c']]))

#print(travel(l))
