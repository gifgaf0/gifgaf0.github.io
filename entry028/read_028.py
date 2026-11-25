"""read_028.py -- reader for gen_028 binary records (shared by build and analysis)."""
import numpy as np
REC = np.dtype([('magic', '<u8'), ('r', '<u8'), ('y_r', '<u8'), ('s_r', '<u8'), ('nkept', '<u8'), ('first', '<u8'),
                ('last', '<u8'), ('sum', '<u8'), ('xor', '<u8'), ('pair_index', '<u8'), ('pair_p', '<u8'),
                ('pair_q', '<u8'), ('flags', '<u8'), ('nseen', '<u8'), ('lag1', '<u4', (256,)), ('lag2', '<u4', (256,))])
MAGIC = 0x3832304E45474545
def read(fn): return np.fromfile(fn, REC)
