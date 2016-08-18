import numpy as np
import pyximport; pyximport.install(setup_args={'include_dirs':[np.get_include()]}) 
from bug_masked_arrays import *

ma = np.ma.MaskedArray(np.arange(1.,5.))
ma[3] = np.ma.masked
masked_bug(ma)
