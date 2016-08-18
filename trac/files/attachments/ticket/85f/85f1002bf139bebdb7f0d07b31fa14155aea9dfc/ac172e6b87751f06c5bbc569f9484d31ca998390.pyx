import cython
import numpy as np
cimport numpy as np

ctypedef np.float64_t dtype_t
dtype = np.float64

def matmul_cy(np.ndarray[dtype_t, ndim=2] A,
              np.ndarray[dtype_t, ndim=2] B,
              np.ndarray[dtype_t, ndim=2] out=None):
    cdef int i, j, k
    cdef dtype_t s
    
    if A.shape[1] != B.shape[0]:
        raise ValueError("Matrices are not aligned")
    outshape = (A.shape[0], B.shape[1])
    if out is None:
        out = np.empty(outshape, A.dtype)
    elif out.shape[0] != outshape[0] and out.shape[1] != outshape[1]:
        raise ValueError("Output array has wrong size")
    
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            s = 0
            for k in range(A.shape[1]):
                s += A[i, k] * B[k, j]
            out[i,j] = s
                
    return out

@cython.boundscheck(False)
def matmul_cy_2(np.ndarray[dtype_t, ndim=2] A,
                np.ndarray[dtype_t, ndim=2] B,
                np.ndarray[dtype_t, ndim=2] out=None):
    cdef unsigned int i, j, k
    cdef dtype_t s
    
    if A.shape[1] != B.shape[0]:
        raise ValueError("Matrices are not aligned")
    outshape = (A.shape[0], B.shape[1])
    if out is None:
        out = np.empty(outshape, A.dtype)
    elif out.shape[0] != outshape[0] and out.shape[1] != outshape[1]:
        raise ValueError("Output array has wrong size")
    
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            s = 0
            for k in range(A.shape[1]):
                s += A[i, k] * B[k, j]
            out[i,j] = s
                
    return out
