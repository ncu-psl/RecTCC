if_table = {'l': ['l'],
            'm': ['m - 2', 'm / 2'],
            }

else_table = {'l': ['l - 1'],
              'm': ['m - 4', 'm / 4'],
              'n': ['n']
              }

def combine_if_else(if_table, else_table):
    for key, value in else_table.items():
        if key in if_table:
            if_table[key].extend(value)
            pass
        else:
            if_table[key] = else_table[key]
    return if_table

print(combine_if_else(if_table, else_table))
