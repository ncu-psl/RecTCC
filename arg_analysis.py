import collections
import sympy

def arg_analysis(funcName, funcParameter, funcCall):
    print("funcName: %s%s, funcCall: %s" %(funcName, funcParameter, funcCall))
    changed_index = []

    for road in funcCall:
        if not road:
            continue

        for call in road:
            if len(call) != len(funcParameter):
                continue

            for index, args in enumerate(zip(funcParameter, call)):
                if args[0] != args[1]:
                    changed_index.append(index)

    changed_index = list(set(changed_index))

    if len(changed_index) == 1:
        #only 1 arg
        workload_list = []
        for road in funcCall:
            if not road:
                workload_list.append([])
            else:
                workload_in_one_road = []
                for call in road:
                    workload_in_one_road.append(workload_arg1(funcParameter, call, changed_index))
                workload_list.append(workload_in_one_road)
        print(workload_list)

    elif len(changed_index) == 2:
        #2 args
        workload_list = []
        for road in funcCall:
            if not road:
                workload_list.append([])
            else:
                workload_in_one_road = []
                for call in road:
                    workload_in_one_road.append(workload_arg2(funcParameter, call, changed_index))
                workload_list.append(workload_in_one_road)
        print(workload_list)

    else:
        print('Complex')

    return changed_index

def workload_arg1(funcParameter, funcCall, changed_index):
    head = changed_index[0]
    workload_origin = funcParameter[head]
    workload_new = funcCall[head]
    
    workload_diff = '(' + workload_origin + ') - (' + workload_new + ')'
    workload_diff = str(sympy.simplify(workload_diff))

    if '/' in workload_diff:
        return '/'
    else:
        return '+'



def workload_arg2(funcParameter, funcCall, changed_index):
    head = changed_index[0]
    tail = changed_index[1]
    workload_origin = funcParameter[tail] + ' - ' + funcParameter[head]
    workload_new = funcCall[tail] + ' - ' + funcCall[head]

    workload_diff = '(' + workload_origin + ') - (' + workload_new + ')'
    workload_diff = str(sympy.simplify(workload_diff))

    if '/' in workload_diff:
        return '/'
    else:
        return '+'


