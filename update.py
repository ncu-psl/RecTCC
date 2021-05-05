#Input table_j-2: {'m': ['n - 2', 'n / 2']}, table_j-1: {'m': ['m - 4', 'm / 4']}
#Output {'m': ['(n - 2) - 4', '(n / 2) - 4', '(n - 2) / 4', '(n / 2) / 4']}

old = {'m': ['n - 2', 'n / 2']}
new = {'m': ['m - 4', 'm / 4']}

result = []
for key_2, value_2 in new.items():
    if key_2 in old:
        for v2 in value_2:
            f2 = '(' + v2 + ')'
            for assign_value in old[key_2]:
                print(f2.replace(key_2, assign_value))
                result.append(assign_value.replace(key_2, f2))
    else:
        j1[key_2] = value_2

print(result)


old = ['n - 2', 'n / 2']
new = ['m - 4', 'm / 4']

result = []
for n in new:
    for o in old:
        result.append(n + ' + ' + o)

print(result)
