import numpy as np
cimport numpy as np

def masked_bug(np.ndarray[np.float64_t] ma):
    # direct access works fine:
    print ma
    ma[1] = 9999.
    print ma
    # but there is nothing in ma.data!
    print 'bug       ', type(ma), ' data: ', ma.data, ' type of data: ', type(ma.data), ' mask: ', ma.mask
    # hack from http://radlab.soest.hawaii.edu/sunset0/adcp_programs/pycurrents/num/src/utility.pyx
    arr = np.array(ma, copy=False, subok=True)
    print 'hack      ', type(arr), ' data: ', arr.data, ' type of data: ', type(arr.data),  ' mask: ', arr.mask
