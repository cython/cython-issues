"""
    shows Usage of array.pxd 
    ( fast Cython interface to Python's builtin array type )
    
    last changes: 2009-05-14 rk
"""

import array  # Python builtin module  
cimport array  # array.pxd / arrayarray.h

import cython

@cython.boundscheck(False)
cdef array.array calc(a, int columns, float factor):
    """resize and compute array inplace - no new objects"""
    
    array.resize_array(a, columns*columns)
    
    # fast linear view
    cdef array.array[float] b = a 
    
    # fast 2D view
    cdef array.array[float, ndim=2] aa = array.view2D(a, columns) 
    
    # fast 2D [x,y] transposed view (e.g. for 'graphical thinking')
    # ( costs one multiplication per index computation)
    cdef array.array[float, ndim=2, mode="strided"] xy_view = \
        array.view2D(a, -columns) # negativ columns => [x,y]        
    
    # C-fast [x,y] buffer view access
    cdef int mid = columns // 2
    cdef unsigned x, y
    for y in range(columns):
        ##print x,y
        for x in range(columns): 
            xy_view[x, y] = factor * ( mid - <int>x ) * ( mid - <int>y ) 

    print "calc:", b, columns, array.array_rows(aa,columns)

    # C-fast things:
    print b.length, aa[3,1]

    return xy_view

def pandoras_box(a, unsigned n): 
    """ produces many arrays quickly """
    l=[]  # Python list for outer container
    cdef unsigned i, j
    cdef array.array b = a  # fast access, no view buffer overhead
    if b.ob_descr.typecode != 'f':  # C-fast check of data type
        raise RuntimeError, "wrong type"
    for i in range(n):
        b = array.copy_array(a)  # C-fast: duplicate array
        for j in range(b.length):
            # simple indexing would be P-slow without a buffer view
            ## b[j] += (j + i) * 0.01  
            # handy direct float* cast; always C-fast, no bounds check
            b._f[j] += (j + i) * 0.01  
        l.append(b)
    z = array.new_array_zeros(b, n)  # C-fast empty array from template type
    return l,z
        

def test(): 
    print "array_example test ..."
    a = array.array('f')
    cdef array.array hot = a  # for C-fast array usage
    print hot, hot.length
    calc(a, 5, 1.01)
    print hot
    print 'bytes:', hot.length * hot.ob_descr.itemsize
    print hot._f[0] # take a float by chance
    print 'memory section:', repr(hot._c[12:24])  #directly as char buffer
    print 'memory:', repr(hot.tostring())
    lst,z = pandoras_box(hot,3)
    print z 
    print lst
    assert len(z) == 3 and z[0] == 0.0
    assert 4.2 < lst[2][24] < 4.4
    print "done."
    return lst
