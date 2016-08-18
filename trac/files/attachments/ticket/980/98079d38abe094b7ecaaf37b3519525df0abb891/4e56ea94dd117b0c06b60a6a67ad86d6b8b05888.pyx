    
cdef class Lock:
    def __init__(self):
        raise TypeError('You should not instantiate this class, use the '
                        'provided instance instead.')

    def acquire(self, timeout=None):
        return 42

    def release(self, *a):
        '''Release global lock'''
        pass

    __enter__ = acquire
    __exit__ = release

