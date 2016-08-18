import numpy as np
cimport numpy as np
import sys



cdef extern from "badmat.h" :
    ctypedef struct dim3:
        int x, y, z
    ctypedef enum MatrixType :
        Realmatrix = 0
        Complexmatrix=1
        Cuppermatrix = 2
    ctypedef struct gpumat
    void fromgpu(gpumat &gin, float *hval) 
    cdef cppclass gpumat: 
        int nrows 
        int ncols 
        int ld 
        MatrixType mtype 
        float *val 
        dim3 block 
        dim3 grid 
        dim3 residual 
        gpumat() 



