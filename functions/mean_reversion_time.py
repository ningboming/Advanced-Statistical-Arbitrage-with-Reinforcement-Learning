import numpy as np

def get_mean_reverse_time(x: np.ndarray, C):
    # compute the index of important extremum and num
    index_min = find_minimum(x, C)
    index_max = find_maximum(x, C)
    num_extre = len(index_min) + len(index_max)
    # compute the reversion time
    theta = np.mean(x)
    total_reverse_time = 0
    # compute the total reversion time of minimums
    for start_index in index_min:
        reverse_index = start_index
        while reverse_index < len(x)-1:
            if x[reverse_index] < theta and x[reverse_index+1] > theta:
                break
            else:
                reverse_index += 1
        total_reverse_time += reverse_index - start_index
    # compute the total reversion time of maximums
    for start_index in index_max:
        reverse_index = start_index
        while reverse_index < len(x)-1:
            if x[reverse_index] > theta and x[reverse_index+1] < theta:
                break
            else:
                reverse_index += 1
        total_reverse_time += reverse_index - start_index
    # compute mean reverse time
    if num_extre > 0:
        mean_reverse_time = total_reverse_time / num_extre 
    else:
        mean_reverse_time = 0
    return mean_reverse_time

def get_optimal_ratio(s1: np.ndarray, s2: np.ndarray, C):
    b_list = np.arange(200) / 100
    reverse_time_list = np.zeros(200)
    for i in range(200):
        x = s1 - b_list[i] * s2
        reverse_time_temp = get_mean_reverse_time(x, C) 
        reverse_time_list[i] = reverse_time_temp
    b_best = b_list[np.argmin(reverse_time_list)]
    return b_best

def construct_spread(s1, s2, L, C):
    '''
    s1: the first stock
    s2: the second stock
    L: the length of historical data used to estimate the best ratio
    '''
    n = s1.size
    x = np.zeros(n - L)
    s1_train = s1[:L]
    s2_train = s2[:L]  
    b = get_optimal_ratio(s1_train, s2_train, C) 
    x = s1[L:] - b * s2[L:]
    return s1[L:], s2[L:], x, b

def find_minimum(x, C):
    n = x.size
    s = np.std(x)
    index_min = []
    # Check the first point
    j = 1
    res = False
    while j < n:
        if x[j] >= x[0] and x[j] - x[0] > C*s:
            res = True
            break
        if x[j] < x[0]:
            res = False
            break
        if x[j] >= x[0] and x[j] - x[0] < C*s:
            j += 1
    if res:
        index_min.append(0)
    # Check inner points
    for i in range(1, (n-1)):
        # test the left values
        j = 1
        res_left = False
        while i-j >= 0:
            if x[i-j] >= x[i] and x[i-j] - x[i] > C*s:
                res_left = True
                break
            if x[i-j] < x[i]:
                res_left = False
                break
            if x[i-j] >= x[i] and x[i-j] - x[i] < C*s:
                j += 1
        # test the right values
        j = 1
        res_right = False
        while i+j <= n-1:
            if x[i+j] >= x[i] and x[i+j] - x[i] > C*s:
                res_right = True
                break
            if x[i+j] < x[i]:
                res_right = False
                break
            if x[i+j] >= x[i] and x[i+j] - x[i] < C*s:
                j += 1
        # If both left and right results are true, append index          
        if res_left and res_right:
            index_min.append(i)
    # Check the last point
    j = 1
    res = False
    while n-1-j > -1:
        if x[n-1-i] >= x[n-1] and x[n-1-i] - x[n-1] > C*s:
            res = True
            break
        if x[n-1-i] < x[n-1]:
            res = False  
            break
        if x[n-1-i] >= x[n-1] and x[n-1-i] - x[n-1] < C*s:
            i += 1
    if res:
        index_min.append(n-1)

    return index_min

def find_maximum(x, C):
    n = x.size
    s = np.std(x)
    index_max = []
    # Check the first point
    j = 1
    res = False
    while j < n:
        if x[j] <= x[0] and x[0] - x[j] > C*s:
            res = True
            break
        if x[j] > x[0]:
            res = False
            break
        if x[j] <= x[0] and x[0] - x[j] < C*s:
            j += 1
    if res:
        index_max.append(0)
    # Check inner points
    for i in range(1, (n-1)):
        # test the left values
        res_left = False
        j = 1
        while i-j >= 0:
            if x[i-j] <= x[i] and x[i] - x[i-j] > C*s:
                res_left = True
                break
            if x[i-j] > x[i]:
                res_left = False
                break
            if x[i-j] <= x[i] and x[i] - x[i-j] < C*s:
                j += 1
        # test the right values
        res_right = False
        j = 1
        while i+j <= n-1:
            if x[i+j] <= x[i] and x[i] - x[i+j] > C*s:
                res_right = True
                break
            if x[i+j] > x[i]:
                res_right = False
                break
            if x[i+j] <= x[i] and x[i] - x[i+j] < C*s:
                j += 1
        # If both left and right results are true, append index          
        if res_left and res_right:
            index_max.append(i)
    # Check the last point
    j = 1
    res = False
    while n-1-j > -1:
        if x[n-1-j] <= x[n-1] and x[n-1] - x[n-1-j] > C*s:
            res = True
            break
        if x[n-1-j] > x[n-1]:
            res = False  
            break
        if x[n-1-j] <= x[n-1] and x[n-1] - x[n-1-j] < C*s:
            j += 1
    if res:
        index_max.append(n-1)  
    return index_max

