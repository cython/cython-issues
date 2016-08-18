"""
  array.pxd
  
  Cython direct interface to Python's array.array type (builtin module).
  
  * 1D contiguous data view
  * 2D views - contigious or [x,y] transposed/strided
  * tools for fast array creation, maximum C-speed and handiness
  * suitable as allround light weight auto-array within Cython code too
  
  See also: array_example.pyx
  
  Usage:
  
    cimport array

  Usage through Cython buffer interface (Py2.3+):  
  
    @cython.boundscheck(False)
    def f(arg1, unsigned i, double dx)
        array.array[double] a = arg1
        a[i] += dx
  
  Fast C-level new_array(_zeros), resize_array, copy_array, .length,
  zero_array
  
    cdef array.array[double] k = array.copy_array(d) 
    cdef array.array[double] n = array.new_array(d, d.length * 2 ) 
    cdef array.array[double] m = array.new_array_zeros(FLOAT_TEMPLATE, 100)
    array.resize_array(f, 200000)
  
  Zero overhead with naked data pointer views by union: 
  _f, _d, _i, _c, _u, ... 
  => Original C array speed + Python dynamic memory management

    cdef array.array a = inarray
    if 
    a._d[2] += 0.66   # use as double array without extra casting
  
    float *subview = vector._f + 10  # starting from 10th element
    unsigned char *subview_buffer = vector._B + 4  
    
  Suitable as lightweight arrays intra Cython without speed penalty. 
  Replacement for C stack/malloc arrays; no trouble with refcounting, 
  mem.leaks; seamless Python compatibility, buffer() option
  
  2D views on the memory:
  
    array.array[float, ndim=2] my2Dview = view2D(inarray, columns)
    my2Dview[1,3] *= factor
    
  2D transposed [X,Y] access style (convenient for 'graphical thinking')
  
    array.array[float, ndim=2, mode="strided"] myXYview = view2D(inarray, -columns)
    myXYview[3,1] *= factor
      

  IMPORTANT: arrayarray.h (arrayobject, arraydescr) is not part of 
             the official Python C-API so far; arrayarray.h is located 
             next to this file copy it to PythonXX/include or local or 
             somewhere on your -I path 

  last changes: 2009-05-14 rk
"""
#from python_type cimport *

cimport python_buffer as pybuf
cimport stdlib
cimport python_version


ctypedef void PyTypeObject
ctypedef int Py_UNICODE
    #
cdef extern from "stdlib.h" nogil:
    void *memset(void *str, int c, size_t n)
    char *strcat(char *str1, char *str2)
    char *strncat(char *str1, char *str2, size_t n)
    void *memchr(void *str, int c, size_t n)
    int memcmp(void *str1, void *str2, size_t n)
    void *memcpy(void *str1, void *str2, size_t n)
    void *memmove(void *str1, void *str2, size_t n)


