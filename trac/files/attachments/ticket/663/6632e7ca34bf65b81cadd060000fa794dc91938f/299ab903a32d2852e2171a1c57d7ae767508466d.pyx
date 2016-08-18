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
    cdef cppclass badmat: 
        int nrows 
        int ncols 
        int ld 
        MatrixType mtype 
        float *val 
        dim3 block 
        dim3 grid 
        dim3 residual 
        badmat() 
        void cgauss()
        badmat(unsigned i, unsigned j, unsigned nld, MatrixType mt, float *fptr)  

# Python wrapper for a float pointer
cdef class FloatPtr :
    cdef float *ptr
    cdef setf(FloatPtr self, float *fp) :
        self.ptr = fp
    cdef float *getf(FloatPtr self) :
        return self.ptr

cdef class Gmat:
    cdef badmat *gptr # C++ pointer instance
    def __cinit__(self, int r, int c, int ld, int mt, FloatPtr f):
        if (f.ptr == NULL) :
            self.gptr = new badmat(r,c, ld, <MatrixType> mt)
        else:
            self.gptr = new badmat(r,c,ld,  <MatrixType>  mt,f.ptr)
    def __dealloc__(self) :
        del self.gptr
 

cpdef Gmat cgauss(int r, int c) :
    # cdef MatrixType mtype = Complexmatrix
    cdef FloatPtr f
    f.setf(NULL)
    cdef Gmat  g = Gmat(r,c,r,Complexmatrix, f)
    g.gptr[0].cgauss()
    return(g)


