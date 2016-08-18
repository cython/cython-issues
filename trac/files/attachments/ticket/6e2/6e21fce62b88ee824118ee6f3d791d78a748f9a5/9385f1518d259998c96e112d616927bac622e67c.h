/* arrayarray.h  

    artificial C-API for Python's 
    <array.array> type.
    copy this file to your -I path, e.g. .../pythonXX/include
    See array.pxd next to this file
    
    last changes: 2009-05-14 rk

*/

#ifndef _ARRAYARRAY_H
#define _ARRAYARRAY_H

#include <Python.h>

struct arrayobject; /* Forward */

/* All possible arraydescr values are defined in the vector "descriptors"
 * below.  That's defined later because the appropriate get and set
 * functions aren't visible yet.
 */
typedef struct arraydescr {
	int typecode;
	int itemsize;
	PyObject * (*getitem)(struct arrayobject *, Py_ssize_t);
	int (*setitem)(struct arrayobject *, Py_ssize_t, PyObject *);
} arraydescr;

#if PY_VERSION_HEX < 0x02040000
typedef struct arrayobject {
	PyObject_HEAD
	int ob_size;
	char *ob_item;
	struct arraydescr *ob_descr;
} arrayobject;
#else
typedef struct arrayobject {
	PyObject_HEAD       //includes ob_size!
    union {
        int ob_size;
        unsigned length;
    };
    union {
	    char *ob_item;
        float *_f;
        double *_d;
        int *_i;
        unsigned *_I;
        unsigned char *_B;
        signed char *_b;
        char *_c;
        unsigned long *_L;
        long *_l;
        short *_h;
        unsigned short *_H;
        Py_UNICODE *_u;
    };
	Py_ssize_t allocated;
	struct arraydescr *ob_descr;
	PyObject *weakreflist; /* List of weak references */
} arrayobject;
#endif


#ifndef NO_NEWARRAY_INLINE
/* 
 * 
 *  fast creation of a new array - init with zeros
 */
 
static inline PyObject *
newarrayobject(PyTypeObject *type, Py_ssize_t size, struct arraydescr *descr)
{
	arrayobject *op;
	size_t nbytes;

	if (size < 0) {
		PyErr_BadInternalCall();
		return NULL;
	}

	nbytes = size * descr->itemsize;
	/* Check for overflow */
	if (nbytes / descr->itemsize != (size_t)size) {
		return PyErr_NoMemory();
	}
	op = (arrayobject *) type->tp_alloc(type, 0);
	if (op == NULL) {
		return NULL;
	}
	op->ob_descr = descr;
#if !( PY_VERSION_HEX < 0x02040000 )
	op->allocated = size;
	op->weakreflist = NULL;
#endif
	Py_SIZE(op) = size;
	if (size <= 0) {
		op->ob_item = NULL;
	}
	else {
		op->ob_item = PyMem_NEW(char, nbytes);
		if (op->ob_item == NULL) {
			Py_DECREF(op);
			return PyErr_NoMemory();
		}
//      memset(op->ob_item,0,nbytes);  // only in new_array_zeros
	}
	return (PyObject *) op;
}
#else
PyObject *
newarrayobject(PyTypeObject *type, Py_ssize_t size, struct arraydescr *descr);
#endif

// fast resize (realloc to the point) 
// not designed for filing small increments (but for fast opaque array apps)
static inline void resize_array(arrayobject *self, Py_ssize_t n) 
{
    self->ob_item = PyMem_Realloc(self->ob_item, n * self->ob_descr->itemsize);
    self->ob_size = n;
#if PY_VERSION_HEX >= 0x02040000
    self->allocated = n;  //$23
#endif
}

#if PY_VERSION_HEX >= 0x02040000
// suitable for small increments; over-alloc 50%
static inline void resize_array_smart(arrayobject *self, Py_ssize_t n) 
{
    if (n < self->allocated) 
        if (n*4 > self->allocated) {
            self->ob_size = n;
            return;
        }
    Py_ssize_t newsize = n  * 3 / 2 + 1;
    self->ob_item = PyMem_Realloc(self->ob_item, newsize * self->ob_descr->itemsize );
    self->ob_size = n;
    self->allocated = newsize;  //$23
}
#endif


// hack for Cython 2D buffer view set-up; needs GIL only during setup
static Py_ssize_t _viewhelper_shape2=0;  

#endif
/* _ARRAYARRAY_H */