cdef extern from "arrayarray.h":
    void* PyMem_Realloc(void *p, size_t n)
    ##ctypedef int Py_intptr_t
    ##ctypedef Py_intptr_t npy_intp

    ctypedef struct arraydescr:  # [object arraydescr]:
            int typecode
            int itemsize
            #PyObject * (*getitem)(struct arrayobject *, Py_ssize_t);
            #int (*setitem)(struct arrayobject *, Py_ssize_t, PyObject *);

    ctypedef class array.array [object arrayobject]:
        cdef __cythonbufferdefaults__ = {'ndim' : 1, 'mode':'c'}
        ##cdef __cythonbufferdefaults__ = {"mode": "strided"}
        
        cdef:
            object ob_type
            int ob_size             # number of valid items; 
            unsigned length         # = the same 
            
            char* ob_item           # to first item
            Py_ssize_t allocated    # bytes
            arraydescr* ob_descr    # struct arraydescr *ob_descr;
            object weakreflist      # /* List of weak references */

            # view's of ob_item:
            float* _f               # direct float pointer access
            double* _d              # double ...
            int*    _i
            unsigned *_I
            unsigned char *_B
            signed char *_b
            char *_c
            unsigned long *_L
            long *_l
            short *_h
            unsigned short *_H
            Py_UNICODE *_u

        #$9 method decorations don't work so far => module function
        #$9 cdef inline resize(array self, int n):   
        #$9        PyMem_Realloc(self.ob_item, n * self.ob_descr.itemsize)
                
        # Note: This syntax (function definition in pxd files) is an
        # experimental exception made for __getbuffer__ and __releasebuffer__
        # -- the details of this may change.
        def __getbuffer__(array self, Py_buffer* info, int flags):
            # This implementation of getbuffer is geared towards Cython
            # requirements, and does not yet fullfill the PEP.
            # In particular strided access is always provided regardless
            # of flags
            cdef unsigned ndim, rows, columns, itemsize
            
            info.strides = NULL
            info.shape = NULL
            info.suboffsets = NULL

            info.buf = self.ob_item
            info.readonly = 0
            info.itemsize = itemsize = self.ob_descr.itemsize   # e.g. sizeof(float)
            
            global _viewhelper_shape2
            if _viewhelper_shape2: 
                
                #2D view    
                ndim = 2                
                info.strides = <Py_ssize_t*> \
                               stdlib.malloc(sizeof(Py_ssize_t) * ndim * 2 + 2)
                info.shape = info.strides + ndim

                if _viewhelper_shape2>0:
                    columns = _viewhelper_shape2
                    rows = (self.ob_size // columns)
                    info.shape[0] = rows 
                    info.shape[1] = columns
                    info.strides[0] = itemsize * columns
                    info.strides[1] = info.itemsize                     
                else:
                    columns = -_viewhelper_shape2
                    rows = (self.ob_size // columns)
                    info.shape[0] = rows 
                    info.shape[1] = columns
                    info.strides[0] = info.itemsize
                    info.strides[1] = itemsize * columns        
                _viewhelper_shape2 = 0
                
            else: 
                
                ndim = 1
                # one memory block for strides + shape + format
                info.strides = <Py_ssize_t*> \
                               stdlib.malloc(sizeof(Py_ssize_t) * ndim * 2 + 2)
                info.shape = info.strides + ndim
                info.shape[0] = self.ob_size            # number of items
                info.strides[0] = info.itemsize         

            info.ndim = ndim
            info.format = <char*>(info.strides + 2 * ndim)
            info.format[0] = self.ob_descr.typecode
            info.format[1] = 0
            info.obj = self
            #print "array.pyx NDIM rows columns", ndim, rows, columns

        def __releasebuffer__(array self, Py_buffer* info):
            #if PyArray_HASFIELDS(self):
            #    stdlib.free(info.format)
            #if sizeof(npy_intp) != sizeof(Py_ssize_t):
            stdlib.free(info.strides)
            ##print "__releasebuffer__"
    Py_ssize_t _viewhelper_shape2 # helper

    array newarrayobject(PyTypeObject* type, Py_ssize_t size, 
                              arraydescr *descr)

    # // fast resize/realloc. simply: allocated = n 
    # not suitable for small increments
    void resize_array(array self, Py_ssize_t n)
    void resize_array_smart(array self, Py_ssize_t n)   # not for Py2.3?


#  fast creation of a new array - init with zeros 
#  yet you need a (any) template array of the same item type (but not same size)
cdef inline array new_array_zeros(array sametype, unsigned n):
    cdef array op = newarrayobject( <PyTypeObject*>sametype.ob_type, n, sametype.ob_descr)
    memset(op.ob_item, 0, n * op.ob_descr.itemsize)
    return op

#  fast creation of a new array - no init with zeros 
cdef inline array new_array(array sametype, unsigned n):
    return newarrayobject( <PyTypeObject*>sametype.ob_type, n, sametype.ob_descr)

# dn : additional size
cdef inline array copy_array(array self):
    cdef array op = newarrayobject( <PyTypeObject*>self.ob_type, self.ob_size, self.ob_descr)
    memcpy(op.ob_item, self.ob_item, op.ob_size * op.ob_descr.itemsize)
    return op
    
cdef inline void zero_array(array op):
    memset(op.ob_item, 0, op.ob_size * op.ob_descr.itemsize)

cdef inline Py_ssize_t array_rows(array self, unsigned columns): 
    return self.ob_size // columns

# 2D view setup (only) must occur within GIL. But
# anyway: "Python type test not allowed without gil"
cdef inline array view2D(array self, Py_ssize_t columns):
    """ view the array through 2D window 
    to be used like:  
    
        cdef array.array[double, ndim=2] my2dview = view2D(inarray, rows)
      
    negative rows => [x,y] access logic (columns and rows transposed) to
    the memory. Mode "strided" has to be used for that. 
    
        cdef array.array[double, ndim=2, mode="strided"] myXYview = view2D(inarray, -rows)
    """
    global _viewhelper_shape2
    _viewhelper_shape2 = columns
    return self


    