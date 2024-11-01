import numpy as np
import iisignature as iisig

def signature_distance(series1, series2, sig_level):
    '''
    input: 1d np.array
    output: signature distance
    '''
    # compute on the whole time interval
    n = len(series1)
    t = np.linspace(0, n, n)
    aug_series1 = np.transpose(np.array([t, np.array(series1)]))
    aug_series2 = np.transpose(np.array([t, np.array(series2)]))
    signature1 = iisig.sig(aug_series1, sig_level)
    signature2 = iisig.sig(aug_series2, sig_level)
    d1 = np.linalg.norm(np.array(signature1) - np.array(signature2))

    # compute on the two pieces
    n = int(len(series1) / 2)
    t = np.linspace(0, n, n)
    aug_series1 = np.transpose(np.array([t, np.array(series1)[:n]]))
    aug_series2 = np.transpose(np.array([t, np.array(series2)[:n]]))
    signature1 = iisig.sig(aug_series1, sig_level)
    signature2 = iisig.sig(aug_series2, sig_level)
    d2 = np.linalg.norm(np.array(signature1) - np.array(signature2))

    aug_series1 = np.transpose(np.array([t, np.array(series1)[n:]]))
    aug_series2 = np.transpose(np.array([t, np.array(series2)[n:]]))
    signature1 = iisig.sig(aug_series1, sig_level)
    signature2 = iisig.sig(aug_series2, sig_level)
    d3 = np.linalg.norm(np.array(signature1) - np.array(signature2))   

    # compute on the four pieces
    n = int(len(series1) / 4)
    t = np.linspace(0, n, n)
    aug_series1 = np.transpose(np.array([t, np.array(series1)[:n]]))
    aug_series2 = np.transpose(np.array([t, np.array(series2)[:n]]))
    signature1 = iisig.sig(aug_series1, sig_level)
    signature2 = iisig.sig(aug_series2, sig_level)
    d4 = np.linalg.norm(np.array(signature1) - np.array(signature2))

    aug_series1 = np.transpose(np.array([t, np.array(series1)[n:2*n]]))
    aug_series2 = np.transpose(np.array([t, np.array(series2)[n:2*n]]))
    signature1 = iisig.sig(aug_series1, sig_level)
    signature2 = iisig.sig(aug_series2, sig_level)
    d5 = np.linalg.norm(np.array(signature1) - np.array(signature2))  

    aug_series1 = np.transpose(np.array([t, np.array(series1)[2*n:3*n]]))
    aug_series2 = np.transpose(np.array([t, np.array(series2)[2*n:3*n]]))
    signature1 = iisig.sig(aug_series1, sig_level)
    signature2 = iisig.sig(aug_series2, sig_level)
    d6 = np.linalg.norm(np.array(signature1) - np.array(signature2))

    aug_series1 = np.transpose(np.array([t, np.array(series1)[3*n:]]))
    aug_series2 = np.transpose(np.array([t, np.array(series2)[3*n:]]))
    signature1 = iisig.sig(aug_series1, sig_level)
    signature2 = iisig.sig(aug_series2, sig_level)
    d7 = np.linalg.norm(np.array(signature1) - np.array(signature2))  

    d = (d1+d2+d3+d4+d5+d6+d7) / 7
    return d

def ssd_distance(series1, series2):
    '''
    input: 1d np.array
    output: euclidean distance
    '''
    d = np.linalg.norm(np.array(series1) - np.array(series2)) ** 2
    return d