import numpy as np
from .mle_ou import mle_ou
from.mean_reversion_time import get_mean_reverse_time

def ou_get_best_ratio(s1, s2, dt):
    '''  
    Input: a pair of time series
    Output: the best ratio to construct a mean reversion spread
    '''
    s1 = np.array(s1)
    s2 = np.array(s2)
    b_list = (np.arange(600) - 300) / 100
    ll_list = []
    for i in range(400):
        x = s1 - b_list[i] * s2
        ll = mle_ou(x, dt)['ll']
        ll_list.append(ll) 
    b_best = b_list[np.argmax(ll_list)]
    
    return b_best

def mrt_get_best_ratio(s1, s2, C):
    s1 = np.array(s1)
    s2 = np.array(s2)
    b_list = (np.arange(600) - 300) / 100
    reverse_time_list = []
    for i in range(400):
        x = s1 - b_list[i] * s2
        reverse_time = get_mean_reverse_time(x, C) 
        reverse_time_list.append(reverse_time)
    b_best = b_list[np.argmin(reverse_time_list)]

    return b_best
