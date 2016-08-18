typedef  struct {
unsigned int x,y,z ;
} dim3 ;

typedef enum {
	Realmatrix = 0,
	Complexmatrix=1 ,
	Cuppermatrix = 2,
} MatrixType ;


class badmat {
int nrows  ;
int ncols  ;
int ld  ;
MatrixType mtype  ;
float *val  ;
dim3 block  ;
dim3 grid  ;
dim3 residual  ;

badmat() {}



} ;
